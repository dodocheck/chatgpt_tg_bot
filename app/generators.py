from openai import AsyncOpenAI
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'),
                     http_client=httpx.AsyncClient(proxy=os.getenv('PROXY'),
                                                   transport=httpx.HTTPTransport(local_address='0.0.0.0')))


async def ask_chatgpt(request, model):
    response = await client.chat.completions.create(
        messages=request,
        model=model
    )
    return response.choices[0].message.content, response.usage.total_tokens
