import re
from datetime import datetime
import time
import random
from fileLoaders import load_json


class RegexFactory:
    def __init__(self, lang):
        self.globals = load_json("./data/config/lang/regex", "globals.json")
        self.locals = load_json("./data/config/lang/regex", f"{lang}.json")
        self.regex_for = self.__get_regex()

    def __compile_rgx(self, *patterns):
        return re.compile("|".join(patterns), re.IGNORECASE)

    def __get_regex(self):
        self.__date_patterns = []
        patterns = {
            "week": "|".join(self.locals.get("week", [])),
            "months": "|".join(self.locals.get("months", [])),
        }
        for date_format in self.locals["dates"]:
            self.__date_patterns.append(
                date_format.replace("{week}", patterns["week"]).replace(
                    "{months}", patterns["months"]
                )
            )
        return {
            "important": self.__compile_rgx(
                self.globals["important"],
                *self.locals.get("important", ""),
            ),
            "project": self.__compile_rgx(
                self.globals["project"],
                *self.locals.get("project", []),
            ),
            "dificulty": self.__compile_rgx(
                self.globals["dificulty"],
                *self.locals.get("dificulty", []),
            ),
            "date": self.__compile_rgx(*self.__date_patterns),
        }


esp = RegexFactory("es")
test = "el 12 de noviembre martes va a ser muy difícil, @pero es importante"
print(re.search(esp.regex_for["date"], test))
print(re.search(esp.regex_for["important"], test))
print(re.search(esp.regex_for["project"], test))
print(re.search(esp.regex_for["dificulty"], test))


def id_maker(string):
    char_sum = sum(ord(char) for char in string)
    timestamp = int(time.time() * 1000)
    salt = random.randint(1, 9999)
    base_id = (char_sum * timestamp * salt) % (2**64)

    return hex(base_id)[2:]


def parse_task(string, lang):

    parser = RegexFactory(lang)

    important_src = re.search(parser.regex_for["important"], string)
    important = important_src is not None
    # "dificulty",
    # "due_date",
    # "dependencies",

    project_src = re.search(parser.regex_for["project"], string)
    project = project_src.group()[1:] if project_src else None
    # "project",

    return {
        "id": id_maker(string),
        "task": string,
        "creation_date": datetime.now().date(),
        "lang": lang,
        "important": important,
        "project": project,
    }


print(parse_task(test, "es"))
