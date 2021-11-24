from typing import Tuple
import aiohttp


class QuoteAPI:

    url = 'http://quotes.stormconsultancy.co.uk'

    @classmethod
    async def fetch_random_quote(cls) -> Tuple[int, dict[str, str]]:
        async with aiohttp.ClientSession() as client:
            async with client.get(f"{cls.url}/random.json") as response:
                if response.status == 200:
                    api_result = await response.json()
                    response_data = {
                        'author': api_result['author'],
                        'quote': api_result['quote']
                        }
                else:
                    response_data = {
                        'error_msg': f"Failed to fetch quote, API returned {response.status}"
                    }

                return response.status, response_data
