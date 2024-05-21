from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse

from models.model import predict_pretrained

VIEWS_PATH = "./src/application_root/views"

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    with open(f"{VIEWS_PATH}/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content, status_code=200)


@app.post("/predict/")
async def predict(text: str = Body(embed=True)):
    return predict_pretrained(text)
