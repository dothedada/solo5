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
    divider = settings.get("divider", ui_txt["layout"]["line"])
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


def print_context(context, context_name):
    if len(context) == 0:
        print_ui("printer", "empty_context", append=context_name, color="red")
        return

    print_ui("printer", "header_context", append=context_name, both=True)
    sorted_context = list(
        sorted(
            context,
            key=lambda t: (
                getattr(t, "done", False),
                t.due_date is None,
                t.due_date or date.max,
            ),
        )
    )

    tasks_in = 0
    done = 0
    for task in sorted_context:
        tasks_in += 1
        if task.done_date:
            done += 1
            print_line(f"{tasks_in}) {task.task}", style="strike")
            continue
        print_line(f"{tasks_in}) {task.task}")

    percent_done = f"{(done * 100) / len(context)}%"
    print_ui("printer", "done", prepend=percent_done, top=True, color="green")
    print_ui("printer", "total", prepend=tasks_in, divider=" ", bottom=True)


def print_search(tasks, limit):
    if not tasks:
        print_ui("printer", "no_found", color="red")

    print_ui("printer", "found", both=True)
    i = 1
    for _, task in tasks:
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print_ui("printer", "search_overflow", color="red")
            break
        if task.done:
            print_line(f"{i}) {task.task}", style="strike")
        else:
            print_line(f"{i}) {task.task}")
        i += 1

    print_ui("printer", "total", prepend=f"{len(tasks)}", top=True)
    print()
