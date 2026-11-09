# Collections agent backend

Python backend for the AI collections agent: accounts, policies, calls, and the
safety guardrails from [`../safety-guard`](../safety-guard) wrapped around the AI model.

It runs end to end **without any vendor accounts**. Every external service (speech,
AI model, voice, SMS, CRM, payments) has a mock, and you swap in real vendors by
changing one line in `.env`.

## Start in 2 minutes (local)

From this `backend/` folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
pip install ../safety-guard -r requirements-dev.txt
cp .env.example .env              # Windows PowerShell: copy .env.example .env
python -m app.seed                # approved policy + 3 sample accounts
uvicorn app.main:create_app --factory --reload
```

Open **http://localhost:8000/docs**. Every endpoint can be tried from the browser
there. Click "Authorize" and enter the `API_KEY` from `.env` (default `change-me`).

`.env.example` sets `CLOCK_OVERRIDE` so the app thinks it's Monday 10:00. Without
it, the calling-hours rule blocks calls in the evening, which is correct behaviour
but confusing while you are testing.

## Try a call

```bash
KEY="X-API-Key: change-me"; URL=http://localhost:8000

curl -s -H "$KEY" -H "Content-Type: application/json" -X POST $URL/calls -d '{"account_id":"ACC-1001"}'
# -> {"call_id":"call_...","agent_text":"Just so you know, I'm an automated assistant. Hello, am I speaking with Daniel Hughes?", ...}

ID=call_...   # paste the call_id
curl -s -H "$KEY" -H "Content-Type: application/json" -X POST $URL/calls/$ID/turns -d '{"text":"Yes, speaking."}'
curl -s -H "$KEY" -H "Content-Type: application/json" -X POST $URL/calls/$ID/turns -d '{"text":"14/03/1990, LS6 1AB"}'
curl -s -H "$KEY" -H "Content-Type: application/json" -X POST $URL/calls/$ID/turns -d '{"text":"I lost my job, I cant afford much"}'
curl -s -H "$KEY" -H "Content-Type: application/json" -X POST $URL/calls/$ID/turns -d '{"text":"Yes, that works."}'
curl -s -H "$KEY" $URL/calls/$ID       # transcript, AI drafts vs what was said, plan, audit check
```

The mock AI model always proposes 2 × £120. After "I lost my job", the offer guard
replaces that with 4 × £60, the plan the customer can afford. The terminal running
uvicorn shows what each provider did (dial, speak, SMS, CRM update, payment link).

Things to try:

- Account `ACC-1003` is disputed, so it is blocked before dialling.
- Say "I don't want to live anymore": the call escalates to a human and the AI is skipped.
- Send `"confidence": 0.4` with a turn: the agent asks the customer to repeat.

## Run with Docker (Postgres + API + worker)

```bash
cp .env.example .env
docker compose up --build
docker compose exec api python -m app.seed
```

## How it fits together

```
                 ┌──────────── app/api (HTTP) ────────────┐
 lender systems ─┤ /accounts/import   /policies   /calls  ├── /webhooks/voice/{provider} ◄─ telephony
                 └───────────────────┬─────────────────────┘
                                     ▼
                     app/services/conversation.py
          load session ─► guardrails pipeline ─► AI model ─► guards ─► speak
                │                 │                                     │
        app/state.py       ../safety-guard                    app/providers/*
     (live call state)     (rules, audit chain)        STT · LLM · TTS · voice · SMS · CRM · payments
                │                                                       ▲
                └──────── database (app/models.py) ◄────────────────────┘
                                     ▲
                         app/worker.py ─ scheduler: who is due for a call
```

| Folder / file | What it does |
|---|---|
| `app/config.py` | Every setting, read from `.env` |
| `app/registry.py` | The registry pattern: name in config → class |
| `app/providers/base.py` | Interfaces for each external service, one registry each |
| `app/providers/mock.py` | Mock implementations (default) |
| `app/providers/_template.py` | Copy this to add a real vendor |
| `app/bootstrap.py` | Builds the providers, DB and state store from settings |
| `app/state.py` | Live call state between turns (`memory` or `database`) |
| `app/prompts.py` | What the AI model sees each turn |
| `app/services/conversation.py` | The turn loop with guards around the model |
| `app/services/policies.py` | Rulebook versions with two-person approval |
| `app/services/scheduler.py` | Picks accounts due for contact; expires stale calls |
| `app/api/*` | HTTP routes |
| `app/worker.py` | Background loop that starts outbound calls |
| `app/models.py` | Database tables |

## Registries: swapping a vendor

Each external dependency is an interface with a registry:

```python
# app/providers/base.py
LLMS: Registry[LanguageModel] = Registry("llm")

# app/providers/mock.py
@LLMS.register("mock")
class MockLLM(LanguageModel):
    def generate(self, request: LLMRequest) -> LLMReply: ...

# app/bootstrap.py
llm = LLMS.create(settings.llm_provider, settings=settings)
```

To add a real vendor:

1. Copy `app/providers/_template.py` to `app/providers/<vendor>_llm.py` and implement `generate()`.
2. Import it in `app/providers/__init__.py`.
3. Set `LLM_PROVIDER=<vendor>` and its keys in `.env`.

The same steps work for `STT`, `TTS`, `VOICE`, `MESSAGING`, `CRMS`, `PAYMENTS`, and
the state store. `GET /providers` shows which implementation is active and which are
available.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness + database check (no key needed) |
| GET | `/providers` | Active and available implementations |
| POST | `/accounts/import` | Create/update accounts (lender's file or sync) |
| GET | `/accounts`, `/accounts/{id}` | List / read (never returns DOB or postcode) |
| POST | `/policies` | Draft a new rulebook version |
| POST | `/policies/{version}/approve` | Approve. Must be a different person from the author |
| GET | `/policies`, `/policies/active` | List / current |
| POST | `/calls` | Pre-call gate, dial, opening line |
| POST | `/calls/{id}/turns` | Customer says something → agent reply |
| POST | `/calls/{id}/hangup` | End the call |
| GET | `/calls/{id}` | Transcript with AI drafts, plan, audit-chain check |
| POST | `/webhooks/voice/{provider}` | Telephony events (signed by the vendor, no API key) |

## Tests

```bash
pytest -q
```

They cover the full call flow, crisis escalation, blocked accounts, low-confidence
speech, two-person policy approval, the worker, and auth. CI runs them on every
push (`.github/workflows/backend.yml`).

## Before going live

- [ ] Real vendor adapters for telephony (streaming audio), STT, TTS and the AI model
- [ ] Verify webhook signatures per vendor (`app/deps.py: verify_webhook_signature`)
- [ ] Postgres with backups; Alembic migrations instead of `create_all()`
- [ ] Encrypt DOB and postcode at rest; secrets in a vault, not `.env`
- [ ] Remove `CLOCK_OVERRIDE`; set `ENVIRONMENT=production` and a strong `API_KEY`
- [ ] Redis state store and a proper job queue once call volume grows
- [ ] Real time zones and public holidays per market (see `safety-guard` roadmap)
- [ ] Monitoring: escalation rate, guard triggers per rule, model error rate, latency per turn
