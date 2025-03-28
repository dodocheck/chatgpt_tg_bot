from openai import AsyncOpenAI
import httpx
from dotenv import load_dotenv
import os
from typing import Tuple

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))


async def ask_chatgpt(request: list[dict], model: str) -> Tuple[str | None, int]:
    """Gets a response from chatgpt

    Args:
        request (list[dict]): chat context
        model (str): ai model name from API

    Returns:
        Tuple[str | None, int]: answer as str, tokens spent for answer
    """
    response = await client.chat.completions.create(
        messages=request,
        model=model
    )
    return response.choices[0].message.content, response.usage.total_tokens
