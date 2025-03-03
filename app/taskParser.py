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


def id_maker(string):
    char_sum = sum(ord(char) for char in string)
    timestamp = int(time.time() * 1000)
    salt = random.randint(1, 9999)
    base_id = (char_sum * timestamp * salt) % (2**64)

    return hex(base_id)[2:]


def parse_task(string, lang):

    # NOTE: ver como vinculamos la regex factory
    parser = RegexFactory(lang)

    important_src = re.search(parser.regex_for["important"], string)
    important = important_src is not None

    dificulty_src = re.search(parser.regex_for["dificulty"], string)
    dificulty = 3
    # NOTE: evitar trabajar dificulty con try catch
    # pensar en volver a hacer un bucle con los regex de dificultad y el que le
    # atine es el  indice

    if dificulty_src:
        try:
            dificulty = int(dificulty_src.group()[1:])
        except Exception:
            dificulty = parser.locals["dificulty"].index("muy dif[ií]cil") + 1

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
        "dificulty": dificulty,
    }


test = "el 12 de noviembre martes va a ser muy difícil, @pero es importante"
print(parse_task(test, "es"))
