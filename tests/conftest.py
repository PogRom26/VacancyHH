import pytest
import json
import os
import sys
from unittest.mock import Mock

# Добавляем src в путь для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.vacancy import Vacancy
from src.headhunter_api import HeadHunterAPI
from src.json_saver import JSONSaver


@pytest.fixture
def sample_vacancy_data():
    """Фикстура с примером данных вакансии"""
    return {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123456",
        "salary": {
            "from": 100000,
            "to": 150000,
            "currency": "RUR"
        },
        "description": "Разработка на Python и Django",
        "snippet": {
            "requirement": "Опыт работы от 3 лет"
        }
    }


@pytest.fixture
def sample_vacancy_dict():
    """Фикстура с данными для создания Vacancy"""
    return {
        "title": "Python Developer",
        "url": "https://hh.ru/vacancy/123456",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Разработка на Python и Django",
        "requirements": "Опыт работы от 3 лет"
    }


@pytest.fixture
def vacancy_instance(sample_vacancy_dict):
    """Фикстура с экземпляром Vacancy"""
    return Vacancy(**sample_vacancy_dict)


@pytest.fixture
def vacancy_without_salary():
    """Фикстура с вакансией без зарплаты"""
    return Vacancy(
        title="Developer",
        url="https://hh.ru/vacancy/789",
        salary=None,
        description="Описание",
        requirements="Требования"
    )


@pytest.fixture
def vacancy_list():
    """Фикстура со списком вакансий"""
    return [
        Vacancy("Junior Python", "https://hh.ru/vacancy/1",
               {"from": 50000, "to": 80000, "currency": "RUR"},
               "Описание 1", "Требования 1"),
        Vacancy("Middle Python", "https://hh.ru/vacancy/2",
               {"from": 100000, "to": 150000, "currency": "RUR"},
               "Описание 2", "Требования 2"),
        Vacancy("Senior Python", "https://hh.ru/vacancy/3",
               {"from": 180000, "to": 250000, "currency": "RUR"},
               "Описание 3", "Требования 3"),
    ]


@pytest.fixture
def json_saver(tmp_path):
    """Фикстура с JSONSaver для временного файла"""
    # Используем временную директорию напрямую
    test_file = tmp_path / "vacancies.json"
    saver = JSONSaver(str(test_file))
    return saver


@pytest.fixture
def sample_api_response():
    """Фикстура с примером ответа от API HH"""
    return {
        "items": [
            {
                "id": "1",
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Python development",
                "snippet": {"requirement": "Python experience"}
            },
            {
                "id": "2",
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/2",
                "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
                "description": "Java development",
                "snippet": {"requirement": "Java experience"}
            }
        ]
    }