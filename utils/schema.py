# Classe carro do modelo de dados (schema)
from pydantic import BaseModel

class Carro(BaseModel):
    marca: str
    modelo: str
    placa: str
    cor: str
    id: int