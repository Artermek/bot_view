import base64
from openai import OpenAI

base64_image = 1

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Ты ведущий нейропсихолог с опытом работы 20 лет. Можешь провести оценку проективных методик ребенка по рисунку?",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)

print(response.choices[0])