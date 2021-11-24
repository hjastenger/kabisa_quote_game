from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quote.service import QuoteService

router = APIRouter(prefix='/quote')


class RandomQuoteResponse(BaseModel):
    quote: str
    author: str


@router.get('/', response_model=RandomQuoteResponse)
async def quote():
    quote_result = await QuoteService.fetch_and_create_quote()

    if quote_result.success:
        return quote_result.data

    # For the sake of simplicity just treat every 'upstream' issue as temporary.
    return HTTPException(status_code=503, detail=quote_result.error_msg)
