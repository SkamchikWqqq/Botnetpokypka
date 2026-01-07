import asyncio

import aiosqlite
import os
from datetime import datetime, timedelta

DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database/database.db')

async def checkUser(userid):
    print(f"Checking user {userid} in the database...")  # Логируем проверку пользователя
    async with aiosqlite.connect(DIRECTORY) as con:
        async with con.execute("""
        SELECT userid FROM users WHERE userid = ?""", (userid,)) as cur:
            row = await cur.fetchone()
            if row:  # Пользователь найден
                print(f"User {userid} found")  # Логируем, что пользователь найден
                return True
            print(f"User {userid} not found, creating new user")  # Логируем, что пользователь не найден
            await newUser(userid)  # Создаем нового пользователя
            return False

async def newUser(userid):
    async with aiosqlite.connect(DIRECTORY) as con:
        await con.execute("""
        INSERT INTO users (userid, sub, date) VALUES (?, ?, ?)""", (userid, False, None))
        await con.commit()  # Сохраняем изменения
        print(f"New user {userid} added to the database")  # Логируем создание нового пользователя

async def giveSub(userid, days):
    date = datetime.now() + timedelta(days=int(days))
    async with aiosqlite.connect(DIRECTORY) as con:
        await con.execute("""
        UPDATE users SET sub = ?, date = ? WHERE userid = ?
        """, (True, date.isoformat(), userid))
        await con.commit()
        print(f"Subscription given to {userid} for {days} days")  # Логируем выдачу подписки

async def closeSub(userid):
    async with aiosqlite.connect(DIRECTORY) as con:
        await con.execute("""
        UPDATE users SET sub = ?, date = ? WHERE userid = ?
        """, (False, None, userid))
        await con.commit()
        print(f"Subscription closed for user {userid}")  # Логируем закрытие подписки

async def createDatabase():
    async with aiosqlite.connect(DIRECTORY) as con:
        await con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userid INTEGER PRIMARY KEY,
            sub BOOLEAN,
            date REAL
        )""")  # Используем REAL для хранения isoformat
        await con.commit()

async def checkSubStatus(userid):
    async with aiosqlite.connect(DIRECTORY) as con:
        async with con.execute("""
        SELECT sub FROM users WHERE userid = ?""", (userid,)) as cur:
            row = await cur.fetchone()
            if row:
                subStatus = bool(row[0])
                return subStatus
            return False  # Пользователь не найден

async def checkSubDate(userid):
    async with aiosqlite.connect(DIRECTORY) as con:
        async with con.execute("""
        SELECT date FROM users WHERE userid = ?""", (userid,)) as cur:
            row = await cur.fetchone()
            if row and row[0]:  # Если дата подписки существует
                expiration_date = datetime.fromisoformat(row[0])
                if expiration_date <= datetime.now():
                    await closeSub(userid)  # Закрываем подписку, если истекла
                    return False  # Подписка истекла
                return True  # Подписка активна
            return False  # Пользователь не найден или дата отсутствует
async def subDate(userid):
    async with aiosqlite.connect(DIRECTORY) as con:
        async with con.execute("""
        SELECT date FROM users WHERE userid = ?""", (userid,)) as cur:
            row = await cur.fetchone()
            if row and row[0]:  # Если дата подписки существует
                expiration_date = datetime.fromisoformat(row[0])
                return expiration_date

