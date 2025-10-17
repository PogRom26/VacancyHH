from src import Vacancy
from src.HeadHunterAPI import HeadHunterAPI
from src.JSONSaver import JSONSaver
from typing import List, Dict, Any


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтровать вакансии по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = f"{vacancy.title} {vacancy.description} {vacancy.requirements}".lower()
        if any(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтровать вакансии по диапазону зарплат"""
    if not salary_range or salary_range.strip() == "":
        return vacancies

    try:
        # Ожидаем формат: "100000-150000" или "100000 - 150000"
        range_parts = salary_range.replace(' ', '').split('-')
        if len(range_parts) != 2:
            return vacancies

        min_salary = int(range_parts[0])
        max_salary = int(range_parts[1])

        filtered = []
        for vacancy in vacancies:
            avg_salary = vacancy.get_average_salary()
            if min_salary <= avg_salary <= max_salary:
                filtered.append(vacancy)

        return filtered

    except ValueError:
        print("Некорректный формат диапазона зарплат")
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировать вакансии по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получить топ N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывести вакансии в консоль"""
    if not vacancies:
        print("Вакансии не найдены")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'=' * 50}")
        print(f"Вакансия #{i}")
        print(f"{'=' * 50}")
        print(vacancy)
        print(f"{'=' * 50}")


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("Добро пожаловать в программу поиска вакансий!")
    print("=" * 50)

    # Создаем экземпляры классов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    # Ввод данных от пользователя
    search_query = input("Введите поисковый запрос: ").strip()

    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    except ValueError:
        print("Некорректное число, будет использовано значение по умолчанию: 10")
        top_n = 10

    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ").strip()

    print("\nИщем вакансии...")

    # Получение вакансий
    hh_vacancies_data = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)

    if not vacancies_list:
        print("Вакансии по вашему запросу не найдены")
        return

    # Сохранение в файл
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    print(f"Найдено {len(vacancies_list)} вакансий")

    # Фильтрация и сортировка
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    print(f"После фильтрации по ключевым словам: {len(filtered_vacancies)} вакансий")

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    print(f"После фильтрации по зарплате: {len(ranged_vacancies)} вакансий")

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод результатов
    print(f"\nТоп {len(top_vacancies)} вакансий:")
    print_vacancies(top_vacancies)

    # Дополнительные возможности
    while True:
        print("\nДополнительные возможности:")
        print("1 - Показать все сохраненные вакансии")
        print("2 - Поиск по ключевому слову в сохраненных вакансиях")
        print("3 - Очистить файл с вакансиями")
        print("0 - Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            all_vacancies = json_saver.get_vacancies()
            print_vacancies(all_vacancies)

        elif choice == "2":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            found_vacancies = json_saver.get_vacancies({"keyword": keyword})
            print(f"Найдено {len(found_vacancies)} вакансий:")
            print_vacancies(found_vacancies)

        elif choice == "3":
            json_saver.clear()
            print("Файл с вакансиями очищен")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Некорректный выбор")