from config import Defaults, ui_txt, colors, styles
from datetime import date


def print_line(text, style=None, color=None):
    color = colors.get(color, "")
    style = styles.get(style, "")
    reset_format = "\033[0m" if style or color else ""
    print(f"{style}{color}{text}{reset_format}")


def print_ui(*data, **settings):
    if len(data) != 2:
        raise ValueError("the list [section, name] is required")

    text = ui_txt
    for level in data:
        try:
            text = text[level]
        except KeyError:
            raise KeyError(f"No key '{level}' in ui_text")

    prepend = settings.get("prepend", "")
    append = settings.get("append", "")
    text = " ".join(filter(None, [f"{prepend}", text, f"{append}"]))

    style = settings.get("style")
    color = settings.get("color")
    divider = settings.get("divider", ui_txt["layout"]["line"])

    if settings.get("top", False):
        print_line(divider * len(text), style, color)

    print_line(text, style, color)

    if settings.get("bottom", False):
        print_line(divider * len(text), style, color)


def print_context(context):
    if len(context) == 0:
        print_ui("printer", "empty_context", color="red")
        return

    print_ui("printer", "header_context", top=True)
    sorted_context = list(
        sorted(context, key=lambda t: (t.done, t.due_date or date.max))
    )

    tasks_in = 0
    done = 0
    for i, task in enumerate(sorted_context):
        tasks_in += 1
        if task.done_date:
            done += 1
            print_line(f"{i}) {task.task}", style="strike")
            continue
        print_line(f"{i}) {task.task}")

    percent_done = f"{(done * 100) / len(context)}%"
    print_ui("printer", "done", prepend=percent_done, color="green")
    print_ui("printer", "total", prepend=tasks_in, bottom=True, style="bold")


def print_search(tasks, limit):
    if not tasks:
        print_ui("printer", "no_found", color="red")

    sorted_tasks = list(sorted(lambda t: (t.due_date, t.done), tasks))
    i = 1
    for _, task in sorted_tasks:
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print_ui("printer", "search_overflow", color="red")
            break
        if task.done:
            print_line(f"{i}) {task.task}", style="strike")
        else:
            print_line(f"{i}) {task.task}")
        i += 1

    print_ui("printer", "found", prepend=f"{len(tasks)}", bottom=True)
