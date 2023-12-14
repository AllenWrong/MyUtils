from jieba.analyse.tfidf import TFIDF as JiebaTFIDF
import pkuseg
import jieba


class Pkuseg(pkuseg.pkuseg):
    """自定义化的pkuseg类，以支持和jieba.cut同等格式的输出"""
    def __init__(self, model_name="default", user_dict="default", postag=False):
        super().__init__(model_name, user_dict, postag)
    
    def cut(self, text):
        res = super().cut(text)
        if len(res) > 0 and isinstance(res[0], tuple):
            res = [jieba.posseg.pair(*it) for it in res]
        return res


class CustomTFIDF(JiebaTFIDF):
    """自定义的tfidf类，继承自jieba的TFIDF类，以支持pkuseg的分词工具。单例模式"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CustomTFIDF, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, use_pkuseg=True, idf_path=None):
        super().__init__(idf_path=idf_path)
        if use_pkuseg:
            self.tokenizer = Pkuseg()
            self.postokenizer = Pkuseg(postag=True)