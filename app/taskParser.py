import re

global_markers = {
    "project": "@",
    "dificulty": "!",
    "task_separator": "//",
}

global_regex = {
    "project": rf"{global_markers.project}(\w+)",
    "dificulty": rf"{global_markers.dificulty}([1-5])",
}

lang_strings = {
    "esp": {
        "week": [
            "lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes",
            "sabado",
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
    }
}

esp_regex = {
    "due_date": rf"(pasado )?(hoy|ma.ana)|(el |este |el proximo )({lang_strings.esp.week.join('|')})|(dentro de |de (hoy|ma.ana|este (lunes|martes|miercoles|jueves|viernes|sabado|domingo)) en |en )([0-9]+ )(dia.|semana.)|([0-9]{1,2})(\/[0-9]{1,2}| de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre))",
}

eng_regex = {
    "due_date": r"(pasado )?(hoy|ma.ana)|(el |este |el proximo )(lunes|martes|miercoles|jueves|viernes|sabado|domingo)|(dentro de |de (hoy|ma.ana|este (lunes|martes|miercoles|jueves|viernes|sabado|domingo)) en |en )([0-9]+ )(dia.|semana.)|([0-9]{1,2})(\/[0-9]{1,2}| de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre))",
}
