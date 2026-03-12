import os
import logging
import stripe
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhooks"])

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

@router.post("/stripe")
async def stripe_webhook(request: Request):
    stripe_signature = request.headers.get("stripe-signature")

    if not STRIPE_WEBHOOK_SECRET:
        logger.warning("Webhook received but STRIPE_WEBHOOK_SECRET is not configured.")
        return JSONResponse(
            {
                "status": "received",
                "message": "Webhook received (signature verification disabled - configure STRIPE_WEBHOOK_SECRET)"
            },
            status_code=200,
        )

    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    try:
        body = await request.body()
        event = stripe.Webhook.construct_event(
            body,
            stripe_signature,
            STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event.get("type")
    event_id = event.get("id")

    if event_type == "checkout.session.completed":
        session = event.get("data", {}).get("object", {})
        logger.info(
            "Checkout completed: session_id=%s payment_status=%s",
            session.get("id"),
            session.get("payment_status"),
        )

    return JSONResponse(
        {
            "status": "received",
            "event_id": event_id,
            "event_type": event_type,
        },
        status_code=200,
    )