from db_creator import create_tables
from api import get_employer_vacancies
from data_loader import insert_employer_and_vacancies
from db_manager import DBManager

def main():
    create_tables()

    employers = {
        "Яндекс": 1740,
        "Сбер": 3529,
        "Ozon": 2180,
        "VK": 15478,
        "Тинькофф": 78638,
        "Альфа-Банк": 80,
        "Лаборатория Касперского": 98,
        "Skyeng": 1122462,
        "МТС": 3776,
        "Газпром нефть": 39305
    }

    for name, eid in employers.items():
        vacancies = get_employer_vacancies(eid)
        insert_employer_and_vacancies(name, vacancies)

    db = DBManager()

    print("Компании и количество вакансий:")
    for row in db.get_companies_and_vacancies_count():
        print(row)

    print("\nВакансии:")
    for row in db.get_all_vacancies():
        print(row)

    print("\nСредняя зарплата:")
    print(db.get_avg_salary())

    print("\nВакансии с ЗП выше средней:")
    for row in db.get_vacancies_with_higher_salary():
        print(row)

    print("\nВакансии по ключевому слову 'python':")
    for row in db.get_vacancies_with_keyword("python"):
        print(row)

if __name__ == "__main__":
    main()
