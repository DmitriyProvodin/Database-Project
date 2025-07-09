import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def insert_employer_and_vacancies(employer_name: str, vacancies: list):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO employers (name) VALUES (%s) RETURNING id;", (employer_name,))
            employer_id = cur.fetchone()[0]

            for vac in vacancies:
                cur.execute("""
                    INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url)
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    employer_id,
                    vac['name'],
                    vac['salary']['from'] if vac['salary'] else None,
                    vac['salary']['to'] if vac['salary'] else None,
                    vac['alternate_url']
                ))
    conn.close()
