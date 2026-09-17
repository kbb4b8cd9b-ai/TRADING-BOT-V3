# Trading AI v3 — Final Starter

Sistema multi-agente con dashboard mobile, Paper Trading, Risk Engine e architettura multi-broker.

## Stato
- PAPER TRADING: attivo di default
- Capitale virtuale: 50 €
- LIVE: disabilitato nel pacchetto starter
- API keys: mai nel frontend
- Trading 212: adapter predisposto
- IBKR: adapter predisposto

## Avvio
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Apri poi `http://127.0.0.1:8000`.

## Nota
Il progetto non promette né garantisce trasformazioni di capitale. Prima dell'uso con denaro reale vanno verificati broker, strumenti, costi, limiti API, logica di rischio e test in demo.
