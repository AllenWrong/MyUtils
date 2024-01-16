python demo.py \
  --seed 42 \
  --epoch 5 \
  --batch_size 128 \
  --device 'cuda:2' \
  --lr 1e-3 \
  --weight_decay 0.0 \
  --data_path './data/feature/' \
  --ckp_path './ckps/resume1' \
  --use_sched_ckp false \
  --out_ckp_path './ckps/resume2' \
  --log_dir './log/resume1'

#   --ckp_path './ckps/resume' \