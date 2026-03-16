# ClearTariff FastAPI + Stripe Demo

ClearTariff is a FastAPI app for generating recruiter-demo-friendly tariff and landed-cost reports for Amazon sellers. It includes a hosted Stripe Checkout handoff, success and cancel pages, PDF generation, and an optional webhook endpoint.

## Tech Stack

- Python 3.10+
- FastAPI and Uvicorn
- Stripe Checkout and Stripe webhooks
- Jinja2 templates and static assets
- ReportLab and optional WeasyPrint PDF generation
- Docker for deployment

## Checkout Flow

1. The landing or pricing page calls `POST /api/checkout/create-session`.
2. When `ENABLE_PAYWALL=false`, the endpoint returns `/success?demo=true` for a local no-charge demo.
3. When `ENABLE_PAYWALL=true`, Stripe Checkout redirects back to `/success?session_id={CHECKOUT_SESSION_ID}`.
4. The success page renders `app/templates/success.html` and verifies the Stripe session when paywall mode is enabled.

## Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file from `.env.example`.

3. For a fast local demo, use:

```env
APP_URL=http://127.0.0.1:8000
SUCCESS_URL=http://127.0.0.1:8000/success
CANCEL_URL=http://127.0.0.1:8000/cancel
ENABLE_PAYWALL=false
PREFER_REPORTLAB=true
ENABLE_WEASY=false
```

4. For live Stripe checkout, also set:

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PRICE_ID=price_...
STRIPE_WEBHOOK_SECRET=whsec_...
ENABLE_PAYWALL=true
```

5. Start the app:

```bash
python -m uvicorn app.main:app --reload
```

## Required Environment Variables

- `APP_URL`: Base URL for the app.
- `SUCCESS_URL`: Checkout success redirect target. Defaults to `APP_URL/success`.
- `CANCEL_URL`: Checkout cancel redirect target. Defaults to `APP_URL/cancel`.
- `ENABLE_PAYWALL`: `false` for local demo mode, `true` for live Stripe payment enforcement.
- `STRIPE_SECRET_KEY`: Required for live Checkout session creation.
- `STRIPE_PRICE_ID`: Required for live Checkout session creation.
- `STRIPE_WEBHOOK_SECRET`: Required only if you want verified Stripe webhooks.

## Railway Deployment

1. Create a new Railway project from this repo.
2. Let Railway build from the existing Dockerfile.
3. Set these environment variables in Railway:

```env
APP_URL=https://<your-railway-domain>
SUCCESS_URL=https://<your-railway-domain>/success
CANCEL_URL=https://<your-railway-domain>/cancel
ENABLE_PAYWALL=true
STRIPE_SECRET_KEY=sk_live_or_test_...
STRIPE_PRICE_ID=price_...
STRIPE_WEBHOOK_SECRET=whsec_...
PREFER_REPORTLAB=true
ENABLE_WEASY=false
```

4. In Stripe, add the Railway domain to allowed redirect destinations and configure the webhook endpoint as `https://<your-railway-domain>/webhook/stripe` if you plan to receive webhook events.

Railway-specific config files are not required here because the Dockerfile now binds Uvicorn to Railway's injected `PORT`.
