import pytest
from unittest.mock import patch, Mock
import sys
import os

# Добавляем src в путь для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.vacancy import Vacancy


class TestUserInteraction:
    """Тесты для функций взаимодействия с пользователем"""

    @pytest.fixture
    def sample_vacancies(self):
        """Фикстура с тестовыми вакансиями"""
        return [
            Vacancy("Python Developer", "https://hh.ru/vacancy/1",
                    {"from": 100000, "to": 150000, "currency": "RUR"},
                    "Python development with Django", "Python experience"),
            Vacancy("Java Developer", "https://hh.ru/vacancy/2",
                    {"from": 120000, "to": 180000, "currency": "RUR"},
                    "Java development with Spring", "Java experience"),
        ]

    def test_filter_vacancies_basic(self):
        """Базовый тест фильтрации вакансий"""
        # Импортируем здесь, чтобы избежать проблем с моками
        from main import filter_vacancies

        vacancies = [
            Vacancy("Python Dev", "https://test.com", {"from": 100000}, "Python job", "Python"),
            Vacancy("Java Dev", "https://test.com", {"from": 120000}, "Java job", "Java"),
        ]

        # Фильтрация по Python
        filtered = filter_vacancies(vacancies, ["python"])
        assert len(filtered) == 1
        assert filtered[0].title == "Python Dev"

        # Без фильтра
        filtered = filter_vacancies(vacancies, [])
        assert len(filtered) == 2

    def test_sort_vacancies(self):
        """Тест сортировки вакансий"""
        from main import sort_vacancies

        vacancies = [
            Vacancy("Low", "https://test.com", {"from": 50000}, "Desc", "Req"),
            Vacancy("High", "https://test.com", {"from": 100000}, "Desc", "Req"),
        ]

        sorted_vacancies = sort_vacancies(vacancies)
        assert sorted_vacancies[0].title == "High"
        assert sorted_vacancies[1].title == "Low"

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий"""
        from main import get_top_vacancies

        vacancies = [
            Vacancy("1", "https://test.com", {"from": 100000}, "Desc", "Req"),
            Vacancy("2", "https://test.com", {"from": 90000}, "Desc", "Req"),
            Vacancy("3", "https://test.com", {"from": 80000}, "Desc", "Req"),
        ]

        top_2 = get_top_vacancies(vacancies, 2)
        assert len(top_2) == 2

        top_5 = get_top_vacancies(vacancies, 5)
        assert len(top_5) == 3

    @patch('builtins.input')
    def test_user_interaction_integration(self, mock_input):
        """Интеграционный тест user_interaction с прямым импортом"""
        # Мокаем ввод чтобы сразу выйти
        mock_input.side_effect = [
            "python", "1", "", "", "0"  # запрос, топ N, фильтры, выход
        ]

        # Импортируем и тестируем
        from main import user_interaction

        try:
            user_interaction()
            # Если дошли сюда - успех
            assert True
        except Exception as e:
            # Если есть исключение - тест провален
            pytest.fail(f"user_interaction failed with exception: {e}")

    @patch('builtins.input')
    @patch('main.HeadHunterAPI')
    @patch('main.JSONSaver')
    def test_user_interaction_mocked(self, mock_saver, mock_api, mock_input):
        """Тест с моками API и Saver"""
        # Настраиваем моки
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        mock_saver_instance = Mock()
        mock_saver.return_value = mock_saver_instance

        # Настройка возвращаемых значений
        mock_api_instance.get_vacancies.return_value = [{"test": "data"}]
        mock_saver_instance.get_file_info.return_value = {"vacancies_count": 0}

        # Мокаем Vacancy.cast_to_object_list
        with patch('main.Vacancy.cast_to_object_list') as mock_cast:
            mock_cast.return_value = [
                Vacancy("Test", "https://test.com", {"from": 100000}, "Desc", "Req")
            ]

            # Ввод пользователя
            mock_input.side_effect = [
                "test", "1", "", "", "0"  # запрос, топ N, фильтры, выход
            ]

            # Импортируем и запускаем
            from main import user_interaction

            try:
                user_interaction()
                # Проверяем вызовы
                mock_api_instance.get_vacancies.assert_called_once_with("test")
                mock_saver_instance.add_vacancies.assert_called_once()
                assert True
            except Exception as e:
                pytest.fail(f"Test failed with exception: {e}")

    @patch('builtins.input')
    @patch('main.HeadHunterAPI')
    def test_user_interaction_no_results(self, mock_api, mock_input):
        """Тест когда нет результатов"""
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance
        mock_api_instance.get_vacancies.return_value = []  # Пустой результат

        # Ввод только запроса
        mock_input.side_effect = ["nonexistent"]

        from main import user_interaction

        try:
            user_interaction()
            # Должен завершиться после "не найдено"
            mock_api_instance.get_vacancies.assert_called_once_with("nonexistent")
            assert True
        except Exception as e:
            pytest.fail(f"Test failed with exception: {e}")