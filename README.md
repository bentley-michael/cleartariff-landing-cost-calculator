# Stripe Checkout Integration with FastAPI

Production-style demo showing how a backend service integrates with Stripe Checkout and processes webhook events using FastAPI.

## Features

• Stripe Checkout session creation  
• Secure webhook endpoint verification  
• FastAPI modular router architecture  
• Environment variable configuration  
• Local development with Uvicorn

## API Endpoints

POST /api/checkout/create-session  
POST /webhook/stripe

## Flow

User → FastAPI → Stripe Checkout → Stripe Webhook → FastAPI webhook handler