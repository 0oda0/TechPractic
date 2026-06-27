from locust import HttpUser, task, between

class SearchUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def search(self):
        self.client.get("/api/v1/search?q=test")