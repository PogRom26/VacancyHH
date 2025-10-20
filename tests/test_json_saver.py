import pytest
import json
import os
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    def test_saver_initialization(self, json_saver):
        """Тест инициализации JSONSaver"""
        assert os.path.exists(json_saver.filename)

        # Проверяем что файл создан и пуст
        with open(json_saver.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data == []

    def test_data_directory_creation(self, tmp_path):
        """Тест создания папки data"""
        # Создаем путь с несуществующей папкой data
        data_dir = tmp_path / "data"
        test_file = data_dir / "test_vacancies.json"

        # Создаем saver - он должен создать папку data
        saver = JSONSaver(str(test_file))

        # Проверяем что папка data создана
        assert data_dir.exists()
        # Проверяем что файл создан
        assert test_file.exists()

    def test_add_and_get_vacancy(self, json_saver, vacancy_instance):
        """Тест добавления и получения вакансии"""
        # Добавляем вакансию
        json_saver.add_vacancy(vacancy_instance)

        # Получаем вакансии
        vacancies = json_saver.get_vacancies()

        assert len(vacancies) == 1
        assert vacancies[0].title == "Python Developer"
        assert vacancies[0].url == "https://hh.ru/vacancy/123456"

    def test_add_duplicate_vacancy(self, json_saver, vacancy_instance):
        """Тест добавления дублирующей вакансии"""
        json_saver.add_vacancy(vacancy_instance)
        json_saver.add_vacancy(vacancy_instance)  # Пытаемся добавить дубликат

        vacancies = json_saver.get_vacancies()
        assert len(vacancies) == 1  # Дубликат не должен добавиться

    def test_add_multiple_vacancies(self, json_saver, vacancy_list):
        """Тест массового добавления вакансий"""
        json_saver.add_vacancies(vacancy_list)

        vacancies = json_saver.get_vacancies()
        assert len(vacancies) == 3

    def test_delete_vacancy(self, json_saver, vacancy_instance):
        """Тест удаления вакансии"""
        json_saver.add_vacancy(vacancy_instance)
        assert len(json_saver.get_vacancies()) == 1

        json_saver.delete_vacancy(vacancy_instance)
        assert len(json_saver.get_vacancies()) == 0

    def test_clear_vacancies(self, json_saver, vacancy_list):
        """Тест очистки файла"""
        json_saver.add_vacancies(vacancy_list)
        assert len(json_saver.get_vacancies()) == 3

        json_saver.clear()
        assert len(json_saver.get_vacancies()) == 0

    def test_get_vacancies_with_keyword_filter(self, json_saver, vacancy_list):
        """Тест фильтрации по ключевому слову"""
        json_saver.add_vacancies(vacancy_list)

        # Ищем Python вакансии
        python_vacancies = json_saver.get_vacancies({"keyword": "python"})
        assert len(python_vacancies) == 3

        # Ищем Senior вакансии
        senior_vacancies = json_saver.get_vacancies({"keyword": "senior"})
        assert len(senior_vacancies) == 1
        assert senior_vacancies[0].title == "Senior Python"

    def test_get_vacancies_with_salary_filter(self, json_saver, vacancy_list):
        """Тест фильтрации по зарплате"""
        json_saver.add_vacancies(vacancy_list)

        # Вакансии с зарплатой от 100000
        high_salary = json_saver.get_vacancies({"min_salary": 100000})
        assert len(high_salary) == 2  # Middle и Senior

        # Вакансии с зарплатой до 100000
        low_salary = json_saver.get_vacancies({"max_salary": 100000})
        assert len(low_salary) == 1  # только Junior

    def test_file_info(self, json_saver, vacancy_instance):
        """Тест получения информации о файле"""
        json_saver.add_vacancy(vacancy_instance)

        file_info = json_saver.get_file_info()

        assert file_info['filename'] == json_saver.filename
        assert file_info['vacancies_count'] == 1
        assert file_info['file_exists'] is True
        assert file_info['file_size_bytes'] > 0