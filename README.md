# Investing Copilot

AI-assisted portfolio-level analytics software that combines deterministic quantitative analysis with natural-language explanations provided by AI.

> **Project status:** Active development / personal project.
>
> The backend, portfolio data model, and core analytics pipeline are functional and under active development. The frontend is currently an early-stage prototype. The project is not intended for production use or investment advice.

## Overview

Investing Copilot is a personal project for analysing investment portfolios at the portfolio level rather than focusing on individual assets.

The application builds portfolios from transaction data and combines them with market data to calculate quantitative performance and risk metrics such as returns, volatility, drawdown, Value at Risk, and the Sharpe ratio.

An LLM layer is used to translate structured quantitative results into plain-language explanations. A core design principle of the project is that the LLM does not calculate the financial metrics itself. The quantitative analysis is performed deterministically in Python using libraries such as pandas and NumPy, after which the structured results are provided to the LLM for interpretation.

## Architecture and AI Pipeline

The backend is built with FastAPI and uses PostgreSQL for portfolio and application data storage. It exposes a REST API for the frontend.

Portfolio analysis starts from transaction data, which is used to construct holdings and portfolio values over time. The application combines this information with historical market-price data retrieved through a separate market-data provider interface.

The resulting portfolio time series is then passed to the quantitative analytics layer, where performance and risk metrics are calculated deterministically in Python.

These calculated results are converted into a structured analysis context before being passed to the AI layer. The language model therefore receives predefined metrics and relevant portfolio information rather than being responsible for calculating the financial figures itself.

The AI layer is separated from the quantitative analytics logic and uses an adapter architecture designed to support multiple LLM providers. OpenAI is currently supported.

Market-data access follows a similar provider-based architecture, allowing the underlying data source to be changed without tightly coupling it to the portfolio analytics logic. Yahoo Finance is currently used as the primary market-data source.

## Why I Built This

I am interested in investing, quantitative analysis, and the use of AI as an interface for complex information.

Many portfolio tools either present raw metrics or focus mainly on portfolio value and individual holdings. I wanted to experiment with a system that first performs quantitative portfolio-level analysis and then uses AI to make the results easier to understand.

The project has also been a way for me to learn backend architecture, financial data processing, databases, and AI integration by building a larger application from scratch.

## Current Features

### Portfolio Data

* User and portfolio management
* Transaction storage and processing
* Nordnet transaction data parsing
* Position and holdings calculation
* Historical market-price retrieval

### Quantitative Analytics

* Portfolio NAV calculation
* Cash-flow-adjusted returns
* Cumulative and log returns
* Volatility
* Drawdown and maximum drawdown
* Value at Risk (VaR)
* Conditional Value at Risk (CVaR)
* Sharpe ratio

### AI Explanations

* Structured analytics context generation
* Provider-independent LLM adapter architecture
* OpenAI integration
* Prompt templates for portfolio analysis
* Validation layer for LLM responses

### Application

* FastAPI REST backend
* User authentication
* PostgreSQL data model and database migrations
* Early-stage Next.js / TypeScript frontend

## Tech Stack

### Backend

* Python
* FastAPI
* pandas
* NumPy
* SQLAlchemy
* PostgreSQL
* Alembic

### Frontend

* Next.js
* React
* TypeScript

### AI

* OpenAI API
* Provider-independent LLM adapter architecture
* Structured prompt and context pipeline

### Data

* Yahoo Finance market data
* Nordnet transaction data import

## Demo Flow

The current end-to-end demo flow covers:

* Registering and logging in as a user
* Creating portfolios
* Searching stocks from the backend stock universe
* Adding buy/sell transactions
* Viewing portfolio positions
* Generating AI explanations from calculated portfolio analytics

## Running Locally

### Backend

Create a backend environment and install dependencies:

```bash
cd backend
python -m venv venv
venv/bin/pip install -r requirements.txt
```

Create local backend environment variables from the example file:

```bash
cp backend/.env.example backend/.env
```

Start PostgreSQL with Docker:

```bash
docker compose up -d db
```

Start the FastAPI server:

```bash
cd backend
venv/bin/uvicorn app.main:app --reload
```

The API is available at:

```text
http://localhost:8000/api/v1
```

FastAPI docs are available at:

```text
http://localhost:8000/docs
```

### Frontend

Install dependencies and start the Next.js development server:

```bash
cd frontend/my-app
npm ci
npm run dev
```

The frontend runs at:

```text
http://localhost:3000
```

Local frontend environment:

```bash
cp frontend/my-app/.env.local.example frontend/my-app/.env.local
```

## Environment Variables

The backend expects these variables in `backend/.env`. See `backend/.env.example` for placeholders:

```text
APP_SECRET_KEY=change-me
APP_DATABASE_URL=postgresql+psycopg://myapp_user:myapp_password@localhost:5433/myapp_dev
APP_ENVIRONMENT=development
APP_ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_REFRESH_TOKEN_EXPIRE_DAYS=7
APP_OPENAI_API_KEY=optional-for-ai-explanations
```

The frontend expects `NEXT_PUBLIC_API_URL` in `frontend/my-app/.env.local`. See `frontend/my-app/.env.local.example`.

## Tests

Run the backend test suite:

```bash
cd backend
PYTHONPATH=. venv/bin/python -m pytest
```

Run the frontend checks:

```bash
cd frontend/my-app
npm ci
npm run lint
npm run build
```

## Current Limitations

This project is still under active development.

* The frontend is currently an early-stage prototype.
* The frontend transaction list still uses mock data because the backend currently exposes transaction creation but not a transaction-list endpoint.
* Analytics coverage is still limited compared with the intended final scope.
* Market-data handling and portfolio import workflows require further hardening.
* The AI layer currently focuses mainly on explaining existing quantitative analytics rather than performing autonomous portfolio analysis.
* The application has not been hardened for production deployment.
* Error handling, testing, and deployment workflows are still being developed.

## Planned Development

The main areas I intend to explore next include:

* Benchmark comparison and portfolio attribution
* Broader portfolio risk and performance analytics
* Improved portfolio-level visualisations
* More flexible transaction and portfolio import workflows
* More advanced AI-assisted interpretation of portfolio analytics
* Improved frontend and user experience

## Disclaimer

Investing Copilot is an experimental personal project and is not intended to provide financial or investment advice. Any analytics or AI-generated explanations should be treated as informational only.
