from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from models.model import predict_pretrained

VIEWS_PATH = "./application_root/views"

app = FastAPI()

app.mount("/static", StaticFiles(directory="application_root/static"))


@app.get("/", include_in_schema=False)
async def root():
    with open(f"{VIEWS_PATH}/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content, status_code=200)


@app.post("/predict/")
async def predict(
    text: str = Body(
        embed=True,
        title="Текст",
        description="""Текст для классификации ESG
             (экологических, социальных и управленческих) рисков
             из текстовых данных""",
    )
):
    """Основной запрос приложения. Выдает логиты для нескольких
    категорий ESG-рисков, которые затем преобразуются в
    вероятности с помощью сигмоидной функции активации.
    """
    return predict_pretrained(text)
