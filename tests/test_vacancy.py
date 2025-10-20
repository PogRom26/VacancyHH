import pytest

from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_vacancy_creation(self, vacancy_instance):
        """Тест создания вакансии"""
        assert vacancy_instance.title == "Python Developer"
        assert vacancy_instance.url == "https://hh.ru/vacancy/123456"
        assert vacancy_instance.salary["from"] == 100000
        assert vacancy_instance.salary["to"] == 150000
        assert vacancy_instance.description == "Разработка на Python и Django"

    def test_vacancy_creation_with_string_salary(self):
        """Тест создания вакансии со строкой зарплаты"""
        vacancy = Vacancy(
            title="Developer",
            url="https://hh.ru/vacancy/123",
            salary="100 000-150 000 руб.",
            description="Test",
            requirements="Test",
        )
        assert vacancy.salary["from"] == 100000
        assert vacancy.salary["to"] == 150000
        assert vacancy.salary["currency"] == "руб."

    def test_vacancy_without_salary(self, vacancy_without_salary):
        """Тест вакансии без зарплаты"""
        assert vacancy_without_salary.salary["from"] == 0
        assert vacancy_without_salary.salary["to"] == 0
        assert vacancy_without_salary.salary["currency"] == "не указана"

    def test_average_salary(self, vacancy_instance, vacancy_without_salary):
        """Тест расчета средней зарплаты"""
        assert vacancy_instance.get_average_salary() == 125000
        assert vacancy_without_salary.get_average_salary() == 0

    def test_average_salary_only_from(self):
        """Тест средней зарплаты когда указана только нижняя граница"""
        vacancy = Vacancy(
            title="Dev",
            url="https://test.com",
            salary={"from": 100000, "currency": "RUR"},
            description="Test",
        )
        assert vacancy.get_average_salary() == 100000

    def test_average_salary_only_to(self):
        """Тест средней зарплаты когда указана только верхняя граница"""
        vacancy = Vacancy(
            title="Dev",
            url="https://test.com",
            salary={"to": 150000, "currency": "RUR"},
            description="Test",
        )
        assert vacancy.get_average_salary() == 150000

    def test_comparison_operators(self, vacancy_list):
        """Тест операторов сравнения"""
        junior, middle, senior = vacancy_list

        # senior (215000) > middle (125000) > junior (65000)
        assert senior > middle
        assert middle > junior
        assert junior < senior
        assert middle >= junior
        assert junior <= middle
        assert senior != junior

    def test_to_dict_method(self, vacancy_instance):
        """Тест преобразования в словарь"""
        vacancy_dict = vacancy_instance.to_dict()

        assert vacancy_dict["title"] == "Python Developer"
        assert vacancy_dict["url"] == "https://hh.ru/vacancy/123456"
        assert vacancy_dict["salary"]["from"] == 100000
        assert isinstance(vacancy_dict, dict)

    def test_from_dict_method(self, sample_vacancy_dict):
        """Тест создания из словаря"""
        vacancy = Vacancy.from_dict(sample_vacancy_dict)

        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123456"
        assert vacancy.salary["from"] == 100000

    def test_str_representation(self, vacancy_instance):
        """Тест строкового представления"""
        string_repr = str(vacancy_instance)
        assert "Python Developer" in string_repr
        assert "https://hh.ru/vacancy/123456" in string_repr
        assert "100 000 - 150 000" in string_repr  # Исправлено: без запятых
        assert "RUR" in string_repr

    def test_cast_to_object_list(self, sample_api_response):
        """Тест преобразования JSON в список объектов"""
        vacancies = Vacancy.cast_to_object_list(sample_api_response["items"])

        assert len(vacancies) == 2
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].title == "Python Developer"
        assert vacancies[1].title == "Java Developer"

    def test_invalid_url_validation(self):
        """Тест валидации некорректного URL"""
        with pytest.raises(ValueError):
            Vacancy("Test", "invalid_url", None, "Test")

    def test_empty_title_validation(self):
        """Тест валидации пустого названия"""
        with pytest.raises(ValueError):
            Vacancy("", "https://test.com", None, "Test")

    def test_url_with_angle_brackets(self):
        """Тест URL с угловыми скобками"""
        vacancy = Vacancy("Test", "<https://hh.ru/vacancy/123>", None, "Test")
        assert vacancy.url == "https://hh.ru/vacancy/123"
