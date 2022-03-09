import os
import requests
from time import sleep

def download_from_drive(file_id, target, first=False):
    # Get directory
    script_dir = os.path.dirname(__file__)
    
    mode = "ab"
    if first:
        if os.path.isfile(os.path.join(script_dir, target)):
            return
        mode = "wb"

    sleep(5)
    origin = "https://www.googleapis.com/drive/v3/files/" + file_id + "?alt=media&key=AIzaSyA7Vj0O3qcwKHh_K-88eAimMrNhg9Kmb3E"
    response = requests.get(origin)

    open(os.path.join(script_dir, target), mode).write(response.content)

''' checkpoint 2
gpt2_keys = [
    "1P4cLqcHHGiXix1rwtY_aU5r_R0MMJ_Tc",
    "1L8UcVKLcYYzx3aSycaIPL7eMMglMxzu2",
    "1P6hsoPrw3sHYbuGBjhg2XkoLeBSvfw-y",
    "1g6VpJR25xpxY_uyQcxUdDen8EABmm-hd",
    "1Oket4DZ8DKbeY70GWDDWxVs-yBle5k9m",
    "1aVspPQwMbooekXxV9zskoCZWEuooQpJx",
    "19iJ7qE7L9BUF_TUtq-ue6PkaUN4gH2FI",
    "1f456_B6ZYRGO6qcemfeb-mN1jSSckBOo",
    "1Ql78p3qu0aQOGNFFwwDd4KPjHLtsI4p1",
    "1TJjhDH49p3paR3GE7Ag_QcpRbB7Odffe",
]
'''
''' checkpoint 5 
gpt2_keys = [
    "1cLhKqP9xUp_MO0A6pZB1Ia_1U1Fl4Orw",
    "1LAD-OptlaX81U1PQlqiRk0FjrNgbzs95",
    "10H4QvyxJXzq-Fe0yVoYEZDEivWSNOueE",
    "1NzIPoMdns8yMTiXcKwVXs_T0j5_EmYo3",
    "1ZxkwimcIKVEsEumXqrt4k6bs5CIv0UTt",
    "19ikL7rtFXoxR8DfDx12SWGqNyeUNSF_D",
    "1uMDrj48r4AM7Vn75wIMqD7E_1KWTGKM6",
    "1ewiYg-VNBebsQgA4pZk-rhYFAVtZWLrX",
    "1QLcgUdTr9mmPBjxOifiyUWSI6Blt0Fyi",
    "1pRkKBVglfKlWWALgezc7wmBdsleoMiTK",
]
'''
''' attempt with linebreaks 1'''
gpt2_keys = [
    "1FkEMmbLhOcxyNLwE_B3WW6FCVF4-R4F0",
    "1zhUCiVqVzpUseMtn1zScvSt7T40DX5at",
    "18xaBVYPaQWYGlc_wTChzlEIZE2PTWVuV",
    "1EyM9Q0EW8ReeSN2cX6EAh7OQOhip3TY1",
    "1C2kd54k8Sat0QxieFdsKthBydQTIIEnb",
    "1Lgwo7L-IBPmiRvftZMtMfKb2kEPXTBZO",
    "1bY_8P3eob-0TW5qrNRtu-ZxT16o8ajNh",
    "1wbpYofMf_MtarBvohRy4eeJaOBhMJsIc",
    "1qBl78LICtEdN0hbB2XuN3bd78Yxl16bU",
    "1RL2IBUVrN0k5xLm3PVE225kbbWcRb-hK",
]
gpt2_names = [
    "config.json",
    "merges.txt",
    "model_args.json",
    "optimizer.pt",
    "pytorch_model.bin",
    "scheduler.pt",
    "special_tokens_map.json",
    "tokenizer_config.json",
    "training_args.bin",
    "vocab.json"
]
lyric_model_key = "1Nx5kEC_KAYM1MSDBimr66NmIj_K_OCl5"
