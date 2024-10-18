from locust import HttpUser, task, between

class StreamlitUser(HttpUser):
    wait_time = between(1, 5)  # Time between tasks for each simulated user

    @task
    def load_page(self):
        self.client.get("/")  # This simulates accessing your app's home page
