from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import threading
import time

load_dotenv()


app = Flask(__name__)
estado_maquina = "IDLE"
payment_atual = None
pagamento_confirmado = False

# ===============================
# CRIAR PAGAMENTO PIX
# ===============================

ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")

@app.route("/criar_pix", methods=["POST"])
def criar_pix():
    global estado_maquina, payment_atual
    data = request.json

    valor = float(data.get("valor"))
    email = data.get("email")

    headers = {
        "access_token": ASAAS_API_KEY,
        "Content-Type": "application/json"
    }

    # 1️⃣ Criar cliente
    cliente_data = {
        "name": "Cliente Teste",
        "email": email,
        "cpfCnpj": "52998224725"
    }

    cliente = requests.post(
        "https://sandbox.asaas.com/api/v3/customers",
        json=cliente_data,
        headers=headers
    ).json()

    customer_id = cliente["id"]

    # 2️⃣ Criar cobrança PIX
    due_date = (datetime.now() + timedelta(minutes=2)).strftime("%Y-%m-%d")
    cobranca_data = {
        "customer": customer_id,
        "billingType": "PIX",
        "value": valor,
        "dueDate": due_date
    }

    cobranca_resp = requests.post(
        "https://sandbox.asaas.com/api/v3/payments",
        json=cobranca_data,
        headers=headers
    )

    cobranca = cobranca_resp.json()

    print("RESPOSTA ASAAS:", cobranca)

    if "id" not in cobranca:
        return jsonify({
            "erro": cobranca
        }), 400

    payment_id = cobranca["id"]
    estado_maquina = "AGUARDANDO_PAGAMENTO"
    payment_atual = payment_id

    # 3️⃣ Pegar QR Code
    pix = requests.get(
        f"https://sandbox.asaas.com/api/v3/payments/{payment_id}/pixQrCode",
        headers=headers
    ).json()

    return jsonify({
        "id": payment_id,
        "qr_code": pix["payload"],
        "qr_code_base64": pix["encodedImage"]
    })
# ===============================
# VERIFICAR STATUS DO PAGAMENTO
# ===============================
@app.route("/verificar_pagamento/<payment_id>", methods=["GET"])
def verificar_pagamento(payment_id):

    headers = {
        "access_token": ASAAS_API_KEY,
        "Content-Type": "application/json"
    }

    payment = requests.get(
        f"https://sandbox.asaas.com/api/v3/payments/{payment_id}",
        headers=headers
    ).json()

    return jsonify({
        "id": payment["id"],
        "status": payment["status"]
    })

# =================================
# EXPIRAR PAGAMENTO
# =================================
def expirar_pagamento(payment_id):
    global estado_maquina, payment_atual

    time.sleep(120)

    if payment_atual == payment_id and estado_maquina == "AGUARDANDO_PAGAMENTO":

        print("PIX expirado")

        requests.delete(
            f"https://sandbox.asaas.com/api/v3/payments/{payment_id}",
            headers={
                "access_token": ASAAS_API_KEY,
                "Content-Type": "application/json"
            }
        )

        estado_maquina = "EXPIRADO"
        payment_atual = None

    threading.Thread(target=expirar_pagamento, args=(payment_id,)).start()

# ===============================
# WEBHOOK (CONFIRMAÇÃO AUTOMÁTICA)
# ===============================
@app.route("/webhook", methods=["POST"])
def webhook():

    global estado_maquina, payment_atual
    global pagamento_confirmado

    data = request.json
    evento = data.get("event")

    print("EVENTO RECEBIDO:", data)

    if evento == "PAYMENT_RECEIVED":

        payment_id = data["payment"]["id"]

        if payment_id == payment_atual and estado_maquina == "AGUARDANDO_PAGAMENTO":

            print("PIX PAGO")
            pagamento_confirmado = True

            estado_maquina = "PAGO"
            payment_atual = None

        else:
            print("Pagamento ignorado (QR antigo)")

    return "", 200

@app.route("/status_pagamento", methods=["GET"])
def status_pagamento():

    global pagamento_confirmado

    status = pagamento_confirmado

    if pagamento_confirmado:
        pagamento_confirmado = False

    return jsonify({
        "pago": status
    })


if __name__ == "__main__":
    app.run(debug=True)