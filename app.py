from flask import Flask, render_template, request
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    dados = None
    if request.method == "POST":
        # Pega a palavra chave
        termo = request.form["termo"]
        pytrends = TrendReq(hl='pt-BR', tz=360)
        # Usa o pytrends e a palavra chave para retornar os valores, pega de agora a 7 dias atras
        pytrends.build_payload([termo], timeframe='now 7-d', geo='BR')

        df = pytrends.interest_over_time()
        
        if not df.empty:
            dados = [{"data": row["date"].strftime('%d/%m/%Y %H:%M'), "valor": row[termo]} for _, row in df.reset_index().iterrows()]
    return render_template("index.html", dados=dados)

if __name__ == "__main__":
    app.run(debug=True)