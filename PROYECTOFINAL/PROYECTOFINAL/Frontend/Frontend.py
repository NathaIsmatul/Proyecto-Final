from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
from fastapi.responses import RedirectResponse
import os


app = FastAPI()

# Configura las plantillas y los archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")#enviamos un inicio de sesion
async def get_login(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

# ----------------------------------- LOGIN --------------------------------- 
@app.post("/login_datos")
async def post_login_frontend(request: Request, nombre: str = Form(...), contrasena: str = Form(...)):
    # Crear un diccionario con los datos   
    data = {
        'nombre': nombre,
        'contrasena': contrasena
    }

    async with httpx.AsyncClient() as client:#para redirigirse_api
        response = await client.post("http://localhost:5005/verificacion_datos", json=data)

    if response.status_code == 200:
        response_data = response.json()
        user_id = response_data.get("user_id")
        menu_options = response_data.get("menu_options")

        # Redirigir al HTML correspondiente según el ID del usuario
        if user_id == 201:
            return templates.TemplateResponse("Usuario-index.html", {"request": request, "menu_options": menu_options})
        elif user_id == 101:
            return templates.TemplateResponse("Admin-index.html", {"request": request, "menu_options": menu_options})
        else:
            # Si el ID del usuario no es 201 o 101, puedes manejar este caso de alguna manera
            return templates.TemplateResponse("Login.html", {"request": request})
    else:
        return templates.TemplateResponse("Login.html", {"request": request})

# ----------------------------------- CASTRACION --------------------------------- 
# GET para traer datos
@app.get("/Castracion_datos")
async def get_Castracion_datos(request: Request):
    # Realiza una solicitud al backend Flask para obtener los datos de Oracle
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:5005/recibir_Castraciones')

    if response.status_code == 200:
        castracion_data = response.json()
        return templates.TemplateResponse("Admin-Castracion.html", {"request": request, "castracion_data": castracion_data})
    else:
        return templates.TemplateResponse("Admin-Castracion.html", {"request": request})
    

# ----------------------------------- REGISTRAR  --------------------------------- 
# GET para traer datos
@app.get("/Registrar_datos")
async def get_Castracion_datos(request: Request):
    # Realiza una solicitud al backend Flask para obtener los datos de Oracle
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:5005/registrar_Mascotas')

    if response.status_code == 200:
        registro_data = response.json()
        return templates.TemplateResponse("Admin-Registrar.html", {"request": request, "registro_data": registro_data})
    else:
        return templates.TemplateResponse("Admin-Registrar.html", {"request": request})
    
# ----------------------------------- CATALOGO --------------------------------- 
# GET para traer datos
@app.get("/Catalogo_datos")
async def get_Catalogo_datos(request: Request):
    # Realiza una solicitud a la API Flask para obtener los datos de Oracle
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:5005/obtener_Catalogo')

    if response.status_code == 200:
        catalogo_data = response.json()

        # Busca una imagen para cada mascota
        for mascota in catalogo_data:
            nombre = mascota['nombreMascota'].split()[0].lower()
            imagen_url = await buscar_imagen(nombre)
            mascota['imagen_url'] = imagen_url

        return templates.TemplateResponse("Admin-Adopciones.html", {"request": request, "catalogo_data": catalogo_data})
    else:
        return templates.TemplateResponse("Admin-Adopciones.html", {"request": request})

async def buscar_imagen(nombre):
    # Busca una imagen local
    imagen_nombre = f'{nombre}.jpg'
    imagen_path = os.path.join('static/images', imagen_nombre)
    if os.path.exists(imagen_path):
        return f"/{imagen_path}"  # Agrega una barra para formar la ruta completa
    else:
        return None
    
# ----------------------------------- Insertar registro --------------------------------- 
import json
from fastapi import FastAPI, Request, HTTPException, Form

@app.post("/Registrar_mascota")
async def registrar_mascota(request: Request, 
                            nombreMascota: str = Form(...),
                            raza: str = Form(...),
                            edad: int = Form(...),
                            descripcion: str = Form(...)):
    
    # Crear un diccionario con los datos
    mascota_data = {
        'nombreMascota': nombreMascota,
        'raza': raza,
        'edad': edad,
        'descripcion': descripcion
    }

    # Convierte los datos a JSON
    mascota_json = json.dumps(mascota_data)

    # Realiza una solicitud al backend Flask para insertar la orden
    async with httpx.AsyncClient() as client:
        response = await client.post('http://localhost:5005/Insertar_registro_mascota', json=mascota_json)

        if response.status_code == 200:
            return print('Producto agregado al carrito correctamente')
        else:
            raise HTTPException(status_code=500, detail='Error al agregar el producto al carrito')
