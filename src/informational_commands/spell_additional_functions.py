import csv

from src.informational_commands.spell import *

SPELL_SCHOOL_ICON_MAP = {
    'abjuration': 'https://media-waterdeep.cursecdn.com/attachments/2/707/abjuration.png',
    'conjuration': 'https://media-waterdeep.cursecdn.com/attachments/2/708/conjuration.png',
    'divination': 'https://media-waterdeep.cursecdn.com/attachments/2/709/divination.png',
    'enchantment': 'https://media-waterdeep.cursecdn.com/attachments/2/702/enchantment.png',
    'evocation': 'https://media-waterdeep.cursecdn.com/attachments/2/703/evocation.png',
    'illusion': 'https://media-waterdeep.cursecdn.com/attachments/2/704/illusion.png',
    'necromancy': 'https://media-waterdeep.cursecdn.com/attachments/2/720/necromancy.png',
    'transmutation': 'https://media-waterdeep.cursecdn.com/attachments/2/722/transmutation.png',
}


def get_list_list(data):
    if len(data) == 0:
        return 'None'
    out_str = ''
    for i in data:
        out_str += i + '\n'
    return out_str


def process_spell_name(name_input_list):
    name_input_list = name_input_list.lower().replace("'", '').replace('/', '').replace('(', '').replace(')', '').split(
        ' ')
    if len(name_input_list) == 1:
        return name_input_list[0]
    out_str = ''
    name_input_list = [i.lower() for i in name_input_list]
    for i in range(len(name_input_list)):
        out_str += name_input_list[i]
        if i != len(name_input_list) - 1:
            out_str += '-'
    return out_str


# note that this assumes you are calling from the 'src' dir
JSON_SPELL_DATA_PATH = '../data/game/spell_data.json'


# loads spells from json into dict
def read_spells_from_json():
    with open(JSON_SPELL_DATA_PATH, 'r') as f:
        file_text = ''
        for l in f.readlines():
            file_text += l
    return json.loads(file_text)


# takes a dict of spell info and a spells processed name see process_spell_name() and returns a Spell object
def compile_spell(spell_dict, processed_spell_name):
    spell_dict = spell_dict[processed_spell_name]
    return Spell(spell_dict[SPELL_NAME_KEY], spell_dict[SPELL_SCHOOL_KEY], spell_dict[SPELL_LEVEL_KEY],
                 spell_dict[SPELL_CAST_TIME_KEY], spell_dict[SPELL_RANGE_KEY], spell_dict[SPELL_COMPONENTS_KEY],
                 spell_dict[SPELL_DURATION_KEY], spell_dict[SPELL_DESCRIPTION_KEY],
                 spell_dict[SPELL_UPCAST_DESCRIPTION_KEY], spell_dict[SPELL_REFERENCE_LOCATION_KEY],
                 spell_dict[SPELL_AVAILABLE_CLASSES_KEY])


# note that this assumes you are calling from the 'src' dir
SPELL_DATA_CSV_PATH = '../data/game/spell_data.csv'


# returns a lift of spell names
def get_spell_names():
    spell_names = []
    with open(SPELL_DATA_CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                spell_names.append(row[0].replace('â€™', "'"))
        f.close()
    return spell_names[1::]
