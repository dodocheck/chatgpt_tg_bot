from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from loguru import logger

from app.generators import ask_chatgpt
from app.states import Chat

max_tokens = 3000

user = Router()

context = {}  # {user_id: chat context}

ai_model = 'o3-mini-2025-01-31'


@user.message(Command('clear'))
async def cmd_clear(message: Message) -> None:
    """Clears chat context

    Args:
        message (Message): message_obj from user
    """
    context[message.from_user.id] = []
    context[message.from_user.id].append({'role': 'system',
                                          'content': 'answer in the same language I asked you. Desired response output format: If the user query is asking for a knowledge-based answer or is specifying a data processing or coding task, immediately proceed to the direct answer written as though it was a document. There will be no additional chatty dialog from the AI unless the user is directly conversing with the AI with a chat style. AI should appear to be a data processor, not a chat partner. Keep in mind that you answers will be delivered to me as telegram messages. Answer in detail but try to avoid huge answers.'})
    await message.react([{"type": "emoji", "emoji": "👌"}])


@user.message(Chat.busy)
async def answer_that_busy(message: Message) -> None:
    """If user sends another message before AI answers

    Args:
        message (Message): message_obj from user
    """
    await message.react([{"type": "emoji", "emoji": "👨‍💻"}])


@user.message(F.text)
async def get_chatgpt_response(message: Message, state: FSMContext) -> None:
    """Writes a response to user's message

    Args:
        message (Message): message_obj from user
        state (FSMContext): state of the user
    """

    await state.set_state(Chat.busy)

    try:
        if message.from_user.id not in context:
            context[message.from_user.id] = []
            context[message.from_user.id].append({'role': 'system',
                                                  'content': 'answer in the same language I asked you. Desired response output format: If the user query is asking for a knowledge-based answer or is specifying a data processing or coding task, immediately proceed to the direct answer written as though it was a document. There will be no additional chatty dialog from the AI unless the user is directly conversing with the AI with a chat style. AI should appear to be a data processor, not a chat partner. Keep in mind that you answers will be delivered to me as telegram messages. Answer in detail but try to avoid huge answers.'})

        context[message.from_user.id].append({'role': 'user',
                                              'content': message.text})

        await message.react([{"type": "emoji", "emoji": "✍️"}])
        
        response, tokens_used = await ask_chatgpt(context[message.from_user.id], ai_model)

        if tokens_used > max_tokens: # compressing context to 1 message to control tokens spending
            msg = 'Сделай короткий пересказ нашего диалога от третьего лица. Себя называй как Бот, а меня - Пользователь'
            context[message.from_user.id].append({'role': 'user',
                                                  'content': msg})
            summary, tokens_used = await ask_chatgpt(context[message.from_user.id], ai_model)
            context[message.from_user.id] = []
            context[message.from_user.id].append({'role': 'system',
                                                  'content': summary})

        context[message.from_user.id].append({'role': 'assistant',
                                              'content': response})

        await message.answer(response, parse_mode='Markdown')

    except Exception as error:
        logger.error(f'Error: {error}')

    await state.clear()
