import re
from fileLoaders import load_json
from config import Defaults


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
        n_lang["local_format"] = {}

        for key, value in n_lang["locals"].items():
            n_lang["local_format"][key] = "|".join(value)

        # Assigns global and local formats before compiling regex
        cls._lang[lang] = n_lang
        cls._lang[lang]["regex_for"] = cls._make_regex_dict(lang)

        return cls._lang[lang]

    @classmethod
    def _regex_compiler(cls, pattern, lang):
        patterns = []
        global_patterns = cls._lang[lang]["globals"].get(pattern, None)
        local_patterns = cls._lang[lang]["locals"].get(pattern, [])
        local_str_format = cls._lang[lang]["local_format"]

        # Assemble the regex structure
        if global_patterns is not None:
            patterns.append(re.compile(global_patterns, re.IGNORECASE))

        for pattern in local_patterns:
            # Replace the placeholders with the keys present in local_patterns
            new_pattern = pattern.format(**local_str_format)
            patterns.append(re.compile(new_pattern, re.IGNORECASE))

        return patterns

    @classmethod
    def _make_regex_dict(cls, lang):
        local_patterns = cls._lang[lang]["locals"]

        return {
            "week": local_patterns.get("week", []),
            "months": local_patterns.get("months", []),
            "time_structure": local_patterns.get("time_structure", []),
            "today_rel": local_patterns.get("today_rel", []),
            "amount_str": local_patterns.get("amount_str", []),
            "project": cls._regex_compiler("project", lang),
            "important": cls._regex_compiler("important", lang),
            "dificulty": cls._regex_compiler("dificulty", lang),
            "dates": cls._regex_compiler("dates", lang),
        }
