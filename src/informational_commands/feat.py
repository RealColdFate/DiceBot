import json

FEAT_NAME_KEY = "FEAT_NAME"
FEAT_DESCRIPTION_KEY = "FEAT_DESCRIPTION"


class Feat:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.clean_attributes()
        self.FEAT_ATTRIBUTE_MAP = {
            FEAT_NAME_KEY: self.name,
            FEAT_DESCRIPTION_KEY: self.description
        }

    def clean_attributes(self):
        delimiter = 'â€¢'
        self.description = self.description.replace(delimiter, '\n\t*').replace('â€™', "'")
        self.name = self.name.replace('â€™', "'").replace('\n', ' ')

    def to_json(self):
        return str(json.dumps(self.FEAT_ATTRIBUTE_MAP, sort_keys=True))
