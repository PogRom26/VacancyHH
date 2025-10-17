import json, os


from src import Vacancy
from src.VacancyStorage import VacancyStorage
from typing import List, Dict, Any
from src.Vacancy import Vacancy




class JSONSaver(VacancyStorage):
    """Класс для сохранения вакансий в JSON файл"""

    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создать файл, если он не существует"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в JSON файл"""
        vacancies = self._load_vacancies()

        # Проверяем, нет ли уже такой вакансии
        for v in vacancies:
            if (v['title'] == vacancy.title and
                    v['url'] == vacancy.url and
                    v['salary'] == vacancy.salary):
                return  # Вакансия уже существует

        vacancies.append(vacancy.to_dict())
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Vacancy]:
        """Получить вакансии по критериям"""
        vacancies_data = self._load_vacancies()
        vacancies = [Vacancy.from_dict(data) for data in vacancies_data]

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            matches = True

            # Фильтрация по ключевым словам в описании
            if 'keyword' in criteria:
                keyword = criteria['keyword'].lower()
                if (keyword not in vacancy.description.lower() and
                        keyword not in vacancy.requirements.lower() and
                        keyword not in vacancy.title.lower()):
                    matches = False

            # Фильтрация по зарплате
            if 'min_salary' in criteria:
                if vacancy.get_average_salary() < criteria['min_salary']:
                    matches = False

            if matches:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из JSON файла"""
        vacancies = self._load_vacancies()

        vacancies = [v for v in vacancies if not (
                v['title'] == vacancy.title and
                v['url'] == vacancy.url and
                v['salary'] == vacancy.salary
        )]

        self._save_vacancies(vacancies)

    def clear(self) -> None:
        """Очистить JSON файл"""
        self._save_vacancies([])

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузить вакансии из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Сохранить вакансии в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)