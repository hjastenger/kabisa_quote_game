from fastapi import FastAPI
from quote.router import router as quote_router
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

logger = logging.getLogger("uvicorn.error")
logger.propagate = False

app = FastAPI()
app.include_router(quote_router)
