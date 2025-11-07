import argparse
from unittest.mock import patch

import pytest
import csv
from src.main import parser_csv_report



class TestParserCSVReport:
    """Тесты функции parser_csv_report"""

    def create_test_csv(self, tmp_path, filename, data):
        """Создает временный CSV файл с тестовыми данными"""
        file_path = tmp_path / filename
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return file_path

    def test_single_file_processing(self, tmp_path):
        """Обработка одного CSV файла с корректными данными"""
        
        test_data = [
            {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
            {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
            {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
            {'name': 'iphone 14', 'brand': 'apple', 'price': '799', 'rating': '4.7'},
            {'name': 'galaxy a54', 'brand': 'samsung', 'price': '349', 'rating': '4.2'}
        ]

        temp_csv = self.create_test_csv(tmp_path, "test.csv", test_data)
        report_file = tmp_path / "test_report.csv"

        test_args = ['--files', str(temp_csv), '--report', str(report_file)]


        with patch('sys.argv', ['main'] + test_args):
            parser_csv_report()

        assert report_file.exists()

        with open(report_file,  encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

            assert len(rows) == 3
            assert rows[0] == ['apple', '4.8']
            assert rows[1] == ['samsung', '4.5']
            assert rows[2] == ['xiaomi', '4.6']

    def test_multiple_files_processing(self, tmp_path):
        """Обработка нескольких CSV файлов с агрегацией данных"""
        
        data1 = [
            {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
            {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
            {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
            {'name': 'iphone 14', 'brand': 'apple', 'price': '799', 'rating': '4.7'},
            {'name': 'galaxy a54', 'brand': 'samsung', 'price': '349', 'rating': '4.2'}
        ]

        data2 = [
            {"name": "poco x5 pro", "brand": "xiaomi", "price": 299, "rating": 4.4},
            {"name": "iphone se", "brand": "apple", "price": 429, "rating": 4.1},
            {"name": "galaxy z flip 5", "brand": "samsung", "price": 999, "rating": 4.6},
            {"name": "redmi 10c", "brand": "xiaomi", "price": 149, "rating": 4.1},
            {"name": "iphone 13 mini", "brand": "apple", "price": 599, "rating": 4.5}
        ]

        temp_csv1 = self.create_test_csv(tmp_path, "test1.csv", data1)
        temp_csv2 = self.create_test_csv(tmp_path, "test2.csv", data2)
        report_file = tmp_path / "test_report_multi.csv"

        test_args = ['--files', str(temp_csv1), str(temp_csv2), '--report', str(report_file)]

        
        with patch('sys.argv', ['main'] + test_args):
            parser_csv_report()

        
        assert report_file.exists()

        with open(report_file, encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

            assert len(rows) == 3
            assert rows[0] == ['apple', '4.55']
            assert rows[1] == ['samsung', '4.53']
            assert rows[2] == ['xiaomi', '4.37']

    def test_file_not_found(self, tmp_path):
        """Обработка отсутствующего файла"""

        non_existent_file = tmp_path / "non_existent.csv"
        report_file = tmp_path / "test_report.csv"

        test_args = ['--files', str(non_existent_file), '--report', str(report_file)]


        with patch('sys.argv', ['main'] + test_args):
            with pytest.raises(FileNotFoundError) as exc_info:
                parser_csv_report()

            assert "File not find" in str(exc_info.value)

    def test_valid_arguments(self):
        """Тест ввода различных аргументов"""

        parser = argparse.ArgumentParser("parser csv files")
        parser.add_argument("--files", nargs="+", required=True, help="csv files can be multiple files")
        parser.add_argument("--report", required=True, help="report name average-rating.csv")

        # валидные аргументы
        args = parser.parse_args(['--files', 'file1.csv', 'file2.csv', '--report', 'average-rating.csv'])

        assert args.files == ['file1.csv', 'file2.csv']
        assert args.report == 'average-rating.csv'

        # отсутствует обязательный --files
        with pytest.raises(SystemExit):
            parser.parse_args(['--report', 'average-rating.csv'])

        # отсутствует обязательный --report
        with pytest.raises(SystemExit):
            parser.parse_args(['--files', 'file.csv'])

         # Тест 4: Неизвестный аргумент
        with pytest.raises(SystemExit):
            parser.parse_args(['--files', 'file.csv', '--report', 'average-rating.csv', '--unknown', 'value'])

