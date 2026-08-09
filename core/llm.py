import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found")

client = InferenceClient(
    api_key=HF_TOKEN
)

class HuggingFaceLLM:

    def invoke(self, prompt):

        response = client.chat.completions.create(

            model="Qwen/Qwen2.5-7B-Instruct",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            max_tokens=1024

        )

        class Result:

            content = response.choices[0].message.content

        return Result()

llm = HuggingFaceLLM()