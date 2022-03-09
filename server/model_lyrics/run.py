import tensorflow as tf
import numpy as np
from .helper import *
import random

file_prefix = os.path.dirname(__file__)
_, vocab_to_int, int_to_vocab, token_dict = load_preprocess()
seq_length, load_dir = load_params()

def get_tensors(loaded_graph):
    """
    Get input, initial state, final state, and probabilities tensor from <loaded_graph>
    :param loaded_graph: TensorFlow graph loaded from file
    :return: Tuple (InputTensor, InitialStateTensor, FinalStateTensor, ProbsTensor)
    """
    # TODO: Implement Function

    inputTensor = loaded_graph.get_tensor_by_name('input:0')
    initialStateTensor = loaded_graph.get_tensor_by_name('initial_state:0')
    finalStateTensor = loaded_graph.get_tensor_by_name('final_state:0')
    probsTensor = loaded_graph.get_tensor_by_name('probs:0')
    return inputTensor, initialStateTensor, finalStateTensor, probsTensor

def pick_word(probabilities, int_to_vocab):
    """
    Pick the next word in the generated text
    :param probabilities: Probabilites of the next word
    :param int_to_vocab: Dictionary of word ids as the keys and words as the values
    :return: String of the predicted word
    """
    # TODO: Implement Function
    a = np.array(list(int_to_vocab.values()))
    word = np.random.choice(a, p=probabilities)

    return word


def run(seed_word):
    gen_length = 250

    if(len(seed_word) < 1):
        n = random. randint(2,len(vocab_to_int.keys()))
        possible_in = list(vocab_to_int.keys())
        prime_word = possible_in[n]
    else:
        prime_word = seed_word

    loaded_graph = tf.Graph()
    with tf.compat.v1.Session(graph=loaded_graph) as sess:
        loader = tf.compat.v1.train.import_meta_graph(os.path.join(file_prefix, load_dir[2:] + '.meta'))
        loader.restore(sess, os.path.join(file_prefix, load_dir[2:]))

        # Get Tensors from loaded model
        input_text, initial_state, final_state, probs = get_tensors(loaded_graph)

        # Sentences generation setup
        gen_sentences = [prime_word]
        print(gen_sentences)
        prev_state = sess.run(initial_state, {input_text: np.array([[1]])})
        # Generate sentences
        for n in range(gen_length):
            # Dynamic Input

            dyn_input = [[vocab_to_int[word] for word in gen_sentences[-seq_length:]]]
            dyn_seq_length = len(dyn_input[0])
            # Get Prediction
            probabilities, prev_state = sess.run(
                [probs, final_state],
                {input_text: dyn_input, initial_state: prev_state})

            pred_word = pick_word(probabilities[0][dyn_seq_length-1], int_to_vocab)

            gen_sentences.append(pred_word)

        # Remove tokens
        lyrics = ' '.join(gen_sentences)
        for key, token in token_dict.items():
            ending = ' ' if key in ['\n', '(', '"'] else ''
            lyrics = lyrics.replace(' ' + token.lower(), key)
        lyrics = lyrics.replace('\n ', '\n')
        lyrics = lyrics.replace('( ', '(')

    return lyrics
