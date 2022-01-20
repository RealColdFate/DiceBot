import json

SPELL_NAME_KEY = "SPELL_NAME"
SPELL_SCHOOL_KEY = "SPELL_SCHOOL"
SPELL_LEVEL_KEY = "SPELL_LEVEL"
SPELL_CAST_TIME_KEY = "SPELL_CAST_TIME"
SPELL_RANGE_KEY = "SPELL_RANGE"
SPELL_COMPONENTS_KEY = "SPELL_COMPONENTS"
SPELL_DURATION_KEY = "SPELL_DURATION"
SPELL_DESCRIPTION_KEY = "SPELL_DESCRIPTION"
SPELL_UPCAST_DESCRIPTION_KEY = "SPELL_UPCAST_DESCRIPTION"
SPELL_REFERENCE_LOCATION_KEY = "SPELL_REFERENCE_LOCATION"
SPELL_AVAILABLE_CLASSES_KEY = "SPELL_AVAILABLE_CLASSES"


class Spell:

    def __init__(self, name: str, school: str, level: str, cast_time: str, spell_range: str, components: str,
                 duration: str, description: str, upcast_description: str, ref_location: str, classes: list):
        self.name = name
        self.school = school
        self.level = level
        self.cast_time = cast_time
        self.spell_range = spell_range
        self.components = components
        self.duration = duration
        self.description = description
        self.upcast_description = upcast_description
        self.ref_location = ref_location
        self.classes = classes

        self.clean_attributes()

        self.SPELL_ATTRIBUTE_MAP = {
            SPELL_NAME_KEY: self.name,
            SPELL_SCHOOL_KEY: self.school,
            SPELL_LEVEL_KEY: self.level,
            SPELL_CAST_TIME_KEY: self.cast_time,
            SPELL_RANGE_KEY: self.spell_range,
            SPELL_COMPONENTS_KEY: self.components,
            SPELL_DURATION_KEY: self.duration,
            SPELL_DESCRIPTION_KEY: self.description,
            SPELL_UPCAST_DESCRIPTION_KEY: self.upcast_description,
            SPELL_REFERENCE_LOCATION_KEY: self.ref_location,
            SPELL_AVAILABLE_CLASSES_KEY: self.classes
        }

    def clean_attributes(self):
        self.cast_time = self.cast_time.replace(' Casting time: ', '')
        self.duration = self.duration.replace(' Duration: ', '')
        self.components = self.components.replace(' Components: ', '')
        self.level = self.level.replace(' Level: ', '')
        self.spell_range = self.spell_range.replace(' Range: ', '')

    def get_info_string(self):
        return f'Level: {self.level}\nCasting time: {self.cast_time}\nRange: {self.spell_range}\n' \
               f'Components: {self.components}\nDuration: {self.duration}\n '

    def to_json(self):
        return str(json.dumps(self.SPELL_ATTRIBUTE_MAP, sort_keys=True))
