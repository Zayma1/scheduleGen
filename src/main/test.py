import json

# Definir a classe
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

# JSON de exemplo
json_string = '{"nome": "João", "idade": 30}'

# Carregar o JSON em um dicionário Python
dados = json.loads(json_string)

# Criar instância da classe com base nos dados do JSON
pessoa = Pessoa(**dados)

# Acessar os atributos da instância
print("Nome:", pessoa.nome)
print("Idade:", pessoa.idade)