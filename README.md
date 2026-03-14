# Stripe Checkout Integration with FastAPI

Backend demo showing how a Python service integrates with the **Stripe API** to create Checkout sessions and process payment events using webhook verification.

This repository demonstrates common patterns used in **API integration and fintech backend systems**.

---

## Key Features

* Stripe Checkout session creation
* Secure Stripe webhook verification
* FastAPI modular router architecture
* Environment-based configuration
* Local development with Uvicorn

---

## Core Endpoints

### Create Checkout Session

```
POST /api/checkout/create-session
```

Creates a Stripe Checkout session and redirects the user to Stripe's hosted payment page.

---

### Stripe Webhook

```
POST /webhook/stripe
```

Receives and verifies Stripe webhook events.

Currently processes:

```
checkout.session.completed
```

This event is typically used to trigger order fulfillment or account upgrades.

---

## Payment Flow

```
Client
  ↓
FastAPI Backend
  ↓
Stripe Checkout Session
  ↓
Stripe Hosted Payment Page
  ↓
Stripe Webhook Event
  ↓
FastAPI Webhook Handler
```

---

## Tech Stack

* Python
* FastAPI
* Stripe Python SDK
* Uvicorn
* Environment variables (.env)

---

## Local Setup

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure:

```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PRICE_ID=price_...
STRIPE_WEBHOOK_SECRET=whsec_...

SUCCESS_URL=http://localhost:8000/success
CANCEL_URL=http://localhost:8000/cancel
ENABLE_PAYWALL=true
```

Run the server:

```
python -m uvicorn app.main:app --reload
```

Open API docs:

```
http://127.0.0.1:8000/docs
```

---

## Purpose

This project demonstrates backend integration patterns used in **payment systems, SaaS products, and fintech platforms**.
