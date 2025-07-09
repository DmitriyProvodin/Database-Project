import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id)
                FROM employers e
                JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL;")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT title, salary_from, url
                FROM vacancies
                WHERE salary_from > %s;
            """, (avg,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT title, url
                FROM vacancies
                WHERE LOWER(title) LIKE %s;
            """, (f"%{keyword.lower()}%",))
            return cur.fetchall()
