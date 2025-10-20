from llms import online_llm
from llms.local_llm import local_llms
from llms.online_llm import online_llms

class LLMs():
    def __init__(self,type: str, model_name: str, model_version: str, api_key: str=None,engine: str=None,base_url: str=None, **kwargs):
        if type == "online":
            self.llm = online_llms(model_name=model_name, model_version=model_version,api_key=api_key)
        elif type == "offline":
            self.llm = local_llms(model_name=model_name, model_version=model_version,engine=engine,base_url=base_url)
        else:
            raise ValueError("Unsupported LLM type")
    def generate_content(self, prompt: list[dict[str,str]]) -> str:
        return self.llm.generate_content(prompt=prompt)