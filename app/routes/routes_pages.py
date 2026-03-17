# app/routes/routes_pages.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["pages"])

@router.get("/cancel", response_class=HTMLResponse)
async def cancel():
    return HTMLResponse(
        """
        <html>
            <head><title>ClearTariff - Checkout canceled</title></head>
            <body>
                <h2>ClearTariff - Checkout canceled</h2>
                <p>No charge was made. You can try again any time.</p>
            </body>
        </html>
        """
    )


@router.get("/pricing")
async def pricing():
    try:
        html = (open("app/templates/pricing.html", "r", encoding="utf-8").read())
    except Exception as e:
        html = f"<h2>Pricing</h2><p>$9 per report.</p><pre>{e}</pre>"
    return HTMLResponse(html)


@router.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(
        """
        <html>
            <head><title>ClearTariff</title></head>
            <body>
                <h1>ClearTariff</h1>
                <p>Service is up.</p>
            </body>
        </html>
        """
    )


@router.get("/form")
async def form():
    from fastapi.responses import HTMLResponse
    try:
        html = (open("app/templates/form.html", "r", encoding="utf-8").read())
    except Exception as e:
        html = f"<h2>Calculate</h2><p>Form error</p><pre>{e}</pre>"
    return HTMLResponse(html)
