import calendar
import re
from datetime import date
from enum import Enum

from config import Defaults
from regexGenerator import TaskRegex, UIRegex
from task import Task


class Confirm(Enum):
    YES = "yes"
    NO = "no"
    OUT = "cancel"
    ERR = "error"


class Command(Enum):
    ADD_TASKS = "add_tasks"
    MAKE_TODAY = "make_today"
    UPDATE_TASK = "update_task"
    MARK_DONE = "mark_done"
    DELETE_TASKS = "delete_tasks"
    IN_TODAY = "in_today"
    IN_GLOBAL = "in_global"
    IN_DONE = "in_done"
    SEARCH = "search"
    EXIT = "exit"
    PURGE = "purge"
    FIX_DATES = "fix_dates"
    ENCORE = "encore"
    HELP = "help"
    ERR = "error"


class InputParser:
    def __init__(self):
        self._lang = Defaults.LANG.value
        self._parser = UIRegex.of(self._lang)

    def confirm(self, input_str):
        for response, regex in self._parser["confirm"].items():
            if re.search(regex, input_str):
                return Confirm(response)
        return Confirm.ERR

    def command(self, input_str):
        for response, regex in self._parser["command"].items():
            if re.search(regex, input_str):
                return Command(response)
        return Command.ERR


class TaskParser:
    def __init__(self):
        self._lang = Defaults.LANG.value
        self._parser = TaskRegex.of(self._lang)

    # Compares the string with the regex source to get the object or the index
    def _matcher(func):
        def wrapper(self, string, regex_src):
            for i, pattern in enumerate(self._parser["regex_for"][regex_src]):
                match = re.search(pattern, string)
                if match:
                    return func(self, match=match, match_index=i)

            return func(self, match=None, match_index=-1)

        return wrapper

    @_matcher
    def _match_bool(self, match, match_index):
        return True if match else False

    @_matcher
    def _match_ind(self, match, match_index):
        return match_index

    @_matcher
    def _match_dict(self, match, match_index):
        return match.group() if match else None

    @_matcher
    def parse_date(self, match, match_index):
        if match is None:
            return None

        date_info = match.groupdict()
        base_date = self._get_date(date_info)

        if date_info.get("date"):
            return base_date

        add_days, add_monts, add_years = self._get_date_modifier(date_info)

        year, month, day = TaskParser.normalize_date(
            base_date.year + add_years,
            base_date.month + add_monts,
            base_date.day + add_days,
        )
        return date(year, month, day)

    def _get_next_weekday(self, name):
        return (self._match_ind(name, "week") - date.today().weekday()) % 7

    def _get_month(self, data_dict):
        if month_num := data_dict.get("month_num"):
            return int(month_num)
        elif month_name := data_dict.get("month_name"):
            return self._match_ind(month_name, "months") + 1

        return date.today().month

    def _get_date(self, data_dict):
        if data_dict.get("from") is None:
            return date.today()

        b_day = date.today().day
        if today_rel := data_dict.get("today_rel"):
            b_day += self._match_ind(today_rel, "today_rel")
        elif weekday := data_dict.get("weekday"):
            b_day += self._get_next_weekday(weekday)
        elif day_str := data_dict.get("day_str"):
            b_day = self._match_ind(day_str, "enumeration_str")
        elif (day := data_dict.get("day")) and day.isnumeric():
            b_day = int(day)
        else:
            print("Cannot parse the day setted")

        b_month = self._get_month(data_dict)
        b_year = data_dict.get("year", date.today().year)

        year, month, day = TaskParser.normalize_date(b_year, b_month, b_day)

        if date(year, month, day) < date.today():
            year += 1

        return date(year, month, day)

    def _get_date_modifier(self, data_dict):
        if data_dict.get("modifier") is None:
            return 0, 0, 0

        amount = 0
        if parsed_amount := data_dict.get("amount", None):
            if parsed_amount.isnumeric():
                amount = int(parsed_amount)
            else:
                amount += self._match_ind(parsed_amount, "amount_str")

        def add_amount(unit):
            return amount if data_dict.get(unit) is not None else 0

        days = add_amount("unit_day")
        days += add_amount("unit_week") * 7
        months = add_amount("unit_month")
        years = add_amount("unit_year")

        return days, months, years

    def _get_dificulty(self, task_raw):
        if (parsed_diff := self._match_ind(task_raw, "dificulty")) > 0:
            return parsed_diff

        if parsed_diff == -1:
            return Defaults.BASE_DIF.value

        dificulty_l = re.search(self._parser["globals"]["dificulty"], task_raw)
        return int(dificulty_l.group()[1:])

    @staticmethod
    def sanitize_text(string):
        string = string.strip()
        string = re.sub(r"\s+", " ", string)

        return string

    @staticmethod
    def normalize_date(year, month, day):
        try:
            date(year, month, day)
            return year, month, day
        except ValueError:
            days_in_mont = calendar.monthrange(year, month)[1]

            while day > days_in_mont:
                day -= days_in_mont
                month += 1
                if month > 12:
                    month = 1
                    year += 1
                days_in_mont = calendar.monthrange(year, month)[1]

        return year, month, day

    @staticmethod
    def make_tasks_from_csv(tasks_list):
        tasks = []

        def get_csv_date(date_data):
            return date.fromisoformat(date_data) if date_data else None

        for task in tasks_list:
            task["done"] = task.get("done") == "True"
            task["undelayable"] = task.get("undelayable") == "True"
            task["dificulty"] = int(task.get("dificulty"))
            task["creation_date"] = get_csv_date(task.get("creation_date"))
            task["due_date"] = get_csv_date(task.get("due_date"))

            tasks.append(Task(task))

        return tasks

    def make_task(self, string):
        tasks = []

        for i, task_raw in enumerate(string.split(Defaults.TASK_SPLIT.value)):
            if task_raw.strip() == "":
                continue

            task = Task(
                {
                    "lang": self._lang,
                    "task": TaskParser.sanitize_text(task_raw),
                    "done": False,
                    "project": self._match_dict(task_raw, "project"),
                    "undelayable": self._match_bool(task_raw, "undelayable"),
                    "dificulty": self._get_dificulty(task_raw),
                    "due_date": self.parse_date(task_raw, "dates"),
                }
            )
            tasks.append(task)

        return tasks
