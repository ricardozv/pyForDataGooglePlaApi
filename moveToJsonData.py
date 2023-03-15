import json

# Carregar o JSON de destino em um dicionário
with open('destino.json', 'r') as f:
    destino = json.load(f)

# Iterar sobre os dados do JSON de origem
with open('origem.json', 'r') as f:
    for linha in f:
        dados = json.loads(linha)['PutRequest']['Item']
        id_estabelecimento = dados['id']

        # Verificar se o estabelecimento já existe no dicionário de destino
        if any(estabelecimento['id'] == id_estabelecimento for estabelecimento in destino['establishments']):
            print(f'Estabelecimento {id_estabelecimento} já existe no JSON de destino.')
        else:
            # Adicionar o estabelecimento ao dicionário de destino
            novo_estabelecimento = {
                'id': id_estabelecimento,
                'name': dados['nome'],
                'image': dados.get('imagem_url', ''),
                'location': {
                    'address': dados['endereco'],
                    'latitude': dados['latitude'],
                    'longitude': dados['longitude']
                }
            }
            destino['establishments'].append(novo_estabelecimento)

# Salvar o dicionário de destino como um JSON
with open('destino.json', 'w') as f:
    json.dump(destino, f, indent=2)

