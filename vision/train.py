"""Train the model"""

import argparse
import logging
import os
import random
from torch.utils.data import DataLoader
import numpy as np
import torch
import torch.optim as optim
import torchvision.datasets
from tqdm import tqdm

import utils
import model.net as net
import model.data_loader as data_loader
from evaluate import evaluate
import time

# this code is referenced from cs230
rand_seed = 230


def train(model, optimizer, loss_fn, dataloader, metrics, params):
    """Train the model on `num_steps` batches

    Args:
        model: (torch.nn.Module) the neural network
        optimizer: (torch.optim.optim.Optimizer) optimizer for parameters of model
        loss_fn: a function that takes batch_output and batch_labels and computes the loss for the batch
        dataloader: (DataLoader) a torch.utils.data.DataLoader object that fetches training data
        metrics: (dict) a dictionary of functions that compute a metric using the output and labels of each batch
        params: (Params) hyper-parameters
    """
    # set model to training mode
    model.train()

    # summary for current training loop and a running average object for loss
    summ = []
    loss_avg = utils.RunningAverage()

    # Use tqdm for progress bar
    with tqdm(total=len(dataloader)) as t:
        for i, (train_batch, labels_batch) in enumerate(dataloader):
            # move to GPU if available
            if params.cuda:
                train_batch = train_batch.cuda(non_blocking=True)
                labels_batch = labels_batch.cuda(non_blocking=True)

            # compute model output and loss
            output_batch = model(train_batch)
            loss = loss_fn(output_batch, labels_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Evaluate summaries only once in a while
            if i % params.save_summary_steps == 0:
                # extract data from torch Variable, move to cpu, convert to numpy arrays
                output_batch = output_batch.data.cpu().numpy()
                labels_batch = labels_batch.data.cpu().numpy()

                # compute all metrics on this batch
                summary_batch = {metric: metrics[metric](output_batch, labels_batch)
                                 for metric in metrics}
                summary_batch['loss'] = loss.item()
                summ.append(summary_batch)

            # update the average loss
            loss_avg.update(loss.item())

            t.set_postfix(loss='{:.8f}'.format(loss_avg()))
            t.update()

    # compute mean of all metrics in summary
    metrics_mean = {metric: np.mean([x[metric]
                                     for x in summ]) for metric in summ[0]}
    metrics_string = "; ".join("{}: {:.4f}".format(k, v)
                                for k, v in metrics_mean.items())
    logging.info("- Train metrics: " + metrics_string)


def train_and_evaluate(model, train_dataloader, val_dataloader, optimizer, loss_fn, metrics, params, model_dir,
                       restore_file=None):
    """Train the model and evaluate every epoch.

    Args:
        model: (torch.nn.Module) the neural network
        train_dataloader: (DataLoader) a torch.utils.data.DataLoader object that fetches training data
        val_dataloader: (DataLoader) a torch.utils.data.DataLoader object that fetches validation data
        optimizer: (torch.optim) optimizer for parameters of model
        loss_fn: a function that takes batch_output and batch_labels and computes the loss for the batch
        metrics: (dict) a dictionary of functions that compute a metric using the output and labels of each batch
        params: (Params) hyper-parameters
        model_dir: (string) directory containing config, weights and log
        restore_file: (string) optional- name of file to restore from (without its extension .pth.tar)
    """
    # reload weights from restore_file if specified
    if restore_file is not None:
        restore_path = os.path.join(
            args.model_dir, args.restore_file + '.pth.tar')
        logging.info(f"Restoring parameters from {restore_path}")
        utils.load_checkpoint(restore_path, model, optimizer)

    best_val_acc = 0.0

    for epoch in range(params.num_epochs):
        # Run one epoch
        logging.info("Epoch [{}/{}]".format(epoch + 1, params.num_epochs))

        start_time = time.time()
        # compute number of batches in one epoch (one full pass over the training set)
        train(model, optimizer, loss_fn, train_dataloader, metrics, params)

        # Evaluate for one epoch on validation set
        val_metrics = evaluate(model, loss_fn, val_dataloader, metrics, params)

        end_time = time.time()
        epoch_time = end_time - start_time
        print(f"- Used time: {epoch_time/60:.4f}m, "
              f"estimated remaining time {epoch_time * (params.num_epochs-epoch-1)/60/60:.4}h")

        # May be other metrics
        val_acc = val_metrics['accuracy']
        is_best = val_acc >= best_val_acc

        # Save weights
        utils.save_checkpoint(
            {'epoch': epoch + 1,
             'state_dict': model.state_dict(),
             'optim_dict': optimizer.state_dict()},
            is_best=is_best,
            checkpoint=model_dir)

        # If best_eval, best_save_path
        if is_best:
            logging.info("- Found new best accuracy")
            best_val_acc = val_acc

            # Save best val metrics in a json file in the model directory
            best_json_path = os.path.join(
                model_dir, "metrics_val_best.json")
            utils.save_dict_to_json(val_metrics, best_json_path)

        # Save latest val metrics in a json file in the model directory
        last_json_path = os.path.join(
            model_dir, "metrics_val_last.json")
        utils.save_dict_to_json(val_metrics, last_json_path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='data',
                        help="Path of data")
    parset.add_argument('--data', default='mnist', help='Name of data.')
    parser.add_argument('--model_dir', default='experiments/base_model',
                        help="Directory containing params.json")
    parser.add_argument('--restore_file', default=None,
                        help="Optional, name of the file in --model_dir containing weights to reload before \
                        training")  # 'best' or 'train'

    # Load the parameters from json file
    args = parser.parse_args()
    json_path = os.path.join(args.model_dir, 'params.json')
    assert os.path.isfile(
        json_path), "No json configuration file found at {}".format(json_path)
    params = utils.Params(json_path)

    # use GPU if available
    params.cuda = torch.cuda.is_available()

    # Set the random seed for reproducible experiments
    random.seed(rand_seed)
    np.random.seed(rand_seed)
    torch.manual_seed(rand_seed)
    if params.cuda:
        torch.cuda.manual_seed(rand_seed)

    # Set the logger
    utils.set_logger(os.path.join(args.model_dir, 'train.log'))

    # ---- Create the input data pipeline ----
    logging.info(f"Loading the datasets {args.data}...")

    # fetch dataloaders
    dataloaders = data_loader.fetch_dataloader(
        ['train', 'val'], args.data_dir, params
    )
    train_loader = dataloaders['train']
    val_loader = dataloaders['val']

    logging.info("- done.")

    # ---- Define the model and optimizer ----
    model = net.Net(params).cuda() if params.cuda else net.Net(params)
    optimizer = optim.Adam(model.parameters(), lr=params.learning_rate)

    # fetch loss function and metrics
    # loss_fn = net.loss_fn
    loss_fn = torch.nn.CrossEntropyLoss()
    metrics = net.metrics

    # ---- Train the model ----
    logging.info("Starting training for {} epoch(s)".format(params.num_epochs))
    train_and_evaluate(model, train_loader, val_loader, optimizer, loss_fn, metrics, params, args.model_dir,
                       args.restore_file)
