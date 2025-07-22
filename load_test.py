from locust import HttpUser, task, between

class CalendarUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def login(self):
        self.client.post("/login", json={"username": "test", "password": "Pass123!"})

    @task
    def signup(self):
        self.client.post("/signup", json={"username": "test", "password": "Pass123!"})

    @task
    def create_event(self):
        self.client.post("/calendar", json={
            "title": "Meeting",
            "start": "2025-07-24T10:00:00",
            "end": "2025-07-24T11:00:00"
        })

    @task
    def chatbot(self):
        self.client.post("/chatbot", json={
            "title": "Meeting",
            "start": "2025-07-24T10:00:00",
            "end": "2025-07-24T11:00:00"
        })

    @task
    def analysis(self):
        self.client.post("/analysis", json={
            "title": "Meeting",
            "start": "2025-07-24T10:00:00",
            "end": "2025-07-24T11:00:00"
        })
    @task
    def settings(self):
        self.client.post("/settings", json={
            "title": "Meeting",
            "start": "2025-07-24T10:00:00",
            "end": "2025-07-24T11:00:00"
        })