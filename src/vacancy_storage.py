from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Vacancy]:
        """Получить вакансии по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из хранилища"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистить хранилище"""
        pass
