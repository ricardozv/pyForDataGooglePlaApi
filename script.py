import requests
import json
import boto3
import urllib.request
import time

# Chave de API da Google Places
API_KEY = ""

# Nome da tabela no DynamoDB
NOME_TABELA = ""

# Cidade a ser pesquisada
cidade = ""

# URL da API da Google Places
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

while True:
    try:
        # Parâmetros da requisição
        params = {
            "query": f"bares em {cidade}",
            "key": API_KEY
        }

        # Faz a requisição à API
        response = requests.get(url, params=params)

        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            # Abre o arquivo de saída
            f = open(f"{cidade}_bares.json", "w")

            # Converte a resposta em um objeto json
            data = json.loads(response.text)

            # Percorre os resultados da pesquisa
            for result in data["results"]:
                # Cria o item para o DynamoDB
                item = {
                    "id": result["place_id"],
                    "nome": result["name"],
                    "endereco": result.get("formatted_address", ""),
                    "latitude": result["geometry"]["location"]["lat"],
                    "longitude": result["geometry"]["location"]["lng"]
                }

                # Faz o download da imagem do bar
                photo_reference = result.get("photos", [{}])[0].get("photo_reference")
                if photo_reference:
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=250&photoreference={photo_reference}&key={API_KEY}"
                    nome_imagem = f"{item['id']}.jpg"
                    urllib.request.urlretrieve(photo_url, nome_imagem)

                    # Adiciona o link da imagem ao item
                    item["imagem_url"] = f"local/{nome_imagem}"

                # Adiciona o item ao arquivo de saída
                f.write(json.dumps({"PutRequest": {"Item": item}}))
                f.write("\n")

            # Fecha o arquivo de saída
            f.close()
            
            # Intervalo de 10 segundos entre cada requisição
            time.sleep(10)

    except Exception as e:
        # Em caso de erro, espera 5 segundos e tenta novamente
        print(f"Erro: {e}. Tentando novamente em 5 segundos...")
        time.sleep(5)
