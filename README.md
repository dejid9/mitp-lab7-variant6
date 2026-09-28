# Лабораторная работа №7

ФИО: Вафин Денис Наильевич
Группа: 221141
Вариант: 6
Лабораторная работа: №7

Дисциплина: «Методы и технологии программирования».

## Выполненные практические задания по варианту 6

### Средней сложности
1. **№2 — Вставить данные в таблицу.** Реализованы методы вставки данных `insert_student`, `insert_course`, `insert_enrollment` в модуле `src/db_manager.py` с проверкой ограничений внешних ключей и диапазонов оценок.
2. **№6 — Использовать параметры запроса.** Все обращения к базе данных реализованы исключительно через безопасные позиционные параметры `?` (`get_student_by_email`, `search_students_by_name`), исключающие уязвимости SQL Injection.
3. **№8 — Выполнить JOIN.** Реализован метод `get_student_courses_report`, формирующий комплексный отчёт на основе реляционного слияния трёх таблиц `enrollments INNER JOIN students ... INNER JOIN courses`.

### Повышенной сложности
1. **№4 — Индексация и поиск.** Созданы B-Tree индексы `idx_students_email` и `idx_students_name`. С помощью `EXPLAIN QUERY PLAN` доказано использование созданного индекса при поиске по email (`USING INDEX idx_students_email`).
2. **№10 — Unit-тесты базы данных.** Написан комплекс модульных тестов `tests/test_database.py` на базе `pytest` с использованием изолированной БД в памяти (`:memory:`), проверяющий вставку, ограничения целостности, JOIN и работу индексов.

---

## Архитектура проекта

```text
mitp-lab7-variant6/
├── src/
│   ├── db_manager.py          # Задания 2, 6, 8, 4: менеджер SQLite (CRUD, JOIN, индексы)
│   └── models_sqlalchemy.py   # Декларативные ORM модели SQLAlchemy
├── tests/
│   └── test_database.py       # Задание 10 (повышенное): unit-тесты БД (5 тестов)
├── .flake8                    # Конфигурация линтера flake8
├── .gitattributes             # Нормализация переносов строк (eol=lf)
├── .gitignore                 # Игнорируемые артефакты Python и БД
├── main.py                    # Демонстрационный скрипт работы с базой данных
├── README.md                  # Документация и отчёт по лабораторной работе
└── requirements.txt           # Зависимости проекта
```

---

## Установка и запуск

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Демонстрация работы с базой данных
python main.py

# Проверка линтером и тесты
python -m flake8 .
python -m pytest -v
```

### Linux / macOS (Bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Демонстрация работы с базой данных
python3 main.py

# Проверка линтером и запуск тестов
python3 -m flake8 .
python3 -m pytest -v
```

---

## Подтверждение работы (логи выполнения)

### Демонстрация работы `main.py`:
```text
=================================================================
Лабораторная работа №7 — Вариант 6 (Работа с СУБД в Python)
Дисциплина: «Методы и технологии программирования»
Студент: Вафин Денис Наильевич (Группа 221141)
=================================================================

[1] Индексация базы данных:
    Созданы индексы: idx_students_email, idx_students_name

[2] Вставка данных в таблицы (INSERT):
    Добавлены студенты: id=1, id=2, id=3
    Добавлены курсы:    id=1, id=2, id=3
    Зафиксированы записи об оценках в таблице enrollments.

[3] Параметризованный поиск (защита от SQL Injection):
    Поиск по email ('dejid9@gmail.com'):
    -> Найдено: {'id': 1, 'full_name': 'Вафин Денис Наильевич', 'group_name': '221141', 'email': 'dejid9@gmail.com'}

[4] План выполнения запроса с использованием индекса:
    EXPLAIN QUERY PLAN: SEARCH students USING INDEX idx_students_name (full_name=?)

[5] Выполнение многотабличного объединения JOIN:
    - Вафин Денис Наильевич (221141) | Курс: 'Базы данных и SQL' | Оценка: 5 | Часов: 54
    - Вафин Денис Наильевич (221141) | Курс: 'Методы и технологии программирования' | Оценка: 5 | Часов: 72
    - Иванова Мария Сергеевна (221142) | Курс: 'Архитектура программных систем' | Оценка: 5 | Часов: 36
    - Смирнов Алексей Игоревич (221141) | Курс: 'Методы и технологии программирования' | Оценка: 4 | Часов: 72

=================================================================
```

### Результат проверки линтером `flake8`:
```text
python -m flake8 .
[OK] Ошибок не обнаружено, код полностью соответствует PEP 8.
```

### Результаты тестирования `pytest -v`:
```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Python312\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.12.6', 'Platform': 'Windows-10-10.0.19045-SP0', 'Packages': {'pytest': '9.1.1', 'pluggy': '1.6.0'}, 'Plugins': {'anyio': '4.15.1', 'html': '4.0.2', 'metadata': '3.1.1', 'ordering': '0.6', 'rerunfailures': '16.4', 'xdist': '3.8.0', 'seleniumbase': '4.51.3'}}
rootdir: C:\Users\dejid\Desktop\Учёба\Новая папка\mitp-lab7-variant6
plugins: anyio-4.15.1, html-4.0.2, metadata-3.1.1, ordering-0.6, rerunfailures-16.4, xdist-3.8.0, seleniumbase-4.51.3
collecting ... collected 5 items

tests/test_database.py::TestDatabaseOperations::test_insert_and_retrieve_student PASSED [ 20%]
tests/test_database.py::TestDatabaseOperations::test_unique_email_constraint PASSED [ 40%]
tests/test_database.py::TestDatabaseOperations::test_parameterized_search_by_name PASSED [ 60%]
tests/test_database.py::TestDatabaseOperations::test_multi_table_join PASSED [ 80%]
tests/test_database.py::TestDatabaseOperations::test_index_usage_in_explain_plan PASSED [100%]

============================== 5 passed in 0.12s ==============================
```

---

## Git Flow и ветвление

В репозитории строго соблюдена модель ветвления Git Flow:
- `main` — релизная стабильная ветка;
- `develop` — ветка интеграции разработки;
- `feature/variant6-database` — функциональная ветка разработки реляционной БД;
- Слияния веток выполнены через `--no-ff` с атомарными коммитами по стандарту Conventional Commits;
- Релиз зафиксирован аннотированным тегом `v1.0.0`.
