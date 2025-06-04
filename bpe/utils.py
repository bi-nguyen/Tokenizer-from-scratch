import unicodedata
SPLIT_PATTERN = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""


def get_stats(ids:list,pair_freq:dict=None):
    '''
    count the frequency of each pair of adjacent tokens.

    args:
        ids: a list of token ids
        pair_freq: a dictionary of pair frequencies, default is {}

    return:
        a dictionary of pair frequencies
    '''
    pair_freq = {} if pair_freq == None else pair_freq
    for pair in zip(ids[:-1],ids[1:]):

        pair_freq[pair] = pair_freq.get(pair,0) + 1

    return pair_freq


def merge_func(ids:list,best_pair:dict,idx:int):
    '''
    merge a best pair into a new token in the given ids.
    
    args:
        ids: a list of token ids
        best_pair: a tuple of two best pair
        idx: a new idx for the best_pair
    
    return:
        a new list of token ids with best_pair replaced by idx
    '''
    i = 0
    new_ids = [] 

    while i<len(ids):
        if i<len(ids)-1 and ids[i] == best_pair[0] and ids[i+1]==best_pair[1]:
            new_ids.append(idx)
            i+=2
        else:
            new_ids.append(ids[i])
            i+=1
    
    return new_ids

def replace_control_characters(s: str) -> str:
    # we don't want to print control characters
    # which distort the output (e.g. \n or much worse)
    # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python/19016117#19016117
    # http://www.unicode.org/reports/tr44/#GC_Values_Table
    chars = []
    for ch in s:
        if unicodedata.category(ch)[0] != "C":
            chars.append(ch) # this character is ok
        else:
            chars.append(f"\\u{ord(ch):04x}") # escape
    return "".join(chars)

def render_token(t: bytes) -> str:
    # pretty print a token, escaping control characters
    s = t.decode('utf-8', errors='replace')
    s = replace_control_characters(s)
    return s