import json
import requests


class Transponder():
    
    def __init__(self, report, post_url):
        self.report = report 
        self.post_url = post_url
        self.broadcast()

    def broadcast(self):
        requests.post(url=self.post_url, data=json.dumps(self.report))