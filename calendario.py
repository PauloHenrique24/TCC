import requests
import datetime

# 🔑 Sua chave de API
API_KEY = "8NGbM1OgHCjyKgW8zBdVShMZDBeY4Hrd"
BASE_URL = "https://calendarific.com/api/v2/holidays"

# 📌 Dicionário de tradução de feriados
TRADUCOES = {
    "New Year's Day": "Ano Novo",
    "Carnival": "Carnaval",
    "Good Friday": "Sexta-feira Santa",
    "Easter Sunday": "Páscoa",
    "Tiradentes' Day": "Dia de Tiradentes",
    "Labour Day": "Dia do Trabalho",
    "Corpus Christi": "Corpus Christi",
    "Independence Day": "Dia da Independência",
    "Our Lady of Aparecida": "Nossa Senhora Aparecida",
    "All Souls' Day": "Dia de Finados",
    "Proclamation of the Republic": "Proclamação da República",
    "Christmas Day": "Natal",
}

# 📅 Função para buscar os feriados do ano
def get_holidays(year, country="BR"):
    params = {
        "api_key": API_KEY,
        "country": country,
        "year": year,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code != 200 or "response" not in data:
        print("❌ Erro ao obter os feriados.")
        return []

    holidays = data["response"]["holidays"]
    
    # Remove fuso horário e converte para YYYY-MM-DD
    return sorted(
        [(datetime.datetime.strptime(h["date"]["iso"].split("T")[0], "%Y-%m-%d").date(), TRADUCOES.get(h["name"], h["name"])) for h in holidays],
        key=lambda x: x[0]
    )

# 🔎 Função para encontrar os próximos feriados
def find_next_holiday(date_str, country="BR"):
    try:
        # Agora o usuário pode digitar no formato DD/MM/AAAA
        input_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato de data inválido! Use o formato DD/MM/AAAA.")
        return

    holidays = get_holidays(input_date.year, country)

    # Se não houver feriados, buscar no próximo ano
    if not holidays:
        holidays = get_holidays(input_date.year + 1, country)

    # Filtra feriados que são após a data informada
    upcoming_holidays = [(date, name) for date, name in holidays if date > input_date]

    if upcoming_holidays:
        print("\n📅 Próximos feriados:")
        for date, name in upcoming_holidays[:3]:  # Mostra os 3 próximos
            formatted_date = date.strftime("%d/%m/%Y")
            print(f"➡ {formatted_date}: {name}")
    else:
        print("Nenhum feriado encontrado após esta data.")

# ⌨ Entrada do usuário no formato DD/MM/AAAA
user_date = input("Digite uma data (DD/MM/AAAA): ")
find_next_holiday(user_date)
