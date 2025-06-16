from flask import Flask, render_template
import requests
import pandas as pd
import json
import yfinance as yf

app = Flask(__name__)

def fetch_stock_data(symbol):
    url = f"https://msh-datacenter.cafef.vn/price/api/v1/CompanyCompac/DataChartStock?symbol={symbol.lower()}"
    resp = requests.get(url)
    data = resp.json()

    if not data.get("isSuccess"):
        return None

    prices = data["value"]["price"]
    df = pd.DataFrame(prices, columns=["Timestamp", "Close", "Volume", "Open", "High", "Low"])
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df.sort_values("Date", inplace=True)
    df["Avg5"] = df["Close"].rolling(window=5).mean().round(2)

    chart_labels = df["Date"].dt.strftime("%Y-%m-%d").tolist()
    chart_data = df["Close"].tolist()
    chart_ohlc = [
        {
            "x": row["Date"].strftime("%Y-%m-%d"),
            "o": round(row["Open"], 2),
            "h": round(row["High"], 2),
            "l": round(row["Low"], 2),
            "c": round(row["Close"], 2)
        }
        for _, row in df.iterrows()
    ]

    return df, chart_labels, chart_data, chart_ohlc

def fetch_yahoo_quote(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.VN")
        info = ticker.info
        return {
            "current_price": info.get("regularMarketPrice"),
            "change": info.get("regularMarketChange"),
            "change_percent": info.get("regularMarketChangePercent"),
            "previous_close": info.get("previousClose"),
            "currency": info.get("currency", "VND")
        }
    except Exception as e:
        print("Yahoo API error:", e)
        return {}

@app.route('/stock/<symbol>')
def show_stock(symbol):
    result = fetch_stock_data(symbol)
    if result is None:
        return "Không lấy được dữ liệu từ CafeF"

    df, chart_labels, chart_data, chart_ohlc = result
    yahoo = fetch_yahoo_quote(symbol.upper())

    return render_template("stock.html",
        symbol=symbol.upper(),
        table=df[::-1].to_dict(orient="records"),
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data),
        chart_ohlc=json.dumps(chart_ohlc),
        yahoo=yahoo
    )

if __name__ == '__main__':
    app.run(debug=True)
