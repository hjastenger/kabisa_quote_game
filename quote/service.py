from typing import Optional, List

from pydantic import BaseModel

from postgres import transactional
from quote.infra.storm_quote_api import QuoteAPI
from quote.models import Quote, QuoteRepository


class QuoteDetails(BaseModel):
    author: str
    quote: str


class FetchQuoteResult(BaseModel):
    success: bool = True
    data: Optional[QuoteDetails] = None
    error_msg: Optional[str] = None


class GetQuoteListResult(BaseModel):
    quote_list: List[QuoteDetails] = []


class QuoteService:

    @staticmethod
    @transactional()
    async def fetch_and_create_quote() -> FetchQuoteResult:
        fetch_quote_result = await QuoteAPI.fetch_random_quote()

        if fetch_quote_result[0] == 200:
            new_quote: Quote = Quote(
                author=fetch_quote_result[1]['author'],
                quote_text=fetch_quote_result[1]['quote']
            )

            QuoteRepository.save(new_quote)

            return FetchQuoteResult(data=QuoteDetails(
                author=new_quote.author, quote=new_quote.quote_text)
            )

        return FetchQuoteResult(success=False, error_msg=f'Upstream API service responded with {fetch_quote_result[0]}')

    @staticmethod
    async def get_quotes(limit=1) -> GetQuoteListResult:
        aggregates = QuoteRepository.get_quotes(limit=limit)
        return GetQuoteListResult(
            quote_list=[QuoteDetails(
                author=q.author, quote=q.quote_text)
                for q in aggregates]
        )
