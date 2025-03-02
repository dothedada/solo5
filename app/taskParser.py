import re


class Global_str:
    _TASK_SEPARATOR = "//"
    _IMPORTANT = "\\*"
    _PROJECT = "@([a-zA-Z]+)"
    _DIFICULTY = "!([1-5])"

    @classmethod
    def make_rgx(cls, *args):
        return re.compile("|".join(args), re.IGNORECASE)


class Esp_str(Global_str):
    __IMPORTANT_ALT = "importante"
    __DIFICULTY_LEVELS = ("(muy )?f[aá]cil", "normal", "(muy )?dif[ií]cil")
    __DAYS = (
        "lunes",
        "martes",
        "mi[eé]rcoles",
        "jueves",
        "viernes",
        "s[aá]bado",
        "domingo",
    )
    __MONTH_LIST = (
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
    )
    __MONTH = "|".join(__MONTH_LIST)
    __WEEK = "|".join(__DAYS)
    __DIFICULTY_ALT = "|".join(__DIFICULTY_LEVELS)
    __DATE_1 = rf"([0-9]{{1,2}})(\/[0-9]{{1,2}}| de ({__MONTH}))"
    __DATE_2 = rf"(de (hoy|ma[nñ]ana|este ({__WEEK})) en |en )([0-9]+ )"
    __DATE_3 = r"(dentro de )([0-9]+ )(d[ií]as?|semanas?)"
    __DATE_4 = rf"(hoy|ma[nñ]ana)|(el |este |pr[oó]ximo )({__WEEK})"

    @classmethod
    def importance_rgx(cls):
        return super().make_rgx(cls._IMPORTANT, cls.__IMPORTANT_ALT)

    @classmethod
    def dificulty_rgx(cls):
        return super().make_rgx(cls._DIFICULTY, cls.__DIFICULTY_ALT)

    @classmethod
    def project_rgx(cls):
        return super().make_rgx(cls._PROJECT)

    @classmethod
    def date_rgx(cls):
        return super().make_rgx(
            cls.__DATE_1,
            cls.__DATE_2,
            cls.__DATE_3,
            cls.__DATE_4,
        )
