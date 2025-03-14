import re
from fileManagers import load_json
from config import Defaults


class UIRegex:
    _lang = {}

    @classmethod
    def of(cls, lang):
        if lang in cls._lang:
            return cls._lang[lang]

        file = load_json(Defaults.UI_PATH.value, f"{lang}.json")
        cls._lang[lang] = {}
        cls._lang[lang]["confirmation"] = UIRegex._compile_regex(file["confirmation"])
        cls._lang[lang]["exit"] = UIRegex._compile_regex(file["exit"])

        return cls._lang[lang]

    @staticmethod
    def _compile_regex(regex_list):
        if type(regex_list) is str:
            return re.compile(regex_list, re.IGNORECASE)

        compiled_regex = []
        for regex in regex_list:
            compiled_regex.append(re.compile(regex, re.IGNORECASE))
        return compiled_regex


class GetRegex:
    _lang = {}

    @classmethod
    def of(cls, lang):
        if lang in cls._lang:
            return cls._lang[lang]

        cls._lang[lang] = {}

        n_lang = {}
        n_lang["globals"] = load_json(Defaults.RGX_PATH.value, "globals.json")
        n_lang["locals"] = load_json(Defaults.RGX_PATH.value, f"{lang}.json")
        n_lang["definitions"] = n_lang["locals"]["definitions"]

        # Assigns global and local formats before compiling regex
        cls._lang[lang] = n_lang
        cls._lang[lang]["regex_for"] = cls._regex_compiler(lang)

        return cls._lang[lang]

    @classmethod
    def _regex_compiler(cls, lang):
        patterns = {}
        local_str = {}

        for key, value in cls._lang[lang]["definitions"].items():
            local_str[key] = "|".join(value)

        global_patterns = cls._lang[lang]["globals"]
        local_patterns = cls._lang[lang]["locals"]

        pattern_keys = set([*global_patterns.keys(), *local_patterns.keys()])
        pattern_keys.remove("definitions")

        for pattern in pattern_keys:
            patterns[pattern] = []
            if pattern in global_patterns:
                patterns[pattern].append(
                    re.compile(global_patterns[pattern], re.IGNORECASE)
                )

            if pattern in local_patterns:
                for sub_pattern in local_patterns[pattern]:
                    formated_pattern = sub_pattern.format(**local_str)
                    patterns[pattern].append(
                        re.compile(formated_pattern, re.IGNORECASE)
                    )

        return {**patterns, **cls._lang[lang]["definitions"]}
