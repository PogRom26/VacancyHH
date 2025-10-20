import json
import os
from typing import Any, Dict, List

from src.vacancy import Vacancy
from src.vacancy_storage import VacancyStorage


class JSONSaver(VacancyStorage):
    """Класс для сохранения вакансий в JSON файл в папку data"""

    def __init__(self, filename: str = "vacancies.json"):
        # Создаем путь к файлу в папке data
        self.data_dir = "data"
        self.filename = os.path.join(self.data_dir, filename)
        self._ensure_data_dir_exists()
        self._ensure_file_exists()

    def _ensure_data_dir_exists(self) -> None:
        """Создать папку data, если она не существует"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Создана папка {self.data_dir}")

    def _ensure_file_exists(self) -> None:
        """Создать файл, если он не существует"""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)
            print(f"Создан файл {self.filename}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в JSON файл"""
        vacancies = self._load_vacancies()

        # Проверяем, нет ли уже такой вакансии по URL (более надежный критерий)
        for v in vacancies:
            if v["url"] == vacancy.url:
                print(f"Вакансия уже существует: {vacancy.title}")
                return  # Вакансия уже существует

        vacancies.append(vacancy.to_dict())
        self._save_vacancies(vacancies)
        print(f"Вакансия добавлена: {vacancy.title}")

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Добавить список вакансий в JSON файл"""
        existing_vacancies = self._load_vacancies()
        existing_urls = {v["url"] for v in existing_vacancies}

        new_vacancies = []
        for vacancy in vacancies:
            if vacancy.url not in existing_urls:
                new_vacancies.append(vacancy.to_dict())
                existing_urls.add(
                    vacancy.url
                )  # Добавляем чтобы избежать дубликатов в этом вызове

        if new_vacancies:
            all_vacancies = existing_vacancies + new_vacancies
            self._save_vacancies(all_vacancies)
            print(f"Добавлено {len(new_vacancies)} новых вакансий в {self.filename}")
        else:
            print("Нет новых вакансий для добавления")

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Vacancy]:
        """Получить вакансии по критериям"""
        vacancies_data = self._load_vacancies()

        # Отладочная информация
        print(f"Загружено {len(vacancies_data)} вакансий из файла {self.filename}")

        try:
            vacancies = [Vacancy.from_dict(data) for data in vacancies_data]
        except Exception as e:
            print(f"Ошибка при создании объектов Vacancy: {e}")
            return []

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            matches = True

            # Фильтрация по ключевым словам в описании
            if "keyword" in criteria and criteria["keyword"]:
                keyword = criteria["keyword"].lower()
                vacancy_text = f"{vacancy.title} {vacancy.description} {vacancy.requirements}".lower()
                if keyword not in vacancy_text:
                    matches = False

            # Фильтрация по минимальной зарплате
            if "min_salary" in criteria and criteria["min_salary"]:
                if vacancy.get_average_salary() < criteria["min_salary"]:
                    matches = False

            # Фильтрация по максимальной зарплате
            if "max_salary" in criteria and criteria["max_salary"]:
                if vacancy.get_average_salary() > criteria["max_salary"]:
                    matches = False

            if matches:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из JSON файла"""
        vacancies = self._load_vacancies()
        initial_count = len(vacancies)

        vacancies = [v for v in vacancies if v["url"] != vacancy.url]

        if len(vacancies) < initial_count:
            self._save_vacancies(vacancies)
            print(f"Вакансия удалена: {vacancy.title}")
        else:
            print("Вакансия не найдена для удаления")

    def clear(self) -> None:
        """Очистить JSON файл"""
        self._save_vacancies([])
        print(f"Файл {self.filename} очищен")

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загрузить вакансии из файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    print("Ошибка: данные в файле не являются списком")
                    return []
                return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Ошибка при загрузке файла {self.filename}: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке файла: {e}")
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Сохранить вакансии в файл"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
            print(f"Сохранено {len(vacancies)} вакансий в файл {self.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении в файл {self.filename}: {e}")

    def print_all_vacancies(self) -> None:
        """Вывести все вакансии из файла (для отладки)"""
        vacancies = self.get_vacancies()
        if not vacancies:
            print(f"В файле {self.filename} нет вакансий")
            return

        print(f"\nВсе вакансии в файле {self.filename} ({len(vacancies)}):")
        for i, vacancy in enumerate(vacancies, 1):
            salary_info = "не указана"
            if vacancy.salary.get("from") or vacancy.salary.get("to"):
                from_salary = vacancy.salary.get("from", "")
                to_salary = vacancy.salary.get("to", "")
                currency = vacancy.salary.get("currency", "")

                if from_salary and to_salary:
                    salary_info = f"{from_salary}-{to_salary} {currency}"
                elif from_salary:
                    salary_info = f"от {from_salary} {currency}"
                elif to_salary:
                    salary_info = f"до {to_salary} {currency}"

            print(f"{i}. {vacancy.title} | Зарплата: {salary_info} | {vacancy.url}")

    def get_file_info(self) -> Dict[str, Any]:
        """Получить информацию о файле"""
        try:
            file_size = (
                os.path.getsize(self.filename) if os.path.exists(self.filename) else 0
            )
            vacancies_count = len(self._load_vacancies())

            return {
                "filename": self.filename,
                "file_size_bytes": file_size,
                "file_size_kb": round(file_size / 1024, 2),
                "vacancies_count": vacancies_count,
                "file_exists": os.path.exists(self.filename),
            }
        except Exception as e:
            return {"filename": self.filename, "error": str(e)}
