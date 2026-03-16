import os, base64, logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import resend

log = logging.getLogger(__name__)

RESEND_API_KEY   = os.getenv("RESEND_API_KEY", "")
EMAIL_SENDER     = os.getenv("EMAIL_SENDER", "contact@content365.xyz")
EMAIL_SENDER_NAME = os.getenv("EMAIL_SENDER_NAME", "Nathan Bentley")
REPLY_TO         = os.getenv("REPLY_TO", "")
EMAIL_CC         = [s.strip() for s in os.getenv("EMAIL_CC", "").split(",") if s.strip()]
EMAIL_BCC        = [s.strip() for s in os.getenv("EMAIL_BCC", "").split(",") if s.strip()]


def _write_outbox_copy(to_email: str, subject: str, text: str, pdf_bytes: bytes, filename: str) -> str:
    out = Path("outbox")
    out.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_to = "".join(c for c in (to_email or "unknown") if c.isalnum() or c in ("@", ".", "_", "-"))
    pdf_path = out / f"{stamp}_{safe_to}_{filename or 'report.pdf'}"
    note_path = out / f"{stamp}_{safe_to}_note.txt"
    pdf_path.write_bytes(pdf_bytes or b"")
    note_path.write_text(
        f"TO: {to_email}\nFROM: {EMAIL_SENDER} ({EMAIL_SENDER_NAME})\n"
        f"CC: {', '.join(EMAIL_CC) or '-'}\nBCC: {', '.join(EMAIL_BCC) or '-'}\n"
        f"SUBJECT: {subject}\n\n{text}\n",
        encoding="utf-8",
    )
    return f"dev-outbox:{pdf_path.as_posix()}"


def send_pdf_email(to_email: str, subject: str, text: str, pdf_bytes: bytes, filename: str) -> Optional[str]:
    if not RESEND_API_KEY or not EMAIL_SENDER:
        log.warning("RESEND not configured; writing to ./outbox")
        return _write_outbox_copy(to_email, subject, text, pdf_bytes, filename)

    try:
        resend.api_key = RESEND_API_KEY

        message = {
            "from": f"{EMAIL_SENDER_NAME} <{EMAIL_SENDER}>" if EMAIL_SENDER_NAME else EMAIL_SENDER,
            "to": [to_email],
            "subject": subject,
            "text": text,
            "html": f"<p>{text}</p><p>Report attached.</p>",
            "attachments": [
                {
                    "filename": filename or "report.pdf",
                    "content": base64.b64encode(pdf_bytes or b"").decode("utf-8"),
                }
            ],
        }

        if REPLY_TO:
            message["reply_to"] = REPLY_TO
        if EMAIL_CC:
            message["cc"] = EMAIL_CC
        if EMAIL_BCC:
            message["bcc"] = EMAIL_BCC

        resp = resend.Emails.send(message)
        log.info("Resend response: %s", resp)
        return "202 Accepted"
    except Exception as e:
        log.warning("Resend send failed, using ./outbox: %s", e)
        return _write_outbox_copy(to_email, subject, text, pdf_bytes, filename)