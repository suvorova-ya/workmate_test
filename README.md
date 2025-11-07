# CSV Report Generator

Скрипт формирует отчёт **average-rating** по среднему рейтингу брендов из переданных CSV-файлов.  
Каждая строка входных файлов должна содержать поля: `name`, `brand`, `price`, `rating`.  
Результирующий отчёт сортируется по названию бренда и сохраняется в указанный CSV-файл.

```bash
# Клонировать репозиторий
git clone git@github.com:suvorova-ya/workmate_test.git
cd workmate_test

# Установить зависимости
poetry install

```

```bash
# Перейти в папку src
cd src

# Запустить скрипт с двумя CSV-файлами
python main.py --files products1.csv products2.csv --report average-rating
```

## Пример запуска скрипта

```text
+---+---------+--------+
|   | brand   | rating |
+---+---------+--------+
| 1 | apple   | 4.55   |
| 2 | samsung | 4.53   |
| 3 | xiaomi  | 4.37   |
+---+---------+--------+

```


```bash
# Для запуска тестов необходимо вернуться в корень проекта:
cd src

# Запустить тест
pytest

Результат выполнения:

tests/test_parsing_csv.py::TestParserCSVReport::test_single_file_processing PASSED
tests/test_parsing_csv.py::TestParserCSVReport::test_multiple_files_processing PASSED
tests/test_parsing_csv.py::TestParserCSVReport::test_file_not_found PASSED
tests/test_parsing_csv.py::TestParserCSVReport::test_valid_arguments PASSED
=========================== 4 passed in 0.07s ===========================

Проверка покрытия кода:

pytest --cov=src

Результат:

Name              Stmts   Miss  Cover
-------------------------------------
src/__init__.py       0      0   100%
src/main.py          32      3    91%
-------------------------------------
TOTAL                32      3    91%
```

