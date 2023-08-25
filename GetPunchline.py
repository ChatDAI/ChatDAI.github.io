import torch
from utils import StrDataset, idx2tag
import difflib

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load('duanzai_punchline_ner_model.pth', map_location=device)
model.eval()

def longest_common_substring(str1, str2):
    seq = difflib.SequenceMatcher(None, str1, str2)
    match = seq.find_longest_match(0, len(str1), 0, len(str2))
    if match.size == 0:
        return ""
    return str1[match.a:match.a + match.size]

def getPunchline(text):
    dataset = StrDataset(text)
    Y_hat = []
    tokens, mask = dataset.token_tensors, dataset.mask
    tokens = tokens.to(device)
    mask = mask.to(device)
    y_hat = model(sentence=tokens, mask=mask, is_test=True)
    for j in y_hat:
        Y_hat.extend(j)
    y_pred = [idx2tag[i] for i in Y_hat]
    word = ''
    for i in range(len(y_pred)):
        if y_pred[i] == 'O':
            word += y_pred[i]
        elif y_pred[i] == 'PUNCHLINE':
            word += text[i-1]
    return longest_common_substring(text, word)