import requests
from app.core.config import settings

class ApiSigaSigaRest:
    def __init__(self):
        self.base_url = settings.api_sigasiga_rest.URL

    async def validate_and_start_client(self, token: str, ws_id: str):
        json_data = {
        "ws_id": ws_id
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(f"{self.base_url}/streaming/validate_ws_client", json=json_data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False

    async def disconnect_client(self, token, ws_id):
        json_data = {
            "video_source_name": ws_id
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(f"{self.base_url}/streaming/video_source_remove", json=json_data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False