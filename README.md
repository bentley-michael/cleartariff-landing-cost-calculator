# ClearTariff

ClearTariff is a FastAPI-based landed cost and duty calculator for Amazon sellers that generates a structured PDF report and routes users through a Stripe checkout flow.

## Features

- Landed cost calculator
- HS code duty estimation
- Freight / insurance / cost modeling
- Per-unit landed cost calculation
- PDF report generation
- Stripe checkout integration
- Demo mode for local testing

## Screenshots

### Homepage
![Homepage](docs/screenshots/home.png)

### Calculator Form
![Calculator](docs/screenshots/calculator-form.png)

### Generated PDF Report
![PDF](docs/screenshots/pdf-report.png)

### Checkout Success
![Success](docs/screenshots/success.png)

### Checkout Cancel
![Cancel](docs/screenshots/cancel.png)

## Demo Flow

1. User opens calculator
2. User enters shipment details
3. App calculates landed cost
4. PDF report is generated
5. Stripe checkout or demo redirect occurs
6. Success confirmation page appears

## Tech Stack

- Python
- FastAPI
- Stripe Checkout
- HTML/CSS frontend
- Railway deployment
- Optional Docker support

## Architecture

User
  ↓
FastAPI Web App
  ↓
Landed Cost Calculator
  ↓
PDF Report Generator
  ↓
Stripe Checkout
  ↓
Success / Cancel Redirect

## Local Development

```bash
python -m venv .venv
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

## Environment Variables

APP_URL  
SUCCESS_URL  
CANCEL_URL  
STRIPE_SECRET_KEY  
STRIPE_PUBLISHABLE_KEY  
DEMO_MODE  
ENABLE_LIVE_RATES  
ENABLE_PDF  
ENABLE_EMAIL

## Example API Payload

```json
{
	"meta": {
		"product_name": "Stainless Steel Coffee Tumbler",
		"hs_code": "3924.10.4000",
		"market": "US",
		"country_of_origin": "CN",
		"buyer": "Northwind Commerce",
		"seller": "Shenzhen Sample Manufacturing"
	},
	"numbers": {
		"duty_rate_pct": 7.5,
		"units": 1000,
		"unit_value_usd": 2.75,
		"freight_usd": 500.0,
		"insurance_usd": 25.0,
		"other_costs_usd": 75.0,
		"fba_prep_usd": 0.35
	}
}
```
