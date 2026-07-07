from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

VERSION = "1.0.0"

TEMPLATE_DIVISAS = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversor de Divisas DevOps</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f4f8;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            text-align: center;
            width: 360px;
        }
        h1 { color: #1a365d; margin-bottom: 5px; font-size: 24px; }
        h2 { color: #718096; font-size: 13px; margin-top: 0; margin-bottom: 25px; }
        input[type="number"], select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 16px;
            background-color: #f7fafc;
        }
        button {
            width: 100%;
            background-color: #2b6cb0;
            color: white;
            padding: 14px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
            margin-top: 10px;
        }
        button:hover { background-color: #2c5282; }
        .result {
            margin-top: 22px;
            padding: 15px;
            background-color: #ebf8ff;
            border-left: 4px solid #3182ce;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            color: #2b6cb0;
            text-align: left;
        }
        footer {
            margin-top: 25px;
            font-size: 11px;
            color: #a0aec0;
            line-height: 1.4;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>💱 DevOps FX Converter</h1>
    <h2>Servidor Contabo | Versión {{ version }}</h2>
    
    <form method="POST">
        <label style="display:block; text-align:left; font-size:13px; color:#4a5568; font-weight:bold;">Monto en USD (Dólares):</label>
        <input type="number" step="any" name="monto" placeholder="Ej. 100" value="{{ monto }}" min="0" required>
        
        <label style="display:block; text-align:left; font-size:13px; color:#4a5568; font-weight:bold; margin-top:10px;">Convertir a:</label>
        <select name="divisa_destino">
            <option value="EUR" {% if divisa_destino == 'EUR' %}selected{% endif %}>🇪🇺 EUR - Euro</option>
            <option value="MXN" {% if divisa_destino == 'MXN' %}selected{% endif %}>🇲🇽 MXN - Peso Mexicano</option>
            <option value="COP" {% if divisa_destino == 'COP' %}selected{% endif %}>🇨🇴 COP - Peso Colombiano</option>
            <option value="GBP" {% if divisa_destino == 'GBP' %}selected{% endif %}>🇬🇧 GBP - Libra Esterlina</option>
        </select>
        
        <button type="submit">Convertir Divisa</button>
    </form>

    {% if resultado is not none %}
    <div class="result">
        💵 {{ monto }} USD equivalen a:<br>
        <span style="font-size: 22px; display:block; margin-top:5px; color:#1a365d;">{{ resultado }} {{ divisa_destino }}</span>
    </div>
    {% endif %}

    <footer>
        Hora del servidor: {{ hora }}<br>
        Desplegado de forma independiente mediante Docker Swarm
    </footer>
</div>

</body>
</html>
"""

# Tasas de cambio fijas simuladas (Base: 1 USD)
TASAS_CAMBIO = {
    "EUR": 0.92,
    "MXN": 17.05,
    "COP": 3950.00,
    "GBP": 0.79
}

@app.route("/", methods=["GET", "POST"])
def conversor():
    resultado = None
    monto = ""
    divisa_destino = "EUR"
    
    if request.method == "POST":
        try:
            monto_input = request.form.get("monto")
            divisa_destino = request.form.get("divisa_destino")
            
            if monto_input:
                monto = float(monto_input)
                tasa = TASAS_CAMBIO.get(divisa_destino, 1.0)
                calculo = monto * tasa
                
                if divisa_destino in ["COP", "MXN"]:
                    resultado = f"{calculo:,.2f}"
                else:
                    resultado = f"{calculo:.2f}"
                    
        except Exception as e:
            resultado = f"Error en los datos: {str(e)}"

    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return render_template_string(
        TEMPLATE_DIVISAS,
        version=VERSION,
        hora=hora_actual,
        resultado=resultado,
        monto=monto,
        divisa_destino=divisa_destino
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)