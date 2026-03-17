# System Overview

## Short Architecture Explanation

ClearTariff is a single-service FastAPI application that combines a browser-facing calculator, PDF report generation, and a checkout-ready payment flow. The service accepts landed-cost inputs from HTML forms, transforms those inputs into a structured payload, renders a report, and optionally integrates with Stripe for paid access patterns. The codebase is intentionally compact, but the architecture still demonstrates separation of concerns across routing, rendering, utility helpers, and operational endpoints.

At runtime, the browser interacts with FastAPI routes for page delivery, report generation, checkout, and webhook receipt. Supporting modules handle PDF rendering, optional provider integrations, and fallback delivery behavior such as writing generated reports to an outbox when live email is not configured.

## Major Folders

### `app/`
Primary application source. Contains the FastAPI bootstrap in `main.py`, route modules, templates, PDF generators, presets, and utilities.

### `app/data/`
Home for provider-style integrations such as tariff or rate lookup helpers. This is where external data enrichment can be added without bloating route handlers.

### `app/pdf/`
PDF rendering implementations. The project includes an Amazon-focused ReportLab generator, optional WeasyPrint support, and fallback rendering paths.

### `app/presets/`
Example product presets used to seed calculator scenarios for demos.

### `app/routes/`
Modular route definitions for pages, checkout session creation, success handling, and Stripe webhooks.

### `app/static/`
Static assets and downloadable sample artifacts served directly by the app.

### `app/templates/`
HTML templates for the landing page, calculator form, pricing page, and success or cancel views.

### `app/utils/`
Utility code for secondary workflows such as email delivery and order logging.

### `docs/`
Documentation assets, including README screenshots.

### `outbox/`
Local fallback output for report delivery when a live email provider is not configured.

### `tests/`
Automated route tests and manual smoke-test helpers.

## Landed-Cost Calculation Pipeline

1. The user fills out the calculator form with product, classification, quantity, and shipment cost data.
2. `POST /generate` receives those values and assembles a structured payload containing `meta` and `numbers` sections.
3. The report builder computes landed-cost inputs such as merchandise value, duty impact, freight, insurance, prep cost, and other charges.
4. The PDF layer renders the final report. The application is designed to prefer richer renderers when available and fall back to simpler ReportLab output if needed.
5. The generated PDF is returned directly to the browser, and an optional delivery path can email it or write it to the local outbox.

From an engineering standpoint, the important pattern is graceful degradation. The application still produces a usable artifact even when optional rendering or delivery dependencies are missing.

## Stripe Checkout Flow

1. The frontend can call `POST /api/checkout/create-session` to start payment.
2. The service checks environment flags to determine whether the paywall is enabled.
3. In demo mode, the endpoint returns a local success URL so the workflow can be reviewed without live billing.
4. In paywalled mode, the service creates a Stripe Checkout session using `STRIPE_SECRET_KEY` and `STRIPE_PRICE_ID`.
5. Stripe redirects the user to the configured success or cancel URL after payment or abandonment.
6. A webhook endpoint at `/webhook/stripe` can receive completion events and validate signatures when `STRIPE_WEBHOOK_SECRET` is configured.

This makes the repository useful as a portfolio artifact because it shows both real-world integration boundaries and a developer-friendly local demo path.

## Health Endpoint

The application exposes `GET /__health`, which returns a small JSON response such as `{"ok": true, "status": "healthy"}`. This endpoint is intended for hosting-platform readiness checks, uptime monitors, and simple operational verification during development or deployment.
