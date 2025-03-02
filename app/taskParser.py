from enum import Enum
import re


class Markers(Enum):
    PROJECT = "@"
    DIFICULTY = "!"
    TASK_SEPARATOR = "//"


class Esp_strings(Enum):
    WEEK = "|".join(
        (
            "lunes",
            "martes",
            "mi[eé]rcoles",
            "jueves",
            "viernes",
            "s[aá]bado",
            "domingo",
        )
    )
    MONTH = "|".join(
        (
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
    )
    DATE_1 = rf"([0-9]{{1,2}})(\/[0-9]{{1,2}}| de ({MONTH}))"
    DATE_2 = rf"(de (hoy|ma[nñ]ana|este ({WEEK})) en |en )([0-9]+ )"
    DATE_3 = r"(dentro de )([0-9]+ )(d[ií]as?|semanas?)"
    DATE_4 = rf"(hoy|ma[nñ]ana)|(el |este |el pr[oó]ximo )({WEEK})"
    DATE_REGX = "|".join([DATE_1, DATE_2, DATE_3, DATE_4])

    @classmethod
    def get_date(cls):
        return re.compile(cls.DATE_REGX.value, re.IGNORECASE)


global_regex = {
    "project": rf"{Markers.PROJECT.value}([a-zA-Z]+)",
    "dificulty": rf"{Markers.DIFICULTY.value}([1-5])",
    "date_esp": Esp_strings.get_date(),
}


string = "care care @nalga : el próximo MARTES me explotaré la cabez"
match = re.search(global_regex["date_esp"], string).group()
match2 = re.search(global_regex["project"], string).group()
print(match, match2)
