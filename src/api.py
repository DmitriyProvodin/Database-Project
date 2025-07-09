import requests

def get_employer_vacancies(employer_id: int) -> list:
    url = "https://api.hh.ru/vacancies"
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("items", [])
