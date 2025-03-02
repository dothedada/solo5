import re
from fileLoaders import load_json


class RegexFactory:
    def __init__(self, lang):
        self.__globals = load_json("./data/config/lang/regex", "globals.json")
        self.__locals = load_json("./data/config/lang/regex", f"{lang}.json")
        self.regex_for = self.__get_regex()

    def __compile_rgx(self, *patterns):
        return re.compile("|".join(patterns), re.IGNORECASE)

    def __get_regex(self):
        self.__date_patterns = []
        patterns = {
            "week": "|".join(self.__locals.get("week", [])),
            "months": "|".join(self.__locals.get("months", [])),
        }
        for date_format in self.__locals["dates"]:
            self.__date_patterns.append(
                date_format.replace("{week}", patterns["week"]).replace(
                    "{months}", patterns["months"]
                )
            )
        return {
            "important": self.__compile_rgx(
                self.__globals["important"],
                *self.__locals.get("important", ""),
            ),
            "project": self.__compile_rgx(
                self.__globals["project"],
                *self.__locals.get("project", []),
            ),
            "dificulty": self.__compile_rgx(
                self.__globals["dificulty"],
                *self.__locals.get("dificulty", []),
            ),
            "date": self.__compile_rgx(*self.__date_patterns),
        }


esp = RegexFactory("es")
test = "el 12 de noviembre martes va a ser muy difícil, @pero es importante"
print(re.search(esp.regex_for["date"], test))
print(re.search(esp.regex_for["important"], test))
print(re.search(esp.regex_for["project"], test))
print(re.search(esp.regex_for["dificulty"], test))
