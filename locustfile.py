from locust import HttpUser, task, between

class DashAppUser(HttpUser):
    wait_time = between(1, 5)  # Интервал между запросами (в секундах)

    @task
    def fetch_grades_data(self):
        # Эмулируем запрос к API для получения данных оценок
        self.client.get("http://localhost:8000/grades/", name="Fetch Grades Data")

    @task(3)  # Этот запрос будет выполняться в 3 раза чаще
    def load_dashboard(self):
        # Эмулируем загрузку главной страницы Dash-приложения
        self.client.get("/", name="Load Dashboard")