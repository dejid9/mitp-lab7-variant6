"""Модуль управления базой данных SQLite: параметры, JOIN, индексы."""

import sqlite3
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """Менеджер базы данных SQLite со строгой типизацией и безопасными запросами."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.init_schema()

    def init_schema(self) -> None:
        """Создаёт структуру таблиц базы данных."""
        with self.conn:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    group_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name TEXT NOT NULL,
                    hours INTEGER NOT NULL CHECK (hours > 0)
                );

                CREATE TABLE IF NOT EXISTS enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    grade INTEGER CHECK (grade BETWEEN 2 AND 5),
                    enrollment_date TEXT NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                        ON DELETE CASCADE
                );
                """
            )

    # Задание 4 (повышенное): Индексация и поиск
    def create_indexes(self) -> None:
        """Создаёт индексы для ускорения поиска по ФИО и email."""
        with self.conn:
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_students_name ON students(full_name);"
            )

    def explain_query_index(self, full_name: str) -> str:
        """Возвращает план выполнения запроса EXPLAIN QUERY PLAN."""
        cursor = self.conn.cursor()
        query = "EXPLAIN QUERY PLAN SELECT * FROM students WHERE full_name = ?"
        cursor.execute(query, (full_name,))
        rows = cursor.fetchall()
        return " | ".join(dict(r)["detail"] for r in rows)

    # Задание 2 (среднее): Вставить данные в таблицу
    def insert_student(self, full_name: str, group_name: str, email: str) -> int:
        """Вставляет запись о студенте с параметризацией запроса."""
        query = (
            "INSERT INTO students (full_name, group_name, email) "
            "VALUES (?, ?, ?)"
        )
        with self.conn:
            cursor = self.conn.execute(query, (full_name, group_name, email))
            return cursor.lastrowid or 0

    def insert_course(self, course_name: str, hours: int) -> int:
        """Вставляет запись о курсе."""
        query = "INSERT INTO courses (course_name, hours) VALUES (?, ?)"
        with self.conn:
            cursor = self.conn.execute(query, (course_name, hours))
            return cursor.lastrowid or 0

    def insert_enrollment(
        self,
        student_id: int,
        course_id: int,
        grade: int,
        date_str: str = "2026-09-28"
    ) -> int:
        """Вставляет запись о зачислении на курс с оценкой."""
        query = (
            "INSERT INTO enrollments "
            "(student_id, course_id, grade, enrollment_date) "
            "VALUES (?, ?, ?, ?)"
        )
        with self.conn:
            cursor = self.conn.execute(
                query, (student_id, course_id, grade, date_str)
            )
            return cursor.lastrowid or 0

    # Задание 6 (среднее): Использовать параметры запроса
    def get_student_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Ищет студента по email с использованием позиционных параметров ?."""
        query = "SELECT * FROM students WHERE email = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_students_by_name(self, name_query: str) -> List[Dict[str, Any]]:
        """Выполняет параметризованный поиск студентов по подстроке ФИО."""
        query = "SELECT * FROM students WHERE full_name LIKE ? ORDER BY full_name"
        cursor = self.conn.cursor()
        cursor.execute(query, (f"%{name_query}%",))
        return [dict(row) for row in cursor.fetchall()]

    # Задание 8 (среднее): Выполнить JOIN
    def get_student_courses_report(self) -> List[Dict[str, Any]]:
        """Выполняет INNER JOIN между students, enrollments и courses."""
        query = """
            SELECT
                s.id AS student_id,
                s.full_name,
                s.group_name,
                c.course_name,
                c.hours,
                e.grade,
                e.enrollment_date
            FROM enrollments e
            INNER JOIN students s ON e.student_id = s.id
            INNER JOIN courses c ON e.course_id = c.id
            ORDER BY s.full_name, c.course_name
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()
