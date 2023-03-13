import requests
import json
import boto3

# Chave de API da Google Places
API_KEY = ""

# Nome da tabela no DynamoDB
NOME_TABELA = "SÃOLUIS"

# Cria a conexão com o DynamoDB
 dynamodb = boto3.resource("dynamodb")

# Obtém a referência da tabela
table = dynamodb.Table(BARES_SAOLUIS)

# Cidade a ser pesquisada
cidade = "São luís"

# URL da API da Google Places
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

# Parâmetros da requisição
params = {
    "query": f"bares em {cidade}",
    "key": API_KEY
}

# Faz a requisição à API
response = requests.get(url, params=params)

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Converte a resposta em um objeto json
    data = json.loads(response.text)

    # Percorre os resultados da pesquisa
    for result in data["results"]:
        # Cria o item para o DynamoDB
        item = {
            "id": result["place_id"],
            "nome": result["name"],
            "endereco": result.get("formatted_address", ""),
            "horarios": [],
            "latitude": result["geometry"]["location"]["lat"],
            "longitude": result["geometry"]["location"]["lng"]
        }

        # Obtém os dias e horários de funcionamento do bar
        for periodo in result.get("opening_hours", {}).get("periods", []):
            dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
            dia_inicio = dias[periodo["open"]["day"]]
            hora_inicio = periodo["open"]["time"]
            dia_fim = dias[periodo["close"]["day"]]
            hora_fim = periodo["close"]["time"]
            item["horarios"].append({
                "dia_inicio": dia_inicio,
                "hora_inicio": hora_inicio,
                "dia_fim": dia_fim,
                "hora_fim": hora_fim
            })

        # Armazena a imagem do bar no S3
        photo_reference = result.get("photos", [{}])[0].get("photo_reference")
        if photo_reference:
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=300&photoreference={photo_reference}&key={API_KEY}"
            nome_imagem = f"{item['id']}.jpg"
            s3 = boto3.resource('s3')
            s3.meta.client.download_fileobj('nome_do_seu_bucket', nome_imagem, urllib.request.urlopen(photo_url))

            # Adiciona o link da imagem ao item
            item["imagem_url"] = f"https://sua-bucket.s3.amazonaws.com/{nome_imagem}"

        # Salva o item no DynamoDB
        table.put_item(Item=item)
else:
    print("Erro na requisição:", response.status_code)
