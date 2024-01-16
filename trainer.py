import os
import json
from torch.utils.tensorboard.writer import SummaryWriter
import torch
from logger import setup_logger
from tqdm import tqdm
import numpy as np


class Trainer:
    def __init__(
        self,
        device,
        model,
        criterion,
        optimizer,
        args,
        metrics_dict,
        sched=None,
        use_writer=True
    ):
        self.device = device
        self.model = model.to(device)
        self.optimizer = optimizer
        self.sched = sched
        self.criterion = criterion
        self.args = args
        self.base_epoch = args.base_epoch
        self._pre_config()

        if args.ckp_path is not None:
            json_info = self.load_torch_model()
            self.base_epoch = json_info['epoch'] + 1
        
        if use_writer:
            self.writer = SummaryWriter(log_dir=args.log_dir)
        else:
            self.writer = None
        self.metrics_dict = metrics_dict

    def _pre_config(self):
        # out ckp path config
        os.makedirs(self.args.out_ckp_path, exist_ok=True)
        with open(os.path.join(self.args.out_ckp_path, 'args.json'), 'w') as f:
            json.dump(self.args.__dict__, f)
        self.logger = setup_logger('trainer', os.path.join(self.args.out_ckp_path, 'trainer.log'))

    def fit(self, train_loader, valid_loader, test_loader=None):
        best_auc = 0.0
        for epoch in range(self.base_epoch, self.base_epoch + self.args.epochs):
            losses = []
            preds = []
            targets = []

            prograss_bar = tqdm(train_loader, leave=False)
            for x, y in prograss_bar:
                x = x.to(self.device)
                y = y.to(self.device)

                sim_logits = self.model.forward(x)
                loss = self.criterion(sim_logits, y)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                losses.append(loss.item())

                prograss_bar.set_postfix_str(f'loss={loss.item()}')
                
                preds.append(sim_logits.detach())
                targets.append(y.detach())

            preds = torch.concat(preds, dim=0)
            targets = torch.concat(targets, dim=0)
            loss_val = np.mean(losses)
            train_metrics_val = self._compute_metrics(preds, targets)
            train_metrics_val.update({'loss': loss_val})
            
            if self.sched is not None:
                self.sched.step()
            
            valid_metrics_val = self.valid(valid_loader)
            if valid_metrics_val['auc'] > best_auc:
                best_auc = valid_metrics_val['auc']
                self.save_torch_model(
                    {'epoch': epoch, 'train_auc': train_metrics_val['auc'], 'valid_auc': valid_metrics_val['auc']}
                )

            self._write_tensorboard(train_metrics_val, valid_metrics_val, self.optimizer.param_groups[0]['lr'], epoch)
            self._print_metrics_val(epoch, train_metrics_val, valid_metrics_val)

    def _print_metrics_val(self, epoch, train_met_val, valid_met_val, test_met_val=None):
        info = f"[epoch: {epoch}] "
        for k, v in train_met_val.items():
            info += f"{k}: {v:.6f}, "
        for k, v in valid_met_val.items():
            info += f"{k}: {v:.6f}, "
        if test_met_val is not None:
            for k, v in test_met_val.items():
                info += f"{k}: {v:.6f}, "
        self.logger.info(info)

    def _write_tensorboard(self, train_met_val, valid_met_val, lr, step, test_met_val=None):
        """
        Args:
            cate: train/valid/test
            metrics_val: a dict. {matric_name: value}
        """
        def _helper(cate, met_val):
            for k, v in met_val.items():
                self.writer.add_scalar(f'{k}/{cate}', v, step)
        _helper('train', train_met_val)
        _helper('valid', valid_met_val)
        if test_met_val is not None:
            _helper('test', test_met_val)
        self.writer.add_scalar('lr', lr, step)

    @torch.no_grad()
    def _compute_metrics(self, preds: torch.Tensor, targets: torch.Tensor) -> dict:
        """
        Return:
            `{acc: 0.99999, auc: 0.9999, ...}`
        """
        metrics_res = {}
        for k, fn in self.metrics_dict.items():
            metrics_res[k.name] = fn(preds, targets).item()
        return metrics_res

    @torch.no_grad()
    def valid(self, valid_loader):
        self.model.eval()

        with torch.no_grad():
            losses = []
            targets = []
            preds = []
            prograss_bar = tqdm(valid_loader, leave=False)
            for x, y in prograss_bar:
                x = x.to(self.device)
                y = y.to(self.device)
                sim_logits = self.model(x)
                loss = self.criterion(sim_logits, y).item()
                losses.append(loss)
                targets.append(y.detach())
                preds.append(sim_logits.detach())
                prograss_bar.set_postfix_str(f'loss={loss}')
        self.model.train()

        preds = torch.concat(preds, dim=0)
        targets = torch.concat(targets, dim=0)
        eval_metrics_val = self._compute_metrics(preds, targets)
        eval_metrics_val.update({'loss': np.mean(losses)})
        return eval_metrics_val

    def load_torch_model(self) -> dict:
        """load state and return checkpoint info"""
        path_dir = self.args.ckp_path
        info = f'- loaded from {path_dir}, for model'
        self.model.load_state_dict(torch.load(os.path.join(path_dir, 'model.pth')))

        if self.optimizer is not None:
            self.optimizer.load_state_dict(torch.load(os.path.join(path_dir, 'opt.pth')))
            info += ', for opt'
        if self.args.use_sched_ckp and self.sched is not None:
            self.sched.load_state_dict(torch.load(os.path.join(path_dir, 'sched.pth')))
            info += ', for sched'

        with open(os.path.join(path_dir, 'config.json'), 'r') as f:
            config = json.load(f)
        self.logger.info(info)
        return config

    def save_torch_model(self, json_info: dict):
        """
        Args:
            json_info: 
        """
        torch.save(self.model.state_dict(), os.path.join(self.args.out_ckp_path, 'model.pth'))
        torch.save(self.optimizer.state_dict(), os.path.join(self.args.out_ckp_path, 'opt.pth'))
        if self.sched is not None:
            torch.save(self.sched.state_dict(), os.path.join(self.args.out_ckp_path, 'sched.pth'))
        
        with open(os.path.join(self.args.out_ckp_path, 'config.json'), 'w') as f:
            json.dump(json_info, f)

        self.logger.info(f'- saved model in {self.args.out_ckp_path}')
