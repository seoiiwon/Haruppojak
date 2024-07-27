import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

query = "살려줘.. 너무 피곤해"

messages =[{
    "role" : "system",
    "content" : "너는 매우 유능한 심리상담가야. 사용자의 말에 반응 해줘. 한국어로 대답부탁해."
}, {
    "role" : "user",
    "content" : query
}]

completion = openai.chat.completions.create(model=model, messages=messages)
print(completion.choices[0].message.content)


