import re
from fileLoaders import load_json
from config import Defaults


# Class to make regex dictionarys able to access using dot notation
class RegexDict:
    def __init__(self, dictionary):
        self._dictionary = dictionary

    def __getattribute__(self, key):
        value = self._dictionary[key]
        if isinstance(value, dict):
            return RegexDict(value)
        return value

    def __getitem__(self, key):
        return self.__getattribute__(key)


class GetRegex:
    lang = {}
    cur_lang = ""

    @classmethod
    def of(cls, lang):
        cls.cur_lang = lang

        if lang in cls.lang:
            return cls.lang[lang]

        cls.lang[lang] = {}

        n_lang = {}
        n_lang["globals"] = load_json(Defaults.RGX_PATH.value, "globals.json")
        n_lang["locals"] = load_json(Defaults.RGX_PATH.value, f"{lang}.json")
        n_lang["local_format"] = {}

        for key, value in n_lang["locals"].items():
            n_lang["local_format"][key] = "|".join(value)

        # Assings global and local formats before compiling regex
        cls.lang[lang] = RegexDict(n_lang)
        cls.lang[lang]["regex_for"] = cls._make_regex_dict()

        return cls.lang[lang]

    @classmethod
    def _regex_compiler(cls, pattern):
        patterns = []
        global_patterns = cls.lang[cls.cur_lang]["globals"].get(pattern, None)
        local_patterns = cls.lang[cls.cur_lang]["locals"].get(pattern, [])
        local_str_format = cls.lang[cls.cur_lang]["local_format"]

        # Assemble the regex structure
        if global_patterns is not None:
            patterns.append(re.compile(global_patterns, re.IGNORECASE))

        for pattern in local_patterns:
            # Replace the placeholders with the keys present in __local json
            new_pattern = pattern.format(**local_str_format)
            patterns.append(re.compile(new_pattern, re.IGNORECASE))

        return patterns

    @classmethod
    def _make_regex_dict(cls):
        lcl_patterns = cls.lang[cls.cur_lang]["locals"]

        return {
            "week": lcl_patterns.get("week", []),
            "months": lcl_patterns.get("months", []),
            "time_structure": lcl_patterns.get("time_structure", []),
            "today_rel": lcl_patterns.get("today_rel", []),
            "project": cls._regex_compiler("project"),
            "important": cls._regex_compiler("important"),
            "dificulty": cls._regex_compiler("dificulty"),
            "dates": cls._regex_compiler("dates"),
        }
