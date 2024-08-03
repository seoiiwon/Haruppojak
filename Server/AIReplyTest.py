import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

query = "너무 불안해. 내가 과연 시험에 붙을 수 있을까? 매일 저녁시간에 자격증을 공부했지만, 막상 떨어질 것 같아 잠을 못자겠어."

messages =[{
    "role" : "system",
    "content" : "너는 매우 유능한 심리상담가야. 사용자의 말에 반응 해줘. 한국어로 대답부탁해. 친근한 말로 사용자의 일기에 공감하고 위로의 말을 건네줘. 때론 사용자의 고민에 해결책을 제시해줘."
}, {
    "role" : "user",
    "content" : query
}]

completion = openai.chat.completions.create(model=model, messages=messages)
print(completion.choices[0].message.content)


