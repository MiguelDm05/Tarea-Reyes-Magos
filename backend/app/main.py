# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db import SessionLocal, engine
from models import Base, ReyMago, Usuario, Juguete, Carta
from schemas import (UsuarioCreate, UsuarioBase,
                     ReyMagoCreate, JugueteCreate, JugueteBase,
                     CartaCreate, ReyMagoBase, ReyMagoCreate,
                     CartaBase)
import crud
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Permitir solicitudes CORS desde cualquier origen (ajustable según tus necesidades)
app.add_middleware(
    CORSMiddleware,
    # Permite todos los orígenes, o reemplaza con una lista específica como ["http://localhost"]
    allow_origins=["*", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

Base.metadata.create_all(bind=engine)

# Dependency para obtener el DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas para Usuario


@app.post("/usuarios/", response_model=UsuarioCreate)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)


@app.get("/usuarios/", response_model=List[UsuarioBase])
def get_usuarios(db: Session = Depends(get_db)):
    return crud.get_usuarios(db)

# Endpoint para obtener un Usuario por su nombre
# Endpoint para eliminar un usuario por ID


@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        usuario_eliminado = crud.delete_usuario(db, usuario_id)
        return {"msg": f"Usuario con ID {usuario_id} ha sido eliminado", "usuario": usuario_eliminado}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el usuario: {str(e)}")


@app.get("/usuarios/{nombre}")
def get_usuario_nombre(nombre: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.nombre == nombre).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Rey Mago no encontrado")
    return usuario


# Rutas para ReyMago
@app.post("/reyes_magos/", response_model=ReyMagoCreate)
def create_rey_mago(rey_mago: ReyMagoCreate, db: Session = Depends(get_db)):
    return crud.create_rey_mago(db=db, rey_mago=rey_mago)


@app.get("/reyes_magos/", response_model=List[ReyMagoBase])
def get_reyes_magos(db: Session = Depends(get_db)):
    return crud.get_reyes_magos(db)


# Endpoint para obtener un Rey Mago por su nombre
@app.get("/reyes_magos/{nombre}")
def get_rey_mago(nombre: str, db: Session = Depends(get_db)):
    rey_mago = db.query(ReyMago).filter(
        ReyMago.nombre == nombre).first()
    if rey_mago is None:
        raise HTTPException(status_code=404, detail="Rey Mago no encontrado")
    return rey_mago


@app.delete("/reyes_magos/{rey_mago_id}")
def eliminar_rey_mago(rey_mago_id: int, db: Session = Depends(get_db)):
    try:
        rey_eliminado = crud.delete_rey_mago(db, rey_mago_id)
        return {"msg": f"Rey con ID {rey_mago_id} ha sido eliminado", "rey": rey_eliminado}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el usuario: {str(e)}")


# Rutas para Juguete


@app.post("/juguetes/", response_model=JugueteCreate)
def create_juguete(juguete: JugueteCreate, db: Session = Depends(get_db)):
    return crud.create_juguete(db=db, juguete=juguete)


@app.get("/juguetes/", response_model=List[JugueteBase])
def get_juguetes(db: Session = Depends(get_db)):
    return crud.get_juguetes(db)


# Endpoint para obtener un Rey Mago por su nombre
@app.get("/juguetes/{nombre}")
def get_juguete_nombre(nombre: str, db: Session = Depends(get_db)):
    juguete = db.query(Juguete).filter(
        Juguete.nombre == nombre).first()
    if juguete is None:
        raise HTTPException(status_code=404, detail="Juguete no encontrado")
    return juguete


# Endpoint para obtener un Rey Mago por su nombre
@app.get("/juguetes/{id}")
def get_juguete_id(id: str, db: Session = Depends(get_db)):
    juguete = db.query(Juguete).filter(
        Juguete.id == id).first()
    if juguete is None:
        raise HTTPException(status_code=404, detail="Juguete no encontrado")
    return juguete


@app.delete("/juguetes/{juguete_id}")
def eliminar_juguete(juguete_id: int, db: Session = Depends(get_db)):
    try:
        juguete_eliminado = crud.delete_juguete(db, juguete_id)
        return {"msg": f"Juguete con ID {juguete_id} ha sido eliminado", "juguete": juguete_eliminado}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="juguete no encontrado")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el juguete: {str(e)}")


# Rutas para Carta

@app.post("/cartas/", response_model=CartaCreate)
def create_carta(carta: CartaCreate, db: Session = Depends(get_db)):
    print("************************")
    return crud.create_carta(db=db, carta_create=carta)


@app.get("/cartas/", response_model=List[CartaBase])
def get_cartas(db: Session = Depends(get_db)):
    return crud.get_cartas(db)


@app.get("/cartas/{id}")
def get_cartas_por_usuario(id: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.id == id).first()
    cartas = db.query(Carta).filter(
        Carta.usuario == usuario)
    response_data ={'result': []}
    for carta in cartas:
        
        response_data['result'].append({
            "id": carta.id,
            "usuario_id": carta.usuario_id,
            "rey_mago_id": carta.rey_mago_id,
            # Agregar los IDs de los juguetes
            "juguetes_ids": [{"id": j.id, "nombre": j.nombre, "imagen": j.imagen} for j in carta.juguetes]
        })
    if carta is None:
        raise HTTPException(status_code=404, detail="Juguete no encontrado")
    return response_data



@app.delete("/cartas/{carta_id}")
def eliminar_carta(carta_id: int, db: Session = Depends(get_db)):
    try:
        carta_eliminada = crud.delete_carta(db, carta_id)
        return {"msg": f"Carta con ID {carta_id} ha sido eliminado", "Carta": carta_eliminada}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="carta no encontrado")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el Carta: {str(e)}")
