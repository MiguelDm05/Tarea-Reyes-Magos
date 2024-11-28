# crud.py
from sqlalchemy.orm import Session
from models import Usuario, ReyMago, Juguete, Carta
from schemas import UsuarioCreate, ReyMagoCreate, JugueteCreate, CartaCreate
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
# Usuario CRUD


def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

# Función para eliminar un usuario por ID


def delete_usuario(db: Session, usuario_id: int):
    try:
        # Buscar al usuario en la base de datos usando su id
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        # Si no se encuentra el usuario, lanzamos una excepción
        if usuario is None:
            raise NoResultFound("Usuario no encontrado")

        # Si el usuario existe, lo eliminamos
        db.delete(usuario)  # Marcamos el objeto para eliminarlo
        db.commit()  # Confirmamos la transacción
        return usuario  # Devolvemos el usuario eliminado (opcional)

    except NoResultFound as e:
        raise e  # Lanza una excepción si no se encuentra el usuario
    except Exception as e:
        db.rollback()  # Hacemos rollback si ocurre algún error
        raise e  # Lanza cualquier otro error

# ReyMago CRUD


def create_rey_mago(db: Session, rey_mago: ReyMagoCreate):
    db_rey_mago = ReyMago(**rey_mago.dict())
    db.add(db_rey_mago)
    db.commit()
    db.refresh(db_rey_mago)
    return db_rey_mago


def get_reyes_magos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReyMago).offset(skip).limit(limit).all()


def delete_rey_mago(db: Session, rey_id: int):
    try:
        # Buscar al rey en la base de datos usando su id
        rey = db.query(ReyMago).filter(ReyMago.id == rey_id).first()

        # Si no se encuentra el rey, lanzamos una excepción
        if rey is None:
            raise NoResultFound("Rey no encontrado")

        # Si el rey existe, lo eliminamos
        db.delete(rey)  # Marcamos el objeto para eliminarlo
        db.commit()  # Confirmamos la transacción
        return rey  # Devolvemos el rey eliminado (opcional)

    except NoResultFound as e:
        raise e  # Lanza una excepción si no se encuentra el rey
    except Exception as e:
        db.rollback()  # Hacemos rollback si ocurre algún error
        raise e  # Lanza cualquier otro error

# Juguete CRUD


def create_juguete(db: Session, juguete: JugueteCreate):
    db_juguete = Juguete(**juguete.dict())
    db.add(db_juguete)
    db.commit()
    db.refresh(db_juguete)
    return db_juguete


def get_juguetes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Juguete).offset(skip).limit(limit).all()


def delete_juguete(db: Session, juguete_id: int):
    try:
        # Buscar al juguete en la base de datos usando su id
        juguete = db.query(Juguete).filter(Juguete.id == juguete_id).first()

        # Si no se encuentra el juguete, lanzamos una excepción
        if juguete is None:
            raise NoResultFound("Juguete no encontrado")

        # Si el juguete existe, lo eliminamos
        db.delete(juguete)  # Marcamos el objeto para eliminarlo
        db.commit()  # Confirmamos la transacción
        return juguete  # Devolvemos el juguete eliminado (opcional)

    except NoResultFound as e:
        raise e  # Lanza una excepción si no se encuentra el usuario
    except Exception as e:
        db.rollback()  # Hacemos rollback si ocurre algún error
        raise e  # Lanza cualquier otro error

# Carta CRUD


def create_carta(db: Session, carta_create: CartaCreate):
    # Buscar al usuario y al rey mago
    usuario = db.query(Usuario).filter(
        Usuario.id == carta_create.usuario_id).first()
    reymago = db.query(ReyMago).filter(
        ReyMago.id == carta_create.rey_mago_id).first()
    if not usuario or not reymago:
        raise HTTPException(
            status_code=404, detail="Usuario o Rey Mago no encontrado")

    # Buscar los juguetes en la base de datos
    juguetes = db.query(Juguete).filter(
        Juguete.id.in_(carta_create.juguetes_ids)).all()
    if len(juguetes) != len(carta_create.juguetes_ids):
        raise HTTPException(
            status_code=404, detail="Uno o más juguetes no encontrados")
    # Crear la carta
    # Crear la carta
    db_carta = Carta(usuario_id=carta_create.usuario_id,
                     rey_mago_id=carta_create.rey_mago_id,
                     )

    db.add(db_carta)
    db.commit()
    db.refresh(db_carta)
    # Relacionar la carta con los juguetes
    db_carta.juguetes = juguetes
    db.commit()

    response_data = {
        "id": db_carta.id,
        "usuario_id": db_carta.usuario_id,
        "rey_mago_id": db_carta.rey_mago_id,
        # Agregar los IDs de los juguetes
        "juguetes_ids": [juguete.id for juguete in db_carta.juguetes]
    }

    return response_data


def get_cartas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Carta).offset(skip).limit(limit).all()


def delete_carta(db: Session, carta_id: int):
    try:
        carta = db.query(Carta).filter(Carta.id == carta_id).first()

        if carta is None:
            raise NoResultFound("Juguete no encontrado")

        db.delete(carta)  # Marcamos el objeto para eliminarlo
        db.commit()  # Confirmamos la transacción
        return carta  # Devolvemos el juguete eliminado (opcional)

    except NoResultFound as e:
        raise e  # Lanza una excepción si no se encuentra el usuario
    except Exception as e:
        db.rollback()  # Hacemos rollback si ocurre algún error
        raise e  # Lanza cualquier otro error
