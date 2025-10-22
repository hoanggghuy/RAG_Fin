from llms import llms, local_llm,online_llm
from llms.llms import LLMs
def main():
    llm = LLMs(type="offline", model_name="ollama",model_version="gemma3:4b",engine="ollama",base_url="http://localhost:11434")
    llm = LLMs(type="online", model_name="openai", model_version="gpt-5-nano",api_key="api_key")
    chat_prompt = [
        {
            "role": "user",
            "content": "Hôm nay là ngày bao nhiêu ?"
        }
    ]
    result = llm.generate_content(prompt=chat_prompt)
    return result

if __name__ == "__main__":
    print(main())
