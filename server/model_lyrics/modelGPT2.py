from simpletransformers.language_modeling import LanguageModelingModel,LanguageModelingArgs
import os
import random
import pandas as pd

file_prefix = os.path.dirname(__file__)

def modelGPT2(path = '../data/letrasFinal_clean.txt'):
    model_args = LanguageModelingArgs()
    model_args.reprocess_input_data = True
    model_args.overwrite_output_dir = True
    model_args.num_train_epochs = 5
    model_args.best_model_dir = "outputs/best_model"
    model_args.save_best_model =True
    model_args.train_batch_size = 2
    # model_args.block_size = 48
    model_args.dataset_type = "simple"
    model_args.mlm = False  # mlm must be False for CLM
    model_args.vocab_size = 50257

    input_file = os.path.join(path)
    corpus = []
    with open(input_file, "r") as f:
        #data = f.read()
        lines = f.readlines()
        for line in lines:
           if random.random() < 0.02:
                corpus.append(line)
    
    #corpus = data.lower().split('\n\n')
    #print(len(corpus)) 5605
    # 271618

    print(len(corpus))

    # /200 = 2716

    df = pd.DataFrame(corpus, columns = ['text'])

    df['text'][:-5].to_csv('../data/train.txt', index=False, header=False)
    df['text'][-5:].to_csv('../data/test.txt', index=False, header=False)

    train_file = os.path.join(file_prefix, '../data/train.txt')
    test_file = os.path.join(file_prefix, '../data/test.txt')

    #Language Model Loading it can either GPT2, BERT, ELECTRA etc.
    model = LanguageModelingModel(
        "gpt2", "datificate/gpt2-small-spanish", args=model_args, train_files=train_file
    )

    model.train_model(train_file, eval_file=test_file)
    

if __name__ == '__main__':
    modelGPT2()



