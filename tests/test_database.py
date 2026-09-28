"""Набор модульных тестов pytest для операций с базой данных (Задание 10)."""

import pytest
import sqlite3
from src.db_manager import DatabaseManager


@pytest.fixture
def test_db():
    """Фикстура изолированной базы данных в оперативной памяти."""
    manager = DatabaseManager(":memory:")
    manager.create_indexes()
    yield manager
    manager.close()


class TestDatabaseOperations:
    def test_insert_and_retrieve_student(self, test_db: DatabaseManager):
        # Задание 2: вставка данных
        st_id = test_db.insert_student(
            "Вафин Денис Наильевич", "221141", "vafin@example.com"
        )
        assert st_id > 0

        # Задание 6: параметризованный поиск
        found = test_db.get_student_by_email("vafin@example.com")
        assert found is not None
        assert found["id"] == st_id
        assert found["group_name"] == "221141"

    def test_unique_email_constraint(self, test_db: DatabaseManager):
        test_db.insert_student("Студент 1", "221141", "dup@example.com")
        with pytest.raises(sqlite3.IntegrityError):
            test_db.insert_student("Студент 2", "221141", "dup@example.com")

    def test_parameterized_search_by_name(self, test_db: DatabaseManager):
        test_db.insert_student("Иван Петров", "221141", "ivan@example.com")
        test_db.insert_student("Петр Иванов", "221141", "petr@example.com")
        test_db.insert_student("Сергей Сергеев", "221141", "sergey@example.com")

        res = test_db.search_students_by_name("Иван")
        assert len(res) == 2

    def test_multi_table_join(self, test_db: DatabaseManager):
        # Задание 8: проверка объединения JOIN
        s_id = test_db.insert_student("Вафин Денис", "221141", "dejid@example.com")
        c_id = test_db.insert_course("Python и БД", 54)
        test_db.insert_enrollment(s_id, c_id, 5)

        report = test_db.get_student_courses_report()
        assert len(report) == 1
        entry = report[0]
        assert entry["full_name"] == "Вафин Денис"
        assert entry["course_name"] == "Python и БД"
        assert entry["grade"] == 5

    def test_index_usage_in_explain_plan(self, test_db: DatabaseManager):
        # Задание 4: проверка работы индекса
        test_db.insert_student("Тест Индекса", "221141", "indexed@example.com")
        plan = test_db.explain_query_index("Тест Индекса")
        assert "idx_students_name" in plan
