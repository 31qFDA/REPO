import os

from validators import parse_line
from report import (
    print_table,
    print_errors,
    save_files,
    OK_FILE,
    ERRORS_FILE,
)

INPUT_FILE = "anketa.txt"


def read_lines(path):
    if not os.path.exists(path):
        print(f"Файл {path} не найден. Программа завершена.")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except OSError as e:
        print(f"Не удалось прочитать файл {path}: {e}")
        return None


def process(lines):
    good = []
    bad = []
    total_lines = 0
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        total_lines += 1
        anketa, reason = parse_line(stripped)
        if anketa:
            good.append(anketa)
        else:
            bad.append((line_no, stripped, reason))
    good.sort(key=lambda a: a["fio"])
    return good, bad, total_lines


def print_summary(good, bad, total_lines):
    print(f"\nВсего строк в файле: {total_lines}")
    print(f"Принято: {len(good)} | Отклонено: {len(bad)}")

    stat = {}
    for a in good:
        stat[a["group"]] = stat.get(a["group"], 0) + 1
    print("\nПо группам:")
    for group in sorted(stat):
        print(f"  {group}   {stat[group]}")


def main():
    lines = read_lines(INPUT_FILE)
    if lines is None:
        return

    good, bad, total_lines = process(lines)

    print_table(good)
    print_errors(bad)
    print_summary(good, bad, total_lines)

    save_files(good, bad)
    print(f"\nСохранено: {OK_FILE} и {ERRORS_FILE}")


if __name__ == "__main__":
    main()