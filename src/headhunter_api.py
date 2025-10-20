import requests

from src.vacancy_api import VacancyAPI
from typing import List, Dict, Any

class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str, area: int = 1) -> List[Dict[str, Any]]:
        """
        Получить вакансии с hh.ru

        Args:
            search_query: Поисковый запрос
            area: ID региона (1 - Москва, 2 - СПб, 113 - Россия)

        Returns:
            Список вакансий в формате JSON
        """
        params = {
            'text': search_query,
            'area': area,
            'per_page': 100,  # Максимальное количество на странице
            'page': 0
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            vacancies = data.get('items', [])

            # Получаем полные описания вакансий
            detailed_vacancies = []
            for vacancy in vacancies[:50]:  # Ограничиваем для скорости
                try:
                    vacancy_detail = self.get_vacancy_detail(vacancy['id'])
                    detailed_vacancies.append(vacancy_detail)
                except Exception as e:
                    print(f"Ошибка при получении деталей вакансии {vacancy['id']}: {e}")
                    detailed_vacancies.append(vacancy)

            return detailed_vacancies

        except requests.RequestException as e:
            print(f"Ошибка при запросе к API hh.ru: {e}")
            return []

    def get_vacancy_detail(self, vacancy_id: str) -> Dict[str, Any]:
        """Получить детальную информацию о вакансии"""
        url = f"{self.base_url}/{vacancy_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()