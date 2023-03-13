# esse script adiciona varias fotos a uma tabela do dynamoDB
import os
from PIL import Image
import boto3

# Configuração do cliente DynamoDB
dynamodb = boto3.client('dynamodb')
table_name = 'nome-da-tabela'
table_key = 'id'

# Configuração do diretório onde as fotos estão
photo_directory = 'caminho-para-o-diretorio-das-fotos'

# Itera sobre todas as fotos no diretório
for file_name in os.listdir(photo_directory):
    # Verifica se o arquivo é uma foto JPG
    if file_name.endswith('.jpg'):
        # Abre a foto e lê os dados binários
        with Image.open(os.path.join(photo_directory, file_name)) as img:
            photo_data = img.tobytes()

        # Cria um objeto Item para a foto
        item = {
            table_key: {'S': file_name},  # Pode usar o nome do arquivo como chave
            'photo_data': {'B': photo_data}
        }

        # Insere o Item na tabela do DynamoDB
        dynamodb.put_item(TableName=table_name, Item=item)

print('Todas as fotos foram inseridas na tabela do DynamoDB.')
