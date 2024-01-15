import os
import json
import pandas as pd
from tqdm import tqdm
from typing import Union
from pathlib import Path


def _date_gt(it, from_date):
    return it.split('/')[-1].split('.')[0] >= from_date


class WordDict:
    def __init__(self, persist_path='./worddict/'):
        self.word_2_idx = {'未知': 0}
        self.idx_2_word = {0: '未知'}
        
        os.makedirs(persist_path, exist_ok=True)
        
        self.w2idx_path = os.path.join(persist_path, 'word_2_idx.json')
        self.idx2w_path = os.path.join(persist_path, 'idx_2_word.json')
        self._load_dict(self.word_2_idx , self.w2idx_path)
        self._load_dict(self.idx_2_word, self.idx2w_path)

    def _load_dict(self, to_dict, path):
        if os.path.exists(path):
            print(f'- load from {path}')
            with open(path, 'r') as f:
                to_dict.update(json.load(f))

    def persist(self):
        with open(self.idx2w_path, 'w') as f:
            json.dump(self.idx_2_word, f, ensure_ascii=False)
        print(f'- persist to {self.idx2w_path}')

        with open(self.w2idx_path, 'w') as f:
            json.dump(self.word_2_idx, f, ensure_ascii=False)
        print(f'- persist to {self.w2idx_path}')

    def update(self, word: Union[str, dict]):
        if isinstance(word, float):
            return
        elif isinstance(word, str):
            if word not in self.word_2_idx:
                self.idx_2_word[len(self.word_2_idx)] = word
                self.word_2_idx[word] = len(self.word_2_idx)
        
        elif isinstance(word, dict):
            for key in word.keys():
                if key not in self.word_2_idx:
                    self.idx_2_word[len(self.word_2_idx)] = key
                    self.word_2_idx[key]= len(self.word_2_idx)
    
    def get_idx(self, word: str) -> int:
        if word not in self.word_2_idx:
            return 0
        else:
            return self.word_2_idx[word]

    def get_word(self, idx: int) -> str:
        if idx not in self.idx_2_word:
            return '未知'
        return self.idx_2_word[idx]
    
    def __len__(self):
        return len(self.word_2_idx)
    
    def _eval_item(self, x):
        if isinstance(x, float):  # nan
            return {}
        return eval(x)
    
    def collect(self, datas_path, col_name, from_date=None, need_eval=False):
        tmp_items = list(Path(datas_path).glob('*.tsv'))
        # 过滤不需要处理的日期数据
        items = []
        for it in tmp_items:
            if from_date is None:
                items.append(it)
            elif _date_gt(it, from_date):
                items.append(it)

        for it in tqdm(items):
            df = pd.read_csv(it, sep='\t')
            if need_eval:
                df[col_name] = df[col_name].apply(self._eval_item)
            df[col_name].apply(self.update)
