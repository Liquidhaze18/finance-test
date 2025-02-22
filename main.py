from fastapi import FastAPI
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenido a la API de datos financieros"}

@app.get("/ticker/{symbol}")
def obtener_datos_ticker(symbol: str):
    stock = yf.Ticker(symbol)
    historial = stock.history(period="6mo")  # Últimos 6 meses

    if historial.empty:
        return {"error": f"No se encontraron datos para {symbol}"}

    # Generar gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(historial.index, historial["Close"], label=f"Precio de {symbol}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio de Cierre (USD)")
    plt.title(f"Historial de {symbol}")
    plt.legend()

    # Convertir gráfico a base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return {
        "ticker": symbol,
        "precio_actual": historial["Close"].iloc[-1],
        "rendimiento_6m": (historial["Close"].iloc[-1] - historial["Close"].iloc[0]) / historial["Close"].iloc[0] * 100,
        "grafico": f"data:image/png;base64,{image_base64}"
    }
