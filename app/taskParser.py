from enum import Enum
import re


class Markers(Enum):
    PROJECT = "@"
    DIFICULTY = "!"
    TASK_SEPARATOR = "//"


class Esp(Enum):
    WEEK = "lunes|martes|miercoles|jueves|viernes|sabado|domingo"
    MONTH = "|".join(
        [
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
        ]
    )
    DATE_1 = rf"([0-9]{{1,2}})(\/[0-9]{{1,2}}| de ({MONTH}))"
    DATE_2 = rf"(de (hoy|ma[nñ]ana|este ({WEEK})) en |en )([0-9]+ )"
    DATE_3 = r"(dentro de )([0-9]+ )(dia(?:s)?|semana(?:s)?)"
    DATE_4 = rf"(hoy|ma[nñ]ana)|(el |este |el pr[oó]ximo )({WEEK})"
    DATE_REGX = "|".join([DATE_1, DATE_2, DATE_3, DATE_4])


global_regex = {
    "project": rf"{Markers.PROJECT.value}([a-zA-Z]+)",
    "dificulty": rf"{Markers.DIFICULTY.value}([1-5])",
    "date_esp": rf"{Esp.DATE_REGX.value}",
}


string = "el próximo martes me explotaré la cabez"
match = re.match(global_regex["date_esp"], string)
print(match)
