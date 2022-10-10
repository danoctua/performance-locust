import random

from locust import HttpUser, between, task

from utils import auth


class BaseUser(HttpUser):
    headers: dict

    abstract = True
    page_size = 10
    risks = (
        "all-risk",
        "no-risk",
        "current-risk",
        "future-risk",
        # "published"  # disable as we're sure there's a problem with that endpoint currently
    )
    user_name = "planner"
    wait_time = between(10, 60)

    def get_payload(self):
        return {
            "page": random.randint(1, 10),
            "pageSize": self.page_size,
            "unitOfMeasure": "eaches",
            "aggregationLevel": "none",
            "risk": random.choice(self.risks)
        }

    def get_user(self):
        self.client.post(
            "/api/user",
            headers=self.headers
        )

    def get_global_filters(self):
        self.client.get(
            "/api/user/filters",
            headers=self.headers
        )

    def on_start(self):
        user_token = auth.get_sso_token_cached(self.user_name)
        self.headers = {
            "Authorization": f"Bearer {user_token}"
        }


class PlannerUser(BaseUser):

    @task
    def edited(self):
        self.get_user()
        self.get_global_filters()
        payload = self.get_payload()
        self.client.post(
            "/api/risk/report/edited",
            data=payload,
            headers=self.headers,
            name=f"/api/edited/<{payload['risk']}>"
        )
        self.client.post(
            "/api/risk/report/edited/summary",
            data=payload,
            headers=self.headers,
            name=f"/api/edited/summary/<{payload['risk']}>"
        )


class CommercialUser(BaseUser):
    @task
    def real_time(self):
        self.get_user()
        self.get_global_filters()
        payload = self.get_payload()
        self.client.post(
            "/api/risk/report/commercial",
            headers=self.headers,
            data=payload,
            name=f"/api/commercial/<{payload['risk']}>"
        )
