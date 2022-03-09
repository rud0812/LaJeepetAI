import helper

data_dir = '../data/letrasFinal.txt'
text = helper.load_data(data_dir)
# Ignore notice, since we don't use it for analysing the data
text = text[81:]

import numpy as np

# Import Counter
from collections import Counter

def create_lookup_tables(text):
    """
    Create lookup tables for vocabulary
    :param text: The text of tv scripts split into words
    :return: A tuple of dicts (vocab_to_int, int_to_vocab)
    """
    # TODO: Implement Function
    counts = Counter(text)

    vocab = sorted(counts, key=counts.get, reverse=True)
#     print(counts.most_common())
    vocab_to_int = {word: i for i, word in enumerate(vocab)}
    int_to_vocab = {i: word for i, word in enumerate(vocab)}

    return vocab_to_int, int_to_vocab

def token_lookup():
    """
    Generate a dict to turn punctuation into a token.
    :return: Tokenize dictionary where the key is the punctuation and the value is the token
    """
    # TODO: Implement Function
    tokenize_puntiation = {
                            '.' : '||Period||',
                            ',': '||Comma||',
                            '"': '||QuotationMark||',
                            ';': '||Semicolon||',
                            '!': '||ExclamationMark||',
                            '?': '||QuestionMark||',
                            '(': '||LeftParentheses||',
                            ')': '||Parentheses||',
                            '--': '||Dash||',
                            '\n' : '||Return||'}
    
    return tokenize_puntiation

helper.preprocess_and_save_data(data_dir, token_lookup, create_lookup_tables)