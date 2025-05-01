from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import base64
import os

app = FastAPI()

# Разрешаем запросы с основного домена и (по желанию) с доменов Тильды
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://siriusfuture.ru",
        "https://www.siriusfuture.ru",
        # Если нужно — и поддомены:
        # "https://*.siriusfuture.ru",

        # Опционально: для Тильды
        "https://*.tilda.ws",
        "https://tilda.cc",
        "https://static.tildacdn.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    try:
        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Ты ведущий нейропсихолог с опытом работы 20 лет. Проведи оценку проективных методик ребенка по рисунку"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
        )

        analysis = response.choices[0].message.content
        print (analysis)
        return JSONResponse(content={"analysis": analysis})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки запроса: {e}")
