from registry import Registry

INPUT_FILE = "anketa.txt"


def main():
    reg = Registry()
    if not reg.load(INPUT_FILE):
        print(f"Файл {INPUT_FILE} не найден. Программа завершена.")
        return

    reg.print_table()
    reg.print_errors()

    print(f"\nПринято: {len(reg)} | Отклонено: {len(reg.bad)}")

    print("\nПо ролям:")
    for role, count in sorted(reg.stats_by_role().items()):
        print(f"  {role:<15} {count}")

    print("\nПо группам:")
    for group, count in sorted(reg.stats_by_group().items()):
        print(f"  {group:<15} {count}")

    reg.save_ok()
    reg.save_errors()
    print(f"\nСохранено: ok.txt и errors.txt")


main()