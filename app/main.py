from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi import Request, Response

#para poder usar plantillas por medio de Jinja2  
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/public", StaticFiles(directory="./public/static"),name = "static") 

templates = Jinja2Templates(directory="./public/templates")


#metodo para utilizar el html sin templates
# @app.get("/", response_class=HTMLResponse)
# def root():
#     udicacion_plantilla = os.path.abspath("./public/static/html/index.html")
#     return FileResponse(udicacion_plantilla, status_code=200)

#utilizar el metodo html con templates
@app.get("/", response_class=HTMLResponse)
def template(response: Response, request: Request):
    return templates.TemplateResponse("item.html", {"request": request})

@app.get("/registro", response_class=HTMLResponse)
def registro(response: Response, request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})
