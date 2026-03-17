from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["success"])


@router.get("/success", response_class=HTMLResponse)
async def success(
    demo: bool = Query(False),
    session_id: str | None = Query(None),
    email: str | None = Query(None),
):
    details = []
    if email:
        details.append(f"<p>Email: {email}</p>")
    if session_id:
        details.append(f"<p>Session: {session_id}</p>")
    if demo:
        details.append("<p>Demo mode enabled.</p>")

    return HTMLResponse(
        """
        <html>
            <head><title>ClearTariff - Checkout complete</title></head>
            <body>
                <h1>Checkout complete</h1>
                <p>Your request has been received successfully.</p>
                {details}
            </body>
        </html>
        """.format(details="".join(details))
    )
