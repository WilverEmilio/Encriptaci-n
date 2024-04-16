from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import random 
from fastapi import Request, Response
from typing import List
from fastapi import Form
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from .conexion import SessionLocal, engine
from fastapi import FastAPI, Form, Request
from starlette.responses import RedirectResponse
#para poder usar plantillas por medio de Jinja2  
from fastapi.templating import Jinja2Templates

#Lista de palabras asociadas con cada letra del alfabeto
palabras_por_letra = {
    'a': ["abeja", "ardilla", "alce", "armadillo", "alpaca"],
    'b': ["ballena", "buho", "bisonte", "burro", "boa"],
    'c': ["canguro", "caballo", "camello", "cerdo", "cisne"],
    'd': ["delfín", "dingo", "dragón de Komodo", "dromedario", "diablo de Tasmania"],
    'e': ["elefante", "escarabajo", "erizo", "escorpión", "equidna"],
    'f': ["foca", "flamenco", "faisán", "foca", "faisán"],
    'g': ["gorila", "gato", "gacela", "gallina", "ganso"],
    'h': ["hámster", "hipopótamo", "hiena", "halcón", "hormiga"],
    'i': ["iguana", "impala", "insecto palo", "iris", "isopodo"],
    'j': ["jaguar", "jabalí", "jirafa", "jaguarundi", "jerbo"],
    'k': ["koala", "kangaroo rat", "kinkajou", "kudu", "koalas"],
    'l': ["león", "leopardo", "loro", "lémur", "langosta"],
    'm': ["mono", "murciélago", "mapache", "marmota", "mantis"],
    'n': ["nutria", "narval", "naja", "naipe", "negrón"],
    'ñ': ["ñandú"],
    'o': ["orangután", "ornitorrinco", "oso", "ostrero", "oveja"],
    'p': ["panda", "perro", "pingüino", "pulpo", "pez"],
    'q': ["quokka", "quetzal", "quagga", "quirópteros", "quokkas"],
    'r': ["rinoceronte", "ratón", "rana", "rebeco", "rata"],
    's': ["serpiente", "sapo", "salamandra", "saltamontes", "salmonete"],
    't': ["tigre", "tortuga", "topo", "tábano", "tarántula"],
    'u': ["unicornio"],
    'v': ["vaca", "víbora", "vicuña", "visón", "vulpino"],
    'w': ["wallaby", "wombat", "watusi", "walrus", "weimaraner"],
    'x': ["xenopus", "xenoclea", "xerus", "xantolofa", "xifoforo"],
    'y': ["yak", "yegua", "yaguareté", "yaki", "yunque"],
    'z': ["zorro", "zorro volador", "zarigüeya", "zebra", "zorrillo"]
}

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/public", StaticFiles(directory="./public/static"),name = "static") 

templates = Jinja2Templates(directory="./public/templates")

#función para generar la contraseña aletoriamente
def generar_contrasena_aleatoria(texto):
    contrasena_aleatoria = []
    for i, caracter in enumerate(texto):
        if caracter.isalpha():
            letra = caracter.lower()
            if letra in palabras_por_letra:
                contrasena_aleatoria.append(random.choice(palabras_por_letra[letra]))
            else:
                contrasena_aleatoria.append(random.choice(["banana", "coco", "delfín", "elefante", "flor"]))
        elif caracter.isdigit():
            # Convertir el número en palabra
            palabras_numeros = {
                '0': "cero",
                '1': "uno",
                '2': "dos",
                '3': "tres",
                '4': "cuatro",
                '5': "cinco",
                '6': "seis",
                '7': "siete",
                '8': "ocho",
                '9': "nueve"
            }
            numero_letra = palabras_numeros[caracter]
            contrasena_aleatoria.append(numero_letra)
            # Asegurarse de que no se agregue una palabra adicional si hay una letra después del número
            if i < len(texto) - 1 and texto[i + 1].isalpha():
                siguiente_letra = texto[i + 1].lower()
                if siguiente_letra in palabras_por_letra:
                    contrasena_aleatoria.append(random.choice(palabras_por_letra[siguiente_letra]))
        else:
            # Ignorar caracteres no alfabéticos
            continue
    return contrasena_aleatoria

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

#plantilla de login/inicio
@app.get("/", response_class=HTMLResponse) #para ir al modelo de ingreso
def template(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})
#función para ingresar al sistema
@app.post("/")
async def login(request: Request, 
                db: Session = Depends(get_db), 
                username: str = Form(...), 
                password: str = Form(...)):
    print("usuario:", username)
    print("contraseña:", password)
    
    return templates.TemplateResponse("ingreso.html", {"request": request})
    


#plantilla de registro
@app.get("/registro", response_class=HTMLResponse)
def registro(
    request: Request,
    ):
    return templates.TemplateResponse("registro.html", {"request": request})
#fucnón para registrar los datos a la hora de la creación del usuario
@app.post('/registro', response_model=schemas.Crear_Usuario)
async def registro(request: Request, 
                   username: str = Form(...), 
                   password: str = Form(...), 
                   email: str = Form(...),
                   db: Session = Depends(get_db)
                   ):
    user_exist = db.query(models.Registr).filter(models.Registr.usuario == username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    #implementar la encriptación inventada
    password_random = generar_contrasena_aleatoria(password)
    print("Su texto convertido en lista de animales aleatorios es:", password_random)
    password_random_final = ''.join(password_random)
    password_random_final = ''.join(random.choice([letra.lower(), letra.upper()]) for letra in password_random_final)
    print("Su texto convertido en una sola palabra con letras mayúsculas y minúsculas aleatorias es:", password_random_final)
    password_hexadecimal = password_random_final.encode().hex()
    print("Su texto convertido a hexadecimal es:", password_hexadecimal)

    
    new_user = models.Registr(usuario = username, contrasena = password_hexadecimal, correo_electronico = email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print("usuario:", username)
    print("contraseña:", password)
    print("correo:", email)
    
    return templates.TemplateResponse("item.html", {"request": request})

