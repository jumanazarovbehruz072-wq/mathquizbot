import asyncio
import logging
import os
import random
import sqlite3
from contextlib import closing

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from keep_alive import keep_alive
from questions import QUESTIONS

# --- SOZLAMALAR ---------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8836382323:AAGEhh9Y_62008kz7_2GbWQKbuxLsXQu5p4")
DB_PATH = "quiz.db"
QUESTIONS_PER_ROUND = 10  # har bir o'yinda nechta savol berilsin

logging.basicConfig(level=logging.INFO)
router = Router()


# --- MA'LUMOTLAR BAZASI --------------------------------------------------
def init_db() -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                best_score INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0
            )
            """
        )
        conn.commit()


def save_result(user_id: int, username: str, score: int) -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute(
            "SELECT best_score FROM scores WHERE user_id = ?", (user_id,)
        )
        row = cur.fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO scores (user_id, username, best_score, games_played) "
                "VALUES (?, ?, ?, 1)",
                (user_id, username, score),
            )
        else:
            best = max(row[0], score)
            conn.execute(
                "UPDATE scores SET username = ?, best_score = ?, "
                "games_played = games_played + 1 WHERE user_id = ?",
                (username, best, user_id),
            )
        conn.commit()


def get_top(limit: int = 10):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute(
            "SELECT username, best_score FROM scores "
            "ORDER BY best_score DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()


# --- HOLATLAR (FSM) -------------------------------------------------------
class QuizState(StatesGroup):
    in_progress = State()


# --- YORDAMCHI FUNKSIYALAR -------------------------------------------------
def build_question_keyboard(options: list[str], q_index: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=f"ans:{q_index}:{i}")]
        for i, opt in enumerate(options)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def send_question(message_target, state: FSMContext, edit: bool = False):
    data = await state.get_data()
    order = data["order"]
    pos = data["pos"]
    question = QUESTIONS[order[pos]]
    text = f"❓ Savol {pos + 1}/{len(order)}\n\n{question['question']}"
    kb = build_question_keyboard(question["options"], pos)

    if edit:
        await message_target.edit_text(text, reply_markup=kb)
    else:
        await message_target.answer(text, reply_markup=kb)


# --- HANDLERLAR -------------------------------------------------------
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Salom! Men matematika fanidan test botiman.\n\n"
        "📋 Buyruqlar:\n"
        "/quiz — testni boshlash\n"
        "/top — eng yaxshi natijalar\n\n"
        f"Har bir o'yinda {QUESTIONS_PER_ROUND} ta tasodifiy savol beriladi. Omad!"
    )


@router.message(Command("quiz"))
async def cmd_quiz(message: Message, state: FSMContext):
    total = len(QUESTIONS)
    n = min(QUESTIONS_PER_ROUND, total)
    order = random.sample(range(total), n)

    await state.set_state(QuizState.in_progress)
    await state.update_data(order=order, pos=0, score=0)

    await message.answer(f"🎯 Test boshlandi! {n} ta savol, omad tilayman!")
    await send_question(message, state)


@router.callback_query(F.data.startswith("ans:"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state != QuizState.in_progress.state:
        await callback.answer("Bu test allaqachon tugagan.", show_alert=True)
        return

    data = await state.get_data()
    order = data["order"]
    pos = data["pos"]
    score = data["score"]

    _, q_idx_str, opt_idx_str = callback.data.split(":")
    q_idx = int(q_idx_str)
    opt_idx = int(opt_idx_str)

    if q_idx != pos:
        await callback.answer("Bu savol allaqachon javoblangan.", show_alert=True)
        return

    question = QUESTIONS[order[pos]]
    correct_idx = question["correct"]
    is_correct = opt_idx == correct_idx

    if is_correct:
        score += 1
        feedback = "✅ To'g'ri!"
    else:
        correct_text = question["options"][correct_idx]
        feedback = f"❌ Noto'g'ri. To'g'ri javob: {correct_text}"

    await callback.answer(feedback, show_alert=False)

    pos += 1
    await state.update_data(pos=pos, score=score)

    if pos < len(order):
        await send_question(callback.message, state, edit=True)
    else:
        username = callback.from_user.username or callback.from_user.full_name
        save_result(callback.from_user.id, username, score)
        await state.clear()
        percent = round(score / len(order) * 100)
        await callback.message.edit_text(
            f"🏁 Test tugadi!\n\n"
            f"Natija: {score}/{len(order)} ({percent}%)\n\n"
            f"Yana urinish uchun /quiz buyrug'ini yuboring."
        )


@router.message(Command("top"))
async def cmd_top(message: Message):
    rows = get_top(10)
    if not rows:
        await message.answer("Hozircha hech kim test ishlamagan. Birinchi bo'ling! /quiz")
        return

    lines = ["🏆 Eng yaxshi natijalar:\n"]
    medals = ["🥇", "🥈", "🥉"]
    for i, (username, best_score) in enumerate(rows):
        prefix = medals[i] if i < 3 else f"{i + 1}."
        name = username or "Foydalanuvchi"
        lines.append(f"{prefix} {name} — {best_score} ball")

    await message.answer("\n".join(lines))


# --- ISHGA TUSHIRISH -------------------------------------------------------
async def main():
    if BOT_TOKEN == "BU_YERGA_TOKEN_NI_QOYING":
        raise RuntimeError(
            "BOT_TOKEN sozlanmagan! README.md faylidagi ko'rsatmaga qarang."
        )

    init_db()
    keep_alive()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
