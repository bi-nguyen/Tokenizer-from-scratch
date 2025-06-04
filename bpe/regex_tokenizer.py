from .base import Tokenizer
from .utils import merge_func,get_stats
import regex as re

class RegexTokenizer(Tokenizer):
    def __init__(self,regex_pattern:str=None):
        super().__init__()
        self.regex_pattern = regex_pattern
        
    def train(self,text:str,vocab_size:int):

        assert vocab_size>256, "The vocab size must be larger than 256"
        chunks = re.findall(self.regex_pattern,text)
        encoded_chunks = [list(map(int,chunk.encode("utf-8"))) for chunk in chunks]
        for i in range(vocab_size-256):
            pairs = {}
            for encoded_chunk in encoded_chunks:
                pairs = get_stats(encoded_chunk,pairs)
            if not pairs:
                break
            best_pairs = max(pairs,key=pairs.get)
            idx = 256+i
            encoded_chunks = [merge_func(encoded_chunk,best_pairs,idx) for encoded_chunk in encoded_chunks]
            self.merge[best_pairs] = idx
            self.vocab[idx] = self.vocab[best_pairs[0]] + self.vocab[best_pairs[1]]


    def encode_text(self,text:str):
        
        chunks = re.findall(re.compile(self.regex_pattern),text)

        encoded_text= []
        for chunk in chunks:
            encoded_text.extend(self.encode_chunk(chunk))

        return encoded_text


    def encode_chunk(self,text:str)->list[int]:

        encoded_text = list(map(int,text.encode("utf-8")))

        if len(encoded_text)<2:
            return encoded_text
        
        while True:

            pairs = get_stats(encoded_text)
            if not pairs:
                break
            min_pair  = min(pairs,key=lambda x: self.merge.get(x,float("inf")))

            idx = self.merge.get(min_pair,None)
            if idx :
                encoded_text = merge_func(encoded_text,min_pair,idx)
            else:
                break


        return encoded_text


    def decode(self, ids:list[int]):
        decoded_text = b"".join([self.reverse_special_token[idx].encode("utf-8") if self.reverse_special_token.get(idx,None) else self.vocab[idx]  for idx in ids])
        return decoded_text.decode("utf-8",errors="replace")

    def encode(self,text:str):

        encoded_text = []

        if self.special_token:
            special_token_pattern = "("+ "|".join([re.escape(special) for special in self.special_token.keys()])+")"
            text = re.split(re.compile(special_token_pattern),text)
        else:
            text = [text]
            
        for t in text:
            if self.special_token.get(t,None):
                encoded_text.append(self.special_token[t])
            else:
                encoded_text.extend(self.encode_text(t))

        return encoded_text
    

def main():
    regex_bpe = RegexTokenizer()
    special_token = {
        "<|endoftext|>":100257,
        "<|endofprompt|>": 100276
    }
    text = "xin chào mọi người <|endofprompt|> Tôi tên là hahaa <|endoftext|> "
    regex_bpe.register_special_token(special_token=special_token)



    return




if __name__ =="__main__":
    
    main()