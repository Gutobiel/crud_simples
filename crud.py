from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

# Define o modelo de dados para a entidade "Produto"
class Produto(BaseModel):
    nome: str
    tipo: str
    preco: float
    id: int

    def to_json(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "preco": self.preco,
            "id": self.id
        }

# Lista de produtos, simulando um banco de dados em memória
produtos_db: List[Produto] = []

# Função para persistir os dados da lista de produtos em um arquivo JSON
def persistir_produtos(produtos_db: List[Produto]):
    with open("produtos.json", "w") as f:  # Use "w" para sobrescrever o arquivo
        json.dump([produto.to_json() for produto in produtos_db], f, indent=4)

# Endpoint para criar um novo produto
@app.post("/produtos/", response_model=Produto)
def criar_produto(produto: Produto):
    # Gere um novo ID para o produto
    novo_id = len(produtos_db) + 1
    produto.id = novo_id
    produtos_db.append(produto)
    persistir_produtos(produtos_db)
    return produto

# Endpoint para listar todos os produtos
@app.get("/produtos/", response_model=List[Produto])
def listar_produtos():
    return produtos_db

# Endpoint para deletar um produto pelo seu ID
@app.delete("/produtos/{produto_id}", response_model=Produto)
def deletar_produto(produto_id: int):
    # Verifica se o ID existe
    if produto_id < 1 or produto_id > len(produtos_db):
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Exclui o produto
    produto_deletado = produtos_db.pop(produto_id - 1)
    persistir_produtos(produtos_db)
    return produto_deletado
