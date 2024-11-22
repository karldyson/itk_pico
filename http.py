import urequests

class Http:

    def get(self, url: str):
        response = urequests.get(url)
        text = response.text
        response.close()
        print(f"Received: {text}")
        return text

    def post(self, url: str, data):
        response = urequests.post(url, json=data)
        text = response.text
        print(f" Received: {text}")
        response.close()
        return text