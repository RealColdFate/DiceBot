import csv

from src.informational_commands.feat import *

JSON_FEAT_PATH = '../data/game/feat_data.json'
CSV_FEAT_PATH = '../data/game/feat_data.csv'


def read_feats_dict_from_json():
    with open(JSON_FEAT_PATH, 'r') as f:
        file_text = ''
        for line in f.readlines():
            file_text += line
    return json.loads(file_text)


def compile_feat(feat_dict, feat_name):
    feat = feat_dict[feat_name]
    return Feat(feat[FEAT_NAME_KEY], feat[FEAT_DESCRIPTION_KEY])


def get_feat_names():
    with open(CSV_FEAT_PATH, 'r') as f:
        reader = csv.reader(f)
        names = []
        for row in reader:
            names.append(list(row)[0])
        f.close()
    return names
