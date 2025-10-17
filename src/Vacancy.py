from typing import List, Dict, Any

class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, title: str, url: str, salary: Dict[str, Any], description: str, requirements: str = ""):
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_description(description)
        self._requirements = requirements

    def _validate_title(self, title: str) -> str:
        """Валидация названия вакансии"""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Валидация URL вакансии"""
        if not url or not isinstance(url, str):
            raise ValueError("URL вакансии должен быть непустой строкой")
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Некорректный URL вакансии")
        return url

    def _validate_salary(self, salary: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация зарплаты"""
        if salary is None:
            return {"from": 0, "to": 0, "currency": "не указана"}

        if not isinstance(salary, dict):
            raise ValueError("Зарплата должна быть словарем")

        validated_salary = {
            "from": salary.get('from') or 0,
            "to": salary.get('to') or 0,
            "currency": salary.get('currency', 'не указана')
        }

        return validated_salary

    def _validate_description(self, description: str) -> str:
        """Валидация описания"""
        if not description or not isinstance(description, str):
            return "Описание отсутствует"
        return description.strip()

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary(self) -> Dict[str, Any]:
        return self._salary

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    def get_average_salary(self) -> float:
        """Получить среднюю зарплату"""
        salary_from = self._salary.get('from', 0) or 0
        salary_to = self._salary.get('to', 0) or 0

        if salary_from and salary_to:
            return (salary_from + salary_to) / 2
        elif salary_from:
            return salary_from
        elif salary_to:
            return salary_to
        else:
            return 0

    def __str__(self) -> str:
        salary_info = "Зарплата не указана"
        if self._salary.get('from') or self._salary.get('to'):
            from_salary = self._salary.get('from', '')
            to_salary = self._salary.get('to', '')
            currency = self._salary.get('currency', '')

            if from_salary and to_salary:
                salary_info = f"{from_salary} - {to_salary} {currency}"
            elif from_salary:
                salary_info = f"от {from_salary} {currency}"
            elif to_salary:
                salary_info = f"до {to_salary} {currency}"

        return (f"Вакансия: {self._title}\n"
                f"Зарплата: {salary_info}\n"
                f"Ссылка: {self._url}\n"
                f"Описание: {self._description[:100]}...")

    def __repr__(self) -> str:
        return f"Vacancy('{self._title}', '{self._url}')"

    # Методы сравнения
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_average_salary() == other.get_average_salary()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_average_salary() < other.get_average_salary()

    def __le__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_average_salary() <= other.get_average_salary()

    def __gt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_average_salary() > other.get_average_salary()

    def __ge__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_average_salary() >= other.get_average_salary()

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List['Vacancy']:
        """Преобразовать JSON данные в список объектов Vacancy"""
        vacancies = []

        for vacancy_data in vacancies_data:
            try:
                # Извлекаем данные из структуры hh.ru
                title = vacancy_data.get('name', '')
                url = vacancy_data.get('alternate_url', '')
                salary = vacancy_data.get('salary')

                # Описание и требования
                description = vacancy_data.get('description', '')
                snippet = vacancy_data.get('snippet', {})
                requirements = snippet.get('requirement', '')

                vacancy = cls(title, url, salary, description, requirements)
                vacancies.append(vacancy)

            except Exception as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать вакансию в словарь"""
        return {
            'title': self._title,
            'url': self._url,
            'salary': self._salary,
            'description': self._description,
            'requirements': self._requirements
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Vacancy':
        """Создать вакансию из словаря"""
        return cls(
            title=data['title'],
            url=data['url'],
            salary=data['salary'],
            description=data['description'],
            requirements=data.get('requirements', '')
        )