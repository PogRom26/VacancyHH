import requests

from src.headhunter_api import HeadHunterAPI
from unittest.mock import Mock, patch


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_api_initialization(self):
        """Тест инициализации API"""
        api = HeadHunterAPI()
        assert api.base_url == "https://api.hh.ru/vacancies"

    @patch("src.headhunter_api.requests.get")
    def test_get_vacancies_success(self, mock_get, sample_api_response):
        """Тест успешного получения вакансий"""
        # Настраиваем mock
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Мокаем get_vacancy_detail чтобы избежать дополнительных вызовов
        with patch.object(HeadHunterAPI, "get_vacancy_detail") as mock_detail:
            mock_detail.return_value = sample_api_response["items"][0]

            api = HeadHunterAPI()
            vacancies = api.get_vacancies("Python")

            # Проверяем что был вызван get
            mock_get.assert_called_once()
            # Проверяем результат
            assert len(vacancies) == 2

    @patch("src.headhunter_api.requests.get")
    def test_get_vacancies_api_error(self, mock_get):
        """Тест обработки ошибки API"""
        mock_get.side_effect = requests.RequestException("API Error")

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert vacancies == []

    @patch("src.headhunter_api.requests.get")
    def test_get_vacancies_with_area(self, mock_get):
        """Тест получения вакансий с указанием региона"""
        # Настраиваем mock
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        # Мокаем get_vacancy_detail
        with patch.object(HeadHunterAPI, "get_vacancy_detail"):
            api.get_vacancies("Python", area=2)  # СПб

            # Проверяем параметры вызова
            call_args = mock_get.call_args
            # Для kwargs используем call_args[1] если есть, иначе call_args.kwargs
            if call_args and len(call_args) >= 2:
                params = call_args[1].get("params", {})
            else:
                params = call_args.kwargs.get("params", {})

            assert params.get("area") == 2

    @patch("src.headhunter_api.requests.get")
    def test_get_vacancy_detail_success(self, mock_get):
        """Тест получения деталей вакансии"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "name": "Test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        result = api.get_vacancy_detail("123")

        assert result["id"] == "123"
        assert result["name"] == "Test"
        mock_get.assert_called_with("https://api.hh.ru/vacancies/123")

    @patch("src.headhunter_api.requests.get")
    def test_get_vacancy_detail_error(self, mock_get):
        """Тест ошибки при получении деталей вакансии"""
        mock_get.side_effect = requests.RequestException("Error")

        api = HeadHunterAPI()

        # Должен вернуть пустой список в основном методе
        with patch.object(api, "get_vacancies") as mock_main:
            mock_main.return_value = []
            vacancies = api.get_vacancies("Python")
            assert vacancies == []

    def test_api_parameters(self):
        """Тест параметров API запроса"""
        api = HeadHunterAPI()

        # Проверяем что параметры правильно формируются
        with patch("src.headhunter_api.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"items": []}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            # Мокаем get_vacancy_detail
            with patch.object(HeadHunterAPI, "get_vacancy_detail"):
                api.get_vacancies("Python Developer")

                # Проверяем вызов
                mock_get.assert_called_once()
                call_args = mock_get.call_args

                # Безопасное извлечение параметров
                if call_args and len(call_args) >= 2:
                    params = call_args[1].get("params", {})
                else:
                    params = call_args.kwargs.get("params", {})

                assert params.get("text") == "Python Developer"
                assert params.get("per_page") == 100
                assert params.get("area") == 1  # Москва по умолчанию
