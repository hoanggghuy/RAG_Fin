import openai
import requests
import google.generativeai as genai
class online_llms:
    def __init__(self,model_name:str, model_version:str, api_key:str):
        self.model_name = model_name.lower()
        self.model_version = model_version
        if self.model_name == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif self.model_name == "gemini":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name=model_version)
        else:
            raise ValueError("Invalid model name or missing APIkey")
    def generate_content(self, prompt: list[dict[str,str]]) -> str:
        if self.model_name == "gemini":
            gemini_message = [
                {{"role": msg["role"], "parts": [msg["content"]]} for msg in prompt}
            ]
            response = self.model.generate_content(gemini_message)
            try:
                return response.text
            except:
                return response.candidates[0].content.parts[0].text
        elif self.model_name == "openai":
            response = self.client.chat.completions.create(
                model = self.model_version,
                messages=prompt,
            )
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unsupported model name {self.model_name}")
