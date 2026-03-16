import os

import stripe
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["success"])
templates = Jinja2Templates(directory="app/templates")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
ENABLE_PAYWALL = str(os.getenv("ENABLE_PAYWALL", "false")).lower() in ("1", "true", "yes", "on")


@router.get("/success")
async def success(
    request: Request,
    demo: bool = Query(False),
    session_id: str | None = Query(None),
    email: str | None = Query(None),
):
    if ENABLE_PAYWALL and not demo:
        if not session_id:
            raise HTTPException(status_code=400, detail="Missing session_id")
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Stripe error: {exc}") from exc

        if session.get("payment_status") != "paid":
            raise HTTPException(status_code=402, detail="Payment not completed")

    context = {
        "request": request,
        "email": email,
        "demo": demo,
        "session_id": session_id,
    }
    return templates.TemplateResponse("success.html", context)
