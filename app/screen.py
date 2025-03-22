import sys
import builtins

sys_print = builtins.print
sys_input = builtins.input


def set_print_counter(screen_manager):
    def print_counter(*args, **kwargs):
        text = " ".join([str(arg) for arg in args])
        line_count = text.count("\n") + 1
        screen_manager.add_lines(line_count)
        sys_print(*args, **kwargs)

    return print_counter


def set_input_counter(screen_manager):
    def input_counter(prompt=""):
        line_count = prompt.count("\n") + 1
        screen_manager.add_lines(line_count)
        return sys_input(prompt)

    return input_counter


class ScreenManager:
    def __init__(self, protected_lines=3):
        self.lines = 0
        self.protected_lines = protected_lines

    def add_lines(self, count=1):
        self.lines += count

    def exit(self):
        if self.lines > 0:
            for _ in range(self.lines):
                sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()
            self.lines = 0

    def clear(self):
        lines_to_clear = max(0, self.lines - self.protected_lines)
        if lines_to_clear > 0:
            for _ in range(lines_to_clear):
                sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()
            self.lines = self.protected_lines
