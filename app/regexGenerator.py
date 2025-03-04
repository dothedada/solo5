import re
from fileLoaders import load_json


class RegexFactory:
    def __init__(self, lang):
        self.__global = load_json("./data/config/lang/regex", "globals.json")
        self.__local = load_json("./data/config/lang/regex", f"{lang}.json")
        self.regex_for = self.__get_regex()

    def __regex_compiler(self, pattern_name):
        patterns = []
        global_pattern = self.__global.get(pattern_name, None)
        if global_pattern is not None:
            patterns.append(re.compile(global_pattern, re.IGNORECASE))

        for pattern in self.__local.get(pattern_name, []):
            patterns.append(re.compile(pattern, re.IGNORECASE))

        return patterns

    def __get_regex(self):
        week = "|".join(self.__local.get("week", []))
        months = "|".join(self.__local.get("months", []))
        time_structure = "|".join(self.__local.get("time_structure", []))
        today_relative = "|".join(self.__local.get("today_relative", []))
        dates_formatted = []
        for date_format in self.__local["dates"]:
            date_pattern = date_format.format(
                week=week,
                months=months,
                today_relative=today_relative,
                time_structure=time_structure,
            )
            dates_formatted.append(date_pattern)
        self.__local["dates"] = dates_formatted
        # print(dates_formatted)

        return {
            "week": week,
            "months": months,
            "project": self.__regex_compiler("project"),
            "important": self.__regex_compiler("important"),
            "dificulty": self.__regex_compiler("dificulty"),
            "dates": self.__regex_compiler("dates"),
        }
