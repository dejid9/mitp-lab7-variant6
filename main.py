"""Главный модуль демонстрации работы с базой данных (Лабораторная №7)."""

import os
from src.db_manager import DatabaseManager


def main() -> None:
    print("=" * 65)
    print("Лабораторная работа №7 — Вариант 6 (Работа с СУБД в Python)")
    print("Дисциплина: «Методы и технологии программирования»")
    print("Студент: Вафин Денис Наильевич (Группа 221141)")
    print("=" * 65)

    db_file = "mitp_lab7.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    db = DatabaseManager(db_file)

    # 1. Задание 4 (повышенное): Индексация
    db.create_indexes()
    print("\n[1] Индексация базы данных:")
    print("    Созданы индексы: idx_students_email, idx_students_name")

    # 2. Задание 2 (среднее): Вставка данных в таблицу
    s1 = db.insert_student("Вафин Денис Наильевич", "221141", "dejid9@gmail.com")
    s2 = db.insert_student("Смирнов Алексей Игоревич", "221141", "smirnov@example.com")
    s3 = db.insert_student("Иванова Мария Сергеевна", "221142", "ivanova@example.com")

    c1 = db.insert_course("Методы и технологии программирования", 72)
    c2 = db.insert_course("Базы данных и SQL", 54)
    c3 = db.insert_course("Архитектура программных систем", 36)

    db.insert_enrollment(s1, c1, 5)
    db.insert_enrollment(s1, c2, 5)
    db.insert_enrollment(s2, c1, 4)
    db.insert_enrollment(s3, c3, 5)

    print("\n[2] Вставка данных в таблицы (INSERT):")
    print(f"    Добавлены студенты: id={s1}, id={s2}, id={s3}")
    print(f"    Добавлены курсы:    id={c1}, id={c2}, id={c3}")
    print("    Зафиксированы записи об оценках в таблице enrollments.")

    # 3. Задание 6 (среднее): Использование параметров запроса
    print("\n[3] Параметризованный поиск (защита от SQL Injection):")
    target_email = "dejid9@gmail.com"
    found = db.get_student_by_email(target_email)
    print(f"    Поиск по email ('{target_email}'):")
    print(f"    -> Найдено: {found}")

    # 4. Задание 4 (повышенное): Индексация и план выполнения EXPLAIN QUERY PLAN
    plan = db.explain_query_index("Вафин Денис Наильевич")
    print("\n[4] План выполнения запроса с использованием индекса:")
    print(f"    EXPLAIN QUERY PLAN: {plan}")

    # 5. Задание 8 (среднее): Выполнить JOIN
    print("\n[5] Выполнение многотабличного объединения JOIN:")
    report = db.get_student_courses_report()
    for row in report:
        print(
            f"    - {row['full_name']} ({row['group_name']}) | "
            f"Курс: '{row['course_name']}' | "
            f"Оценка: {row['grade']} | Часов: {row['hours']}"
        )

    db.close()
    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
