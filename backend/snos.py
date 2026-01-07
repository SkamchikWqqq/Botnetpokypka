from telethon import TelegramClient
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import InputReportReasonSpam
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from config import API_HASH, API_ID
import os
import asyncio

DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sessions')

async def report(link):
    username, message_id = link.split('/')[-2], link.split('/')[-1]
    message_id = int(message_id)
    sessions = [session for session in os.listdir(DIRECTORY) if session.endswith('.session')]
    
    if not sessions:
        return "Нет сессий"
    
    successful_reports = 0
    errors = []
    for session in sessions:
        print(f"Используется сессия: {session}")
        
        client = TelegramClient(os.path.join(DIRECTORY, session), API_ID, API_HASH)
        
        try:
            await client.connect()

            if not await client.is_user_authorized():
                print(f"Сессия {session} не авторизована. Пропускаем...")
                continue

            chat = await client.get_entity(username)
                
            await client(ReportRequest(
                peer=chat,
                id=[message_id],
                reason=InputReportReasonSpam(),
                message=''
            ))
            print(f"Жалоба отправлена с сессии {session}")
            successful_reports += 1

        except SessionPasswordNeededError:
            print(f"Сессия {session} требует пароль (двухфакторная аутентификация). Пропускаем...")
        except PhoneCodeInvalidError:
            print(f"Сессия {session} требует код. Пропускаем...")
        except Exception as e:
            errors.append(f"Ошибка с сессией {session}: {repr(e)}")
        finally:
            await client.disconnect()
    
    error_message = f"Ошибки: {', '.join(errors)}" if errors else "0"
    return f"✅ Успешно отправлено: {successful_reports}\n ❌ Ошибок:{error_message}"
