from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse

VIEWS_PATH = "./src/application_root/views"

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    with open(f"{VIEWS_PATH}/index.html", "r", encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content, status_code=200)