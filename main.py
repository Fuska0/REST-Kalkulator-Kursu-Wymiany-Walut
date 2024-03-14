from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests, re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/1fde28618732823fad0035ef/latest"
COINAPI_URL = "https://rest.coinapi.io/v1/exchangerate"


def calculate_statistics(rates: list):
    min_rate = round(min(rates), 2)
    max_rate = round(max(rates), 2)
    avg_rate = round(sum(rates) / len(rates), 2)
    return min_rate, max_rate, avg_rate


def error_handler(e):
    pattern_400s = r'\b4[0-9]{2}\b'
    pattern_500s = r'\b5[0-9]{2}\b'
    pattern_300s = r'\b3[0-9]{2}\b'
    if re.search(pattern_400s, str(e)):
        return "\n Prawdopodobnie pierwsza wpisana waluta jest błędna :("

    if re.search(pattern_500s, str(e)):
        return "\n Wystąpił błąd po stronie serwera :{"

    if re.search(pattern_300s, str(e)):
        return "\n Serwis musi wykonać dodatkowe kroki, aby uzyskać żądane zasoby :/"

    return ""


async def get_exchange_rate(currency1: str, currency2: str):
    url = f"{EXCHANGE_RATE_API_URL}/{currency1}"
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    rates1 = data["conversion_rates"]

    if currency2 not in rates1:
        raise Exception(f"Brak kursu dla waluty {currency2} :<")

    rate2 = round(rates1[currency2], 2)
    return rate2


async def get_coin_api_exchange_rate(currency1: str, currency2: str):
    url = f"{COINAPI_URL}/{currency1}/{currency2}?apikey=C58816FF-A503-4427-B07D-7AC03C05B515"
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise Exception(f"Brak kursu dla waluty {currency2} :[")

    return round(data["rate"], 2)



@app.get("/calculate-exchange-rate")
async def calculate_exchange_rate(currency1: str, currency2: str):
    rate1 = await get_exchange_rate(currency1, currency2)
    return {"Exchange Rate API": rate1}


@app.get("/calculate-coin-api-rate")
async def calculate_coin_api_rate(currency1: str, currency2: str):
    rate3 = await get_coin_api_exchange_rate(currency1, currency2)
    return {"CoinAPI": rate3}


@app.post("/calculate-all-rates", response_class=HTMLResponse)
async def calculate_all_rates(request: Request):
    form = await request.form()
    currency1 = form.get("currency1").upper()
    currency2 = form.get("currency2").upper()
    amount = abs(float(form.get("amount", 0)))

    try:
        exchange_rate_1 = await get_exchange_rate(currency1, currency2)
        exchange_rate_3 = await get_coin_api_exchange_rate(currency1, currency2)

        statistics = calculate_statistics([exchange_rate_1, exchange_rate_3])
        min_rate, max_rate, avg_rate = statistics

        converted_amount = round(amount * avg_rate, 2)

        result_html = f"""
        <html>
            <body>
                <h1>Wyniki obliczeń:</h1>
                <p>Kursy w poszczególnych serwisach:</p>
                <ul>
                    <li>Exchange Rate API: {exchange_rate_1}</li>
                    <li>CoinAPI: {exchange_rate_3}</li>
                </ul>

                <p>Minimalny kurs wymiany: {min_rate}</p>
                <p>Maksymalny kurs wymiany: {max_rate}</p>
                <p>Średni kurs wymiany: {avg_rate}</p>

                <h2>Przeliczona kwota:</h2>
                <p>Wprowadzona kwota: {amount} {currency1}</p>
                <p>Przeliczona kwota na {currency2} przy średnim kursie: {converted_amount} {currency2}</p>
            </body>
        </html>
        """

        return HTMLResponse(content=result_html)

    except Exception as e:
        error_html = f"""
        <html>
            <body>
                <h1>Wystąpił błąd:</h1>
                <p>{str(e)}</p>
                <p>{error_handler(e)}</p>
            </body>
        </html>
        """
        return HTMLResponse(content=error_html)


@app.get("/", response_class=HTMLResponse)
async def main():
    form_html = """
    <html>
        <body>
            <h1>Kalkulator Kursu Wymiany Walut</h1>
            <form action="/calculate-all-rates" method="post">
                <label for="currency1">Waluta źródłowa:</label>
                <input type="text" id="currency1" name="currency1"><br><br>
                <label for="currency2">Waluta docelowa:</label>
                <input type="text" id="currency2" name="currency2"><br><br>
                <label for="amount">Kwota:</label>
                <input type="number" id="amount" name="amount" step="0.01"><br><br>
                <input type="submit" value="Oblicz">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=form_html)
