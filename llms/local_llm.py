import requests
import re

class local_llms():
    def __init__(self,engine:str, model_version: str, base_url: str =None, **kwargs):
        self.engine = engine
        self.model_version = model_version
        self.client = None
        self.max_token = kwargs.get("max_token", 4096)
        if engine == "ollama":
            self.base_url = base_url
            self.init_ollama(model_version)
        elif engine == "vllm":
            self.base_url = base_url
            self.init_vllm(model_version)
        else:
            raise ValueError(f"Unsupported engine: {engine}")
    def init_ollama(self, model_version:str):
        try:
            response = requests.get(self.base_url,timeout=5)
            response.raise_for_status()
            print("Connected to OLLAMA")
            self.client = requests.Session()
            self.pull_ollama(model_version)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Can't connect to OLLAMA at {self.base_url}")
    def pull_ollama(self, model_version:str):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models",[])
            model_exist = any(model_version in m["name"] for m in models)

            if not model_exist:
                print(f"Model {model_version} not found. Starting download")
                pull_data = {"name":model_version}
                pull_response = self.client.post(f"{self.base_url}/api/pull", json=pull_data)
                pull_response.raise_for_status()
                print(f"Downloaded {model_version}")
            else:
                print(f"Model {model_version} is exist")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error with API's Ollama {e}")
    def init_vllm(self, model_version:str):
        pass
    def generate_content(self,prompt: list[dict[str,str]]) ->str:
        if not self.client:
            raise RuntimeError("Not found Client. Please initialize client first")
        try:
            if self.engine == "ollama":
                payload = {
                    "model": self.model_version,
                    "messages": prompt,
                    "stream": False
                }
                response = self.client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                response_data = response.json()["message"]["content"].strip()
                return response_data
        except Exception as e:
            print(f"Having errors {e}")
            raise
