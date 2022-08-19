from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(0, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/show_summary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get(f"/book/Spring Classic/Simply Lift")

    @task
    def purchase_places(self):
        data = {
            "competition": "Spring Classic",
            "club": "Simply Lift",
            "places": 1,
        }

        self.client.post("/purchase_places", data=data)

    @task
    def logout(self):
        self.client.get("/logout")

    @task
    def index(self):
        self.client.get("/clubs_points")
