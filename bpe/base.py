from abc import ABC, abstractmethod
from .utils import render_token

class Tokenizer(ABC):
    def __init__(self,regex_pattern:str=None):
        self.merge = {} # (int, int) -> int
        self.special_token = {} # str -> int, e.g. {'<|endoftext|>': 100257}
        self.regex_pattern = regex_pattern
        self.reverse_special_token = {}
        self.vocab = self.build_vocab() # int -> bytes
    @abstractmethod
    def encode(self,text:str):
        raise NotImplementedError
    
    @abstractmethod
    def decode(self,tokens):
        raise NotImplementedError
    
    @abstractmethod
    def train(self,text:str):
        raise NotImplementedError
    
    def save(self,prefix_name:str):
        '''
        Saves two files: file_prefix.vocab and file_prefix.model
        '''
        model_file = prefix_name + ".model"
        with open(model_file, 'w') as f:
            # write the version, pattern and merges, that's all that's needed
            f.write("minbpe v1\n")
            f.write(f"{self.regex_pattern}\n")
            # write the special tokens, first the number of them, then each one
            f.write(f"{len(self.special_token)}\n")
            for special, idx in self.special_token.items():
                f.write(f"{special} {idx}\n")
            # the merges dict
            for idx1, idx2 in self.merge:
                f.write(f"{idx1} {idx2}\n")
        # write the vocab: for the human to look at
        vocab_file = prefix_name + ".vocab"
        inverted_merges = {idx: pair for pair, idx in self.merge.items()}
        with open(vocab_file, "w", encoding="utf-8") as f:
            for idx, token in self.vocab.items():
                # note: many tokens may be partial utf-8 sequences
                # and cannot be decoded into valid strings. Here we're using
                # errors='replace' to replace them with the replacement char �.
                # this also means that we couldn't possibly use .vocab in load()
                # because decoding in this way is a lossy operation!
                s = render_token(token)
                # find the children of this token, if any
                if idx in inverted_merges:
                    # if this token has children, render it nicely as a merge
                    idx0, idx1 = inverted_merges[idx]
                    s0 = render_token(self.vocab[idx0])
                    s1 = render_token(self.vocab[idx1])
                    f.write(f"[{s0}][{s1}] -> [{s}] {idx}\n")
                else:
                    # otherwise this is leaf token, just print it
                    # (this should just be the first 256 tokens, the bytes)
                    f.write(f"[{s}] {idx}\n")



        model_file = prefix_name + ".model"

        with open(model_file,mode="w") as f:
            f.write(f"{self.regex_pattern}\n")
            special_token_length = len(self.special_token)
            f.write(f"{special_token_length}\n")
            
            for special_token,idx in self.special_token.items():
                f.write(f"{special_token} {idx}\n")

            for token1,token2 in self.merge:
                f.write(f"{token1} {token2}\n")
            
        vocab_file = prefix_name + ".vocab"
        reversed_merge = {idx:pair for pair,idx in self.merge.items()}
        with open(vocab_file,mode="w",encoding="utf-8") as f:
            for idx,token in self.vocab.items():
                s = render_token(token)
                pair_token = reversed_merge.get(idx,None)
                if pair_token:
                    s0 = render_token(self.vocab[pair_token[0]])
                    s1 = render_token(self.vocab[pair_token[1]])
                    f.write(f"[{s0}] [{s1}] -> [{s}] {idx}\n")
                else:
                    f.write(f"[{s}] {idx}\n")

    def load(self,model_file_name:str):
        assert model_file_name.endswith(".model")
        merges = {}
        special_tokens = {}
        idx = 0

        with open(model_file_name,"r",encoding="utf-8") as f:
            self.regex_pattern = f.readline().strip()
            special_tokens_numb = int(f.readline().strip())
            idx = 0 
            for _ in range(special_tokens_numb):
                special_token,special_idx = f.readline().strip().split()
                special_idx = int(special_idx)
                special_tokens[special_token] = special_idx
            
            for line in f:
                token0,token1 = map(int,line.split())
                merges[(token0,token1)]=idx+256
                idx+=1


        self.merge = merges
        self.register_special_token(special_token=special_tokens)
        self.vocab = self.build_vocab()
    
    def build_vocab(self):
        vocab = {idx:bytes([idx]) for idx in range(256)}
        
        for pair,idx in self.merge.items():
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]

        for item,idx in self.special_token.items():
            vocab[idx] = item.encode("utf-8")
            
        return vocab
    
    def register_special_token(self,special_token:dict[str,int]):
        self.special_token = special_token
        self.reverse_special_token = {idx:text for text,idx in special_token.items()}
