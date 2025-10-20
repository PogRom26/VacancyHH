from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получить вакансии по поисковому запросу"""
        pass
