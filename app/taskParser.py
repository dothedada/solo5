import re
from fileLoaders import load_json


class RegexFactory:
    def __init__(self, lang):
        self.globals = load_json("./data/lang/regex", "globals.json")
        self.locals = load_json("./data/lang/regex", f"{lang}.json")
        self.date_patterns = []
        patterns = {
            "week": "|".join(self.locals.get("week", [])),
            "months": "|".join(self.locals.get("months", [])),
        }
        for date_format in self.locals["dates"]:
            self.date_patterns.append(
                date_format.replace("{week}", patterns["week"]).replace(
                    "{months}", patterns["months"]
                )
            )

    def compile_rgx(self, *patterns):
        return re.compile("|".join(patterns), re.IGNORECASE)

    def get_regex(self):
        return {
            "important": self.compile_rgx(
                self.globals["important"], self.locals.get("important", "")
            ),
            "project": self.compile_rgx(self.globals["project"]),
            "dificulty": self.compile_rgx(
                self.globals["dificulty"], *self.locals.get("dificulty", [])
            ),
            "date": self.compile_rgx(*self.date_patterns),
        }


esp = RegexFactory("es")
test = "el 12 de noviembre martes va a ser muy difícil, @pero es importante"
print(re.search(esp.get_regex()["date"], test))
print(re.search(esp.get_regex()["important"], test))
print(re.search(esp.get_regex()["project"], test))
print(re.search(esp.get_regex()["dificulty"], test))
