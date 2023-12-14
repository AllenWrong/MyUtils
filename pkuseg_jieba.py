from jieba.analyse.tfidf import TFIDF as JiebaTFIDF
import pkuseg
import jieba


class Pkuseg(pkuseg.pkuseg):
    """Customed pkuseg class. Custom the output of this class to be
    same as the jieba.cut interface.
    """
    def __init__(self, model_name="default", user_dict="default", postag=False):
        super().__init__(model_name, user_dict, postag)
    
    def cut(self, text):
        """Custom the output of this method to be same as the jieba.cut method."""
        res = super().cut(text)
        if len(res) > 0 and isinstance(res[0], tuple):
            res = [jieba.posseg.pair(*it) for it in res]
        return res


class CustomTFIDF(JiebaTFIDF):
    """Customed TFIDF class. Inherited from jieba.analyse.tfidf.TFIDF.
    This class can support the pukseg word cutting api. This class is
    implemented with single instance mode.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CustomTFIDF, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, use_pkuseg=True, idf_path=None):
        """Custom this class to suppoer the pkuseg word cutting api."""
        super().__init__(idf_path=idf_path)
        if use_pkuseg:
            self.tokenizer = Pkuseg()
            self.postokenizer = Pkuseg(postag=True)