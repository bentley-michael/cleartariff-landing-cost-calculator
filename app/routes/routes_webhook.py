import os
import logging
from typing import Optional

import stripe
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhooks"])

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")


def _received_response(
    *,
    event_id: Optional[str] = None,
    event_type: Optional[str] = None,
    message: Optional[str] = None,
) -> JSONResponse:
    payload = {"status": "received"}
    if message is not None:
        payload["message"] = message
    else:
        payload["event_id"] = event_id
        payload["event_type"] = event_type
    return JSONResponse(payload, status_code=200)


def _construct_event(body: bytes, stripe_signature: str):
    try:
        return stripe.Webhook.construct_event(
            body,
            stripe_signature,
            STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid payload") from exc
    except stripe.error.SignatureVerificationError as exc:
        raise HTTPException(status_code=400, detail="Invalid signature") from exc


@router.post("/stripe")
async def stripe_webhook(request: Request):
    stripe_signature = request.headers.get("stripe-signature")

    if not STRIPE_WEBHOOK_SECRET:
        logger.warning("Webhook received but STRIPE_WEBHOOK_SECRET is not configured.")
        return _received_response(
            message="Webhook received (signature verification disabled - configure STRIPE_WEBHOOK_SECRET)"
        )

    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    body = await request.body()
    event = _construct_event(body, stripe_signature)
    event_type = event.get("type")
    event_id = event.get("id")

    if event_type == "checkout.session.completed":
        session = event.get("data", {}).get("object", {})
        logger.info(
            "Checkout completed: session_id=%s payment_status=%s",
            session.get("id"),
            session.get("payment_status"),
        )

    return _received_response(event_id=event_id, event_type=event_type)