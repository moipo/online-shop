import uuid

import requests

API_URL = "https://api.yookassa.ru/v3/payments"


class YooKassaError(Exception):
    pass


def create_payment(
    shop_id,
    secret_key,
    amount,
    description,
    return_url,
    metadata=None,
):
    if not shop_id or not secret_key:
        raise YooKassaError(
            "YooKassa is not configured. Set YOOKASSA_SHOP_ID and "
            "YOOKASSA_SECRET_KEY environment variables."
        )

    if amount <= 0:
        raise YooKassaError("Payment amount must be greater than zero.")

    payload = {
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB",
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "description": description[:128],
    }
    if metadata:
        payload["metadata"] = metadata

    headers = {
        "Content-Type": "application/json",
        "Idempotence-Key": uuid.uuid4().hex,
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            auth=(shop_id, secret_key),
            timeout=30,
        )
    except requests.RequestException as exc:
        raise YooKassaError(f"Network error: {exc}") from exc

    if not response.ok:
        raise YooKassaError(
            f"YooKassa error {response.status_code}: {response.text[:300]}"
        )

    data = response.json()
    payment_id = data.get("id")
    confirmation_url = (data.get("confirmation") or {}).get("confirmation_url")
    if not payment_id or not confirmation_url:
        raise YooKassaError(f"Unexpected YooKassa response: {data}")

    return payment_id, confirmation_url
