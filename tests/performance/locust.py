from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def showclubsPage(self):
        self.client.get('/clubs')
    
    @task
    def indexPage(self):
        self.client.get('/')
    
    @task
    def showSummaryPage(self):
        self.client.post("/showSummary", {"email":"john@simplylift.co"})
    
    @task
    def purchasePlacesPage(self):
        self.client.post("/purchasePlaces", {"competition":"Fall Classic","club":"Simply Lift","places":2})

    @task
    def bookPage(self):
        self.client.get("/book/Spring Festival/Simply Lift")
    
    @task
    def logoutPage(self):
        self.client.get("logout")