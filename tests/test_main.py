import unittest
import tempfile
import os

from src.HeadHunterAPI import HeadHunterAPI
from src.JSONSaver import JSONSaver
from src.Vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def setUp(self):
        self.sample_salary = {"from": 100000, "to": 150000, "currency": "RUR"}
        self.vacancy1 = Vacancy("Python Developer", "https://hh.ru/vacancy/1",
                                self.sample_salary, "Разработка на Python", "Опыт 3 года")
        self.vacancy2 = Vacancy("Java Developer", "https://hh.ru/vacancy/2",
                                {"from": 120000, "to": None, "currency": "RUR"},
                                "Разработка на Java", "Опыт 2 года")

    def test_vacancy_creation(self):
        self.assertEqual(self.vacancy1.title, "Python Developer")
        self.assertEqual(self.vacancy1.url, "https://hh.ru/vacancy/1")
        self.assertEqual(self.vacancy1.salary, self.sample_salary)

    def test_salary_validation(self):
        vacancy_no_salary = Vacancy("Test", "https://test.com", None, "Desc")
        self.assertEqual(vacancy_no_salary.salary["from"], 0)
        self.assertEqual(vacancy_no_salary.salary["to"], 0)

    def test_comparison(self):
        self.assertTrue(self.vacancy2 > self.vacancy1)  # 120000 > 125000? Нет, 125000 > 120000
        self.assertTrue(self.vacancy1 > self.vacancy2)  # Исправлено

    def test_average_salary(self):
        self.assertEqual(self.vacancy1.get_average_salary(), 125000)
        self.assertEqual(self.vacancy2.get_average_salary(), 120000)


class TestHeadHunterAPI(unittest.TestCase):

    def setUp(self):
        self.api = HeadHunterAPI()

    def test_api_initialization(self):
        self.assertEqual(self.api.base_url, "https://api.hh.ru/vacancies")

    def test_get_vacancies(self):
        vacancies = self.api.get_vacancies("Python", area=1)
        self.assertIsInstance(vacancies, list)


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.saver = JSONSaver(self.temp_file.name)
        self.vacancy = Vacancy("Test", "https://test.com",
                               {"from": 100000, "to": 150000, "currency": "RUR"},
                               "Test description")

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_add_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Test")

    def test_delete_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.delete_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 0)

