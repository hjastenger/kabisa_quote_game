# Kabisa Quote Assignment

Quote game based on the 'memory' spell.

## Install & Run dependencies
Docker deps (flyway & postgres):
- docker-compose up

Python deps:
- Setup virtual env: virtualenv --python=python3.10 .envs/python3
- Install reqs: pip install -r requirements (and prob test_requirements if running test suite)

## Run Application
- Run app with uvicorn: `uvicorn app:app --reload --no-access-log`
- Make sure to have atleast 8 quotes in db: `curl http://127.0.0.1:8000/quote/`
- View api docs at `127.0.0.1:8000/docs`
- Play the game using both `/game/` and `/game/guess` endpoints

## Run tests
- pytest -m "not end_to_end" .