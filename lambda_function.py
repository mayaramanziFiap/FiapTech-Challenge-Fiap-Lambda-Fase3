import re
import requests
import jwt  # Biblioteca para gerar o token JWT

def validate_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False
    return True

def check_cpf_in_test_api(cpf):
    # URL de teste para substituir a chamada real
    api_url = "https://jsonplaceholder.typicode.com/users"
    try:
        # Realiza uma requisição GET para simular uma consulta 
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            # Aqui simulamos que encontramos o cliente se a lista de usuários não estiver vazia
            return {"name": "Teste Usuario", "cpf": cpf}
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API de teste: {e}")
        return None

def generate_jwt(payload, secret="seu-segredo"):
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def lambda_handler(event, context):
    print(f"Evento recebido: {event}")  # Registra o evento para depuração

    # Captura o CPF dos parâmetros da requisição
    cpf = event.get("queryStringParameters", {}).get("cpf")
    if not cpf:
        return {"statusCode": 400, "body": "CPF não fornecido"}

    # Validação básica do CPF
    if not validate_cpf(cpf):
        return {"statusCode": 401, "body": "CPF inválido"}

    # Consulta à API de teste
    client_data = check_cpf_in_test_api(cpf)
    if client_data:
        # Gera um token JWT com os dados fictícios do cliente
        token = generate_jwt(client_data)
        return {"statusCode": 200, "body": f"Token JWT: {token}"}
    else:
        return {"statusCode": 404, "body": "CPF não encontrado"}
