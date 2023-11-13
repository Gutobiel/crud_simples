from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import uvicorn
from utils.schema import Carro
from utils.lista import carros_db
app = FastAPI()


# Lista de carros vazio
carros_db: List[Carro] = []


# Função para persistir os dados da lista de carros em um arquivo JSON
def persistir_carros(carros_db: List[Carro]):
    with open("carros.json", "w") as f:  # Use "w" para sobrescrever o arquivo
        json.dump([carro.dict() for carro in carros_db], f, indent=4)

# Endpoint para criar um novo carro
@app.post("/carros/", response_model=Carro)
def criar_carro(carro: Carro):
    # Gere um novo ID para o carro
    novo_id = len(carros_db) + 1
    carro.id = novo_id
    # Gere a placa com base na marca e no ID
    placa = carro.marca[:3].upper() + "-" + str(novo_id).zfill(3)
    carro.placa = placa
    carros_db.append(carro)
    persistir_carros(carros_db)
    
    return carro

# Endpoint para listar todos os carros
@app.get("/carros/", response_model=List[Carro])
def listar_carros():
    return carros_db

# Endpoint para deletar um carro pelo seu ID
@app.delete("/carros/{carro_id}", response_model=Carro)
def deletar_carro(carro_id: int):
    # Verifica se o ID existe
    if carro_id < 1 or carro_id > len(carros_db):
        raise HTTPException(status_code=404, detail="Carro não encontrado")

    # Exclui o carro
    carro_deletado = carros_db.pop(carro_id - 1)
    persistir_carros(carros_db)
    return carro_deletado

#n entendi ainda como funciona
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=7777)
