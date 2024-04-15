from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/public", StaticFiles(directory="./public/static"),name = "static") 

@app.get("/", response_class=HTMLResponse)
def root():
    udicacion_plantilla = os.path.abspath("./public/static/html/index.html")
    return FileResponse(udicacion_plantilla, status_code=200)