import re


ui_patterns = {
    "global": {
        "ui": {
            "hi": "carajo",
        },
        "pattern": {
            "task_separator": "//",
            "important": "\\*",
            "project": "@([a-zA-Z]+)",
            "dificulty": "!([1-5])",
        },
    },
    "es": {
        "ui": {
            "hi": "hola",
        },
        "pattern": {
            "important": "importante",
            "dificulty": [
                "muy f[aá]cil",
                "f[aá]cil",
                "normal",
                "dif[ií]cil",
                "muy dif[ií]cil",
            ],
            "week": [
                "lunes",
                "martes",
                "mi[eé]rcoles",
                "jueves",
                "viernes",
                "s[aá]bado",
                "domingo",
            ],
            "months": [
                "enero",
                "febrero",
                "marzo",
                "abril",
                "mayo",
                "junio",
                "julio",
                "agosto",
                "septiembre",
                "octubre",
                "noviembre",
                "diciembre",
            ],
            "dates": [
                r"([0-9]{{1,2}})(\/[0-9]{{1,2}}| de ({months}))",
                r"(de (hoy|ma[nñ]ana|este ({week})) en |en )([0-9]+ )",
                r"(dentro de )([0-9]+ )(d[ií]as?|semanas?)",
                r"(hoy|ma[nñ]ana)|(el |este |pr[oó]ximo )({week})",
            ],
        },
    },
}


class RegexFactory:
    def __init__(self, data, lang="es"):
        self.globals = data["global"]["pattern"]
        self.locals = data[lang]["pattern"]
        self.locals["week"] = "|".join(self.locals["week"])
        self.locals["months"] = "|".join(self.locals["months"])

    def get_patterns(self):
        patterns = {}
        patterns["date"] = "|".join(
            pattern.format(**self.locals) for pattern in self.locals["dates"]
        )
        patterns["important"] = "|".join(
            (self.globals["important"], self.locals["important"])
        )
        patterns["dificulty"] = "|".join(
            (self.globals["dificulty"], *self.locals["dificulty"])
        )
        print(patterns)

    def compile_rgx(cls, *patterns):
        return re.compile("|".join(patterns), re.IGNORECASE)


esp = RegexFactory(ui_patterns)
esp.get_patterns()

# print(esp.globals)


# class Global_str:
#     _TASK_SEPARATOR = "//"
#     _IMPORTANT = "\\*"
#     _PROJECT = "@([a-zA-Z]+)"
#     _DIFICULTY = "!([1-5])"
#
#     @classmethod
#     def make_rgx(cls, *args):
#         return re.compile("|".join(args), re.IGNORECASE)
#
#
# class Esp_str(Global_str):
#     __IMPORTANT_ALT = "importante"
#     __DIFICULTY_LEVELS = ("(muy )?f[aá]cil", "normal", "(muy )?dif[ií]cil")
#     __DAYS = (
#         "lunes",
#         "martes",
#         "mi[eé]rcoles",
#         "jueves",
#         "viernes",
#         "s[aá]bado",
#         "domingo",
#     )
#     __MONTH_LIST = (
#         "enero",
#         "febrero",
#         "marzo",
#         "abril",
#         "mayo",
#         "junio",
#         "julio",
#         "agosto",
#         "septiembre",
#         "octubre",
#         "noviembre",
#         "diciembre",
#     )
#     __MONTH = "|".join(__MONTH_LIST)
#     __WEEK = "|".join(__DAYS)
#     __DIFICULTY_ALT = "|".join(__DIFICULTY_LEVELS)
#     __DATE_1 = rf"([0-9]{{1,2}})(\/[0-9]{{1,2}}| de ({__MONTH}))"
#     __DATE_2 = rf"(de (hoy|ma[nñ]ana|este ({__WEEK})) en |en )([0-9]+ )"
#     __DATE_3 = r"(dentro de )([0-9]+ )(d[ií]as?|semanas?)"
#     __DATE_4 = rf"(hoy|ma[nñ]ana)|(el |este |pr[oó]ximo )({__WEEK})"
#
#     @classmethod
#     def importance_rgx(cls):
#         return super().make_rgx(cls._IMPORTANT, cls.__IMPORTANT_ALT)
#
#     @classmethod
#     def dificulty_rgx(cls):
#         return super().make_rgx(cls._DIFICULTY, cls.__DIFICULTY_ALT)
#
#     @classmethod
#     def project_rgx(cls):
#         return super().make_rgx(cls._PROJECT)
#
#     @classmethod
#     def date_rgx(cls):
#         return super().make_rgx(
#             cls.__DATE_1,
#             cls.__DATE_2,
#             cls.__DATE_3,
#             cls.__DATE_4,
#         )
