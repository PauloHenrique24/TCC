import requests

def get_exchange_rate(moeda_origem, moeda_destino):
    """Consulta a taxa de câmbio entre duas moedas usando a API AwesomeAPI."""
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda_origem}-{moeda_destino}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        data = response.json()
        
        chave = f"{moeda_origem}{moeda_destino}"
        if chave in data:
            return float(data[chave]['bid'])  # 'bid' representa a taxa de câmbio
        else:
            print(f"Erro: Dados não encontrados para {moeda_origem}-{moeda_destino}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar API: {e}")
        return None

def converter_moeda():
    """Solicita ao usuário as moedas e o valor a ser convertido."""
    moeda_origem = input("Digite a moeda de origem (ex: USD): ").strip().upper()
    moeda_destino = input("Digite a moeda de destino (ex: BRL): ").strip().upper()
    
    try:
        valor = float(input(f"Digite o valor em {moeda_origem} que deseja converter: "))
    except ValueError:
        print("Erro: Digite um número válido.")
        return
    
    taxa_cambio = get_exchange_rate(moeda_origem, moeda_destino)
    
    if taxa_cambio:
        valor_convertido = valor * taxa_cambio
        print(f"\n{valor:.2f} {moeda_origem} equivale a {valor_convertido:.2f} {moeda_destino}.\n")
    else:
        print("Não foi possível obter a taxa de câmbio.")

# Executa a conversão
converter_moeda()
