from .utils import get_stats,merge_func
from .base import Tokenizer


class NaiveTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
    def train(self,text:str,vocab_size=256):

        assert vocab_size>256, "Vocab size must be larger than 256"

        encoded_text = list(map(int,text.encode("utf-8")))

        for i in range(vocab_size-256):
            pairs = get_stats(encoded_text)
            best_pair = max(pairs,key = pairs.get)
            idx = 256+i
            encoded_text = merge_func(encoded_text,best_pair,idx)
            self.merge[(best_pair)] =idx
            self.vocab[idx] = self.vocab[best_pair[0]] + self.vocab[best_pair[1]] 

        print("The training process is done !!!")

    def encode(self,text:str):
        encoded_text = list(map(int,text.encode("utf-8")))
        while True:
            pairs = get_stats(text)
            min_pair = min(pairs,key= lambda x: self.merge.get(x,float("inf")))
            if self.merge.get(min_pair,None):
                idx = self.merge[min_pair]
                encoded_text = merge_func(encoded_text,min_pair,idx)
            else:
                break
        return encoded_text

    def decode(self,ids:list[int]):
        dedcoded_text = b"".join([self.vocab[idx] for idx in ids])
        return dedcoded_text.decode("utf-8",errors="replace")

def main():
    return


if __name__ == "__main__":
    main()