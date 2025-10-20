"""Дополнительные фикстуры с тестовыми данными"""

import pytest


@pytest.fixture
def large_vacancy_list():
    """Большой список вакансий для тестирования производительности"""
    vacancies = []
    for i in range(100):
        vacancies.append({
            "id": str(i),
            "name": f"Developer {i}",
            "alternate_url": f"https://hh.ru/vacancy/{i}",
            "salary": {
                "from": 50000 + i * 1000,
                "to": 80000 + i * 1000,
                "currency": "RUR"
            },
            "description": f"Description {i}",
            "snippet": {"requirement": f"Requirements {i}"}
        })
    return vacancies


@pytest.fixture
def vacancy_with_special_characters():
    """Вакансия со специальными символами"""
    return {
        "title": "Python/Django Developer (Full-Stack)",
        "url": "https://hh.ru/vacancy/special-chars",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Работа с Python 3.8+, Django 3.2+, REST API",
        "requirements": "Опыт работы 2+ года, знание Docker, Kubernetes"
    }