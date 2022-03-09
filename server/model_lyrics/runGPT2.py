from flask import jsonify
from random import choice
from simpletransformers.language_generation import LanguageGenerationModel, LanguageGenerationArgs
import os

file_prefix = os.path.dirname(__file__)

def run(input, output_len, weight_path = 'gpt2-model'):

    Language_gen_args = LanguageGenerationArgs()
    Language_gen_args.max_length = output_len

    print(os.path.join(file_prefix, weight_path))
    model = LanguageGenerationModel("gpt2", os.path.join(file_prefix, weight_path),
                                    Language_gen_args, use_cuda=False)
    output = model.generate(input)

    return output[0]

def gen_gpt2(seed="", output_len = 100):
    seed_options = ["Papi", "Dime que tu me quieres", "Bailando", "La vida loca", "Te quiero en mi cama", "Sin ti", "Enamorado", "Yo te esperar", "One, two, three", "Una en un millón", "Que tengo que hacer", "Inolvidable", "Por primera vez", "Tan importante"]
    
    if len(seed) < 1:
        seed = choice(seed_options)

    a = run(input = seed, output_len = output_len)
    a = a.replace('\"\"\"', '\n')
    a = a.replace('\"\"', '\n')

    return jsonify(
        lyrics=a,
        title=seed
    )