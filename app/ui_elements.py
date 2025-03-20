import shutil

from config import Defaults, ui_txt
from datetime import date


def make_color(color):
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
    }
    return colors.get(color, "")


def make_style(style):
    styles = {
        "bold": "\033[1m",
        "underline": "\033[4m",
        "strike": "\033[9m",
        "none": "\033[0m",
    }
    return styles.get(style, "")


def print_line(text, **settings):
    style = make_style(settings.get("style", ""))
    color = make_color(settings.get("color", ""))
    reset_format = "\033[0m"
    print(f"{style}{color}{text}{reset_format}")


def print_div(**settings):
    style = make_style(settings.get("style", ""))
    color = make_color(settings.get("color", ""))
    divider = settings.get("div", ui_txt["layout"]["line"])
    width = max(
        shutil.get_terminal_size().columns // 2,
        settings.get("width", 0),
    )
    reset_format = "\033[0m"

    print(f"{style}{color}{divider * width}{reset_format}")


def print_ui(*data, **settings):
    text = ui_txt
    for level in data:
        try:
            text = text[level]
        except KeyError:
            raise KeyError(f"No key '{level}' in ui_text")

    prepend = settings.get("prepend", "")
    append = settings.get("append", "")
    text = " ".join(filter(None, [f"{prepend}", text, f"{append}"]))

    if settings.get("top", False) or settings.get("both", False):
        print_div(width=len(text) + 2, **settings)

    print_line(text, **settings)

    if settings.get("bottom", False) or settings.get("both", False):
        print_div(width=len(text) + 2, **settings)


def sort_key(task):
    return {
        getattr(task, "done", False),
        task.due_date is None,
        task.due_date or date.max,
    }


def print_context(context, context_name):
    if len(context) == 0:
        print_ui("printer", "empty_context", append=context_name, color="red")
        return

    print_ui("printer", "header_context", append=context_name, both=True)

    tasks_in = 0
    done = 0
    overdue = 0
    for task in list(sorted(context, key=sort_key)):
        tasks_in += 1
        color = "red" if task.due_date and task.due_date < date.today() else ""
        style = "strike" if task.done_date else ""
        if task.done_date:
            done += 1
        if task.due_date and task.due_date < date.today():
            overdue += 1
        print_line(f"- {task.task}", color=color, style=style)

    percent_done = (done * 100) / len(context)
    print_ui("printer", "total", prepend=tasks_in, top=True)
    if percent_done:
        print_ui("printer", "done", prepend=percent_done, color="green")
    if overdue:
        print_ui("printer", "overdue", prepend=overdue, color="red")
    print()


def print_search(tasks, limit, selected=False):
    print_ui("printer", "selected" if selected else "found", both=True)
    for i, task in list(sorted(tasks, key=lambda t: sort_key(t[1]))):
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print_ui("printer", "overflow", color="red")
            break
        if task.done:
            print_line(f"{i}) {task.task}", style="strike")
        else:
            print_line(f"{i}) {task.task}")

    print_ui("printer", "total", prepend=f"{len(tasks)}", top=True)
    print()
