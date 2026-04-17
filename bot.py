"""
╔══════════════════════════════════════════════════╗
║   OILAVIY BILIM O'YINI — TELEGRAM BOT            ║
║   بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ        ║
╚══════════════════════════════════════════════════╝
"""

import asyncio
import random
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from questions import QUESTIONS
from database import init_db, get_or_create_user, add_score, get_top_users, get_user_stats

# ─── CONFIG ───────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "8792670802:AAGDy59JOFk0vcz3qIb3e-qQm_q1qsdkKVI")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ─── STATES ───────────────────────────────────────
class QuizState(StatesGroup):
    choosing_mode     = State()
    choosing_category = State()
    in_quiz           = State()
    waiting_next      = State()

# ─── CATEGORIES ───────────────────────────────────
CATEGORIES = {
    "oila":        ("💍", "Nikoh & Oila"),
    "axloq":       ("🌿", "Axloq & Hayot"),
    "quron":       ("📖", "Qur'on & Hadis"),
    "psixologiya": ("🧠", "Psixologiya"),
    "mixed":       ("🎲", "Aralash (hammasi)"),
}

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

# ─── HELPERS ──────────────────────────────────────
def make_inline(buttons: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def main_menu_kb():
    return make_inline([
        [InlineKeyboardButton(text="🎯 O'yin boshlash", callback_data="start_game")],
        [InlineKeyboardButton(text="🏆 Reyting",        callback_data="leaderboard")],
        [InlineKeyboardButton(text="📊 Mening natijam", callback_data="my_stats")],
        [InlineKeyboardButton(text="ℹ️ Loyiha haqida",  callback_data="about")],
    ])

def category_kb():
    buttons = []
    for key, (emoji, name) in CATEGORIES.items():
        buttons.append([InlineKeyboardButton(
            text=f"{emoji} {name}", callback_data=f"cat_{key}"
        )])
    return make_inline(buttons)

def answer_kb(q_index: int, options: list):
    letters = ["A", "B", "D", "E"]
    buttons = []
    for i, opt in enumerate(options):
        buttons.append([InlineKeyboardButton(
            text=f"{letters[i]}. {opt[:40]}",
            callback_data=f"ans_{q_index}_{i}"
        )])
    return make_inline(buttons)

def next_kb():
    return make_inline([
        [InlineKeyboardButton(text="Keyingi savol ›", callback_data="next_q")]
    ])

def finish_kb():
    return make_inline([
        [InlineKeyboardButton(text="🔄 Yana o'ynash",    callback_data="start_game")],
        [InlineKeyboardButton(text="🏆 Reyting ko'rish", callback_data="leaderboard")],
        [InlineKeyboardButton(text="🏠 Bosh menyu",      callback_data="main_menu")],
    ])

# ─── START ────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    get_or_create_user(msg.from_user.id, msg.from_user.username, msg.from_user.full_name)

    text = (
        "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n\n"
        "🌙 *Oilaviy Bilim O'yiniga xush kelibsiz!*\n\n"
        "Bu o'yin oilangizni birlashtiradi, ilmga muhabbat uyg'otadi.\n"
        "Har savol — hayotiy, islomiy va psixologik.\n\n"
        "📖 50 ta savol • 3 qatlam • Hadis va oyatlar\n\n"
        "_\"Ilm izlash har bir musulmonga farzdir\"_\n"
        "— Ibn Moja rivoyati"
    )
    await msg.answer(text, parse_mode="Markdown", reply_markup=main_menu_kb())

# ─── MAIN MENU ────────────────────────────────────
@dp.callback_query(F.data == "main_menu")
async def cb_main_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n\n"
        "🌙 *Oilaviy Bilim O'yini*\n\n"
        "Nima qilmoqchisiz?"
    )
    await cb.message.edit_text(text, parse_mode="Markdown", reply_markup=main_menu_kb())

# ─── START GAME ───────────────────────────────────
@dp.callback_query(F.data == "start_game")
async def cb_start_game(cb: CallbackQuery, state: FSMContext):
    await state.set_state(QuizState.choosing_category)
    text = (
        "🎯 *Mavzu tanlang:*\n\n"
        "💍 Nikoh & Oila — oilaviy munosabatlar\n"
        "🌿 Axloq & Hayot — kundalik hayot saboqlari\n"
        "📖 Qur'on & Hadis — diniy bilimlar\n"
        "🧠 Psixologiya — inson va munosabatlar\n"
        "🎲 Aralash — hammasi birga!"
    )
    await cb.message.edit_text(text, parse_mode="Markdown", reply_markup=category_kb())

# ─── CATEGORY CHOSEN ──────────────────────────────
@dp.callback_query(F.data.startswith("cat_"))
async def cb_category(cb: CallbackQuery, state: FSMContext):
    category = cb.data.replace("cat_", "")

    if category == "mixed":
        qs = QUESTIONS.copy()
    else:
        qs = [q for q in QUESTIONS if q["category"] == category]

    if not qs:
        await cb.answer("Bu kategoriyada savol yo'q!")
        return

    random.shuffle(qs)
    quiz_questions = qs[:10]  # 10 ta savol

    await state.update_data(
        questions=quiz_questions,
        current=0,
        score=0,
        correct=0,
        category=category,
        answered=False
    )
    await state.set_state(QuizState.in_quiz)
    await cb.message.edit_text("⏳ Tayyorlanmoqda...")
    await send_question(cb.message, state)

# ─── SEND QUESTION ────────────────────────────────
async def send_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    questions = data["questions"]
    idx = data["current"]
    q = questions[idx]
    total = len(questions)

    # Layer badge
    layer_badges = {1: "🟢 1-qatlam", 2: "🟡 2-qatlam", 3: "🔵 3-qatlam"}
    layer_text = layer_badges.get(q["layer"], "🟢")

    # Progress bar
    progress = int((idx / total) * 10)
    bar = "█" * progress + "░" * (10 - progress)

    text = (
        f"{layer_text} • {q['cat_emoji']} {q['cat_name']}\n"
        f"[{bar}] {idx+1}/{total}\n\n"
    )

    if q.get("scenario"):
        text += f"📖 _{q['scenario']}_\n\n"

    text += f"*{q['question']}*"

    await state.update_data(answered=False)
    await msg.answer(
        text,
        parse_mode="Markdown",
        reply_markup=answer_kb(idx, q["options"])
    )

# ─── ANSWER ───────────────────────────────────────
@dp.callback_query(F.data.startswith("ans_"))
async def cb_answer(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data.get("answered"):
        await cb.answer("⏳ Allaqachon javob berildi!", show_alert=False)
        return

    parts = cb.data.split("_")
    q_idx = int(parts[1])
    chosen = int(parts[2])

    current = data["current"]
    if q_idx != current:
        await cb.answer("Bu eski savol!")
        return

    questions = data["questions"]
    q = questions[current]
    correct_idx = q["correct"]
    is_correct = (chosen == correct_idx)

    score = data["score"]
    correct_count = data["correct"]
    points = 0

    if is_correct:
        points = 10
        score += points
        correct_count += 1
        result_emoji = "✅"
        result_text = f"To'g'ri! *+{points} ball* 🎉"
    else:
        letters = ["A", "B", "D", "E"]
        result_emoji = "❌"
        result_text = f"Noto'g'ri. To'g'ri javob: *{letters[correct_idx]}. {q['options'][correct_idx]}*"

    await state.update_data(
        score=score,
        correct=correct_count,
        answered=True
    )

    # Source type
    is_ayat = "Qur'on" in q["source"] or "oyat" in q["source"]
    source_emoji = "📖" if is_ayat else "📿"

    feedback = (
        f"{result_emoji} {result_text}\n\n"
        f"{source_emoji} *{q['source']}*\n"
        f"_{q['arabic']}_\n\n"
        f"📝 {q['translation']}\n\n"
        f"💡 {q['explanation']}"
    )

    # Check if last question
    is_last = (current + 1) >= len(questions)

    if is_last:
        next_button = make_inline([
            [InlineKeyboardButton(text="🏆 Natijalarni ko'rish", callback_data="show_results")]
        ])
    else:
        next_button = next_kb()

    await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(feedback, parse_mode="Markdown", reply_markup=next_button)
    await cb.answer()

# ─── NEXT QUESTION ────────────────────────────────
@dp.callback_query(F.data == "next_q")
async def cb_next(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current = data["current"] + 1
    await state.update_data(current=current, answered=False)
    await send_question(cb.message, state)

# ─── RESULTS ──────────────────────────────────────
@dp.callback_query(F.data == "show_results")
async def cb_results(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    correct = data["correct"]
    total = len(data["questions"])

    # Save to DB
    add_score(cb.from_user.id, score, correct, total)

    pct = int((correct / total) * 100)

    if pct >= 90:
        rank = "🌟 Bilimdon Champion!"
        msg_text = "Ajoyib! Siz haqiqiy bilimdon!"
    elif pct >= 70:
        rank = "🏅 Yaxshi natija!"
        msg_text = "Zo'r! Davom eting!"
    elif pct >= 50:
        rank = "📚 O'rtacha"
        msg_text = "Yaxshi boshlanish! Yana o'rganamiz."
    else:
        rank = "🌱 Boshlang'ich"
        msg_text = "Keling, birga o'rganamiz!"

    progress = int((correct / total) * 10)
    bar = "🟩" * progress + "⬜" * (10 - progress)

    text = (
        f"🏆 *O'yin yakunlandi!*\n\n"
        f"{rank}\n"
        f"_{msg_text}_\n\n"
        f"📊 *Natijalar:*\n"
        f"✅ To'g'ri: *{correct}/{total}*\n"
        f"⭐ Ball: *{score}*\n"
        f"📈 Foiz: *{pct}%*\n\n"
        f"{bar}\n\n"
        f"🤲 _\"Ilm izlash har bir musulmonga farzdir\"_"
    )

    await cb.message.answer(text, parse_mode="Markdown", reply_markup=finish_kb())
    await state.clear()

# ─── LEADERBOARD ──────────────────────────────────
@dp.callback_query(F.data == "leaderboard")
async def cb_leaderboard(cb: CallbackQuery):
    top = get_top_users(10)

    if not top:
        text = "🏆 *Reyting hali bo'sh*\n\nBirinchi o'yinchi bo'ling!"
    else:
        text = "🏆 *Eng bilimdon o'yinchilar:*\n\n"
        for i, (name, score, games, correct) in enumerate(top):
            medal = MEDALS[i] if i < len(MEDALS) else f"{i+1}."
            pct = int((correct / max(games * 10, 1)) * 100)
            text += f"{medal} *{name}*\n   ⭐ {score} ball • {pct}% to'g'ri\n\n"

    back_kb = make_inline([
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")]
    ])
    await cb.message.edit_text(text, parse_mode="Markdown", reply_markup=back_kb)

# ─── MY STATS ─────────────────────────────────────
@dp.callback_query(F.data == "my_stats")
async def cb_my_stats(cb: CallbackQuery):
    user = get_user_stats(cb.from_user.id)

    if not user:
        text = "📊 Siz hali o'ynamagansiz. Birinchi o'yinni boshlang!"
    else:
        _, _, name, total_score, games, correct, joined = user
        pct = int((correct / max(games * 10, 1)) * 100)
        text = (
            f"📊 *{name}ning natijalari:*\n\n"
            f"🎮 O'yinlar: *{games}*\n"
            f"⭐ Jami ball: *{total_score}*\n"
            f"✅ To'g'ri javoblar: *{correct}*\n"
            f"📈 O'rtacha: *{pct}%*\n\n"
            f"_Davom eting — har kuni o'rganib boring!_ 🌱"
        )

    back_kb = make_inline([
        [InlineKeyboardButton(text="🎯 O'ynash", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")],
    ])
    await cb.message.edit_text(text, parse_mode="Markdown", reply_markup=back_kb)

# ─── ABOUT ────────────────────────────────────────
@dp.callback_query(F.data == "about")
async def cb_about(cb: CallbackQuery):
    text = (
        "ℹ️ *Oilaviy Bilim O'yini haqida*\n\n"
        "Bu loyiha oilalarni birlashtirish, ilmga muhabbat uyg'otish "
        "maqsadida yaratilgan.\n\n"
        "🟢 *1-qatlam* — Hayotiy stsenariylar\n"
        "🟡 *2-qatlam* — Psixologiya + Islom\n"
        "🔵 *3-qatlam* — Qur'on & Hadis chuqurligi\n\n"
        "📖 50 ta savol\n"
        "💍 4 ta mavzu kategoriyasi\n"
        "🏆 Reyting tizimi\n\n"
        "_\"Yaxshilik va taqvo yo'lida bir-biringizga yordam bering\"_\n"
        "— Al-Ma'ida surasi, 2-oyat\n\n"
        "وَتَعَاوَنُوا عَلَى الْبِرِّ وَالتَّقْوَىٰ"
    )

    back_kb = make_inline([
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")]
    ])
    await cb.message.edit_text(text, parse_mode="Markdown", reply_markup=back_kb)

# ─── MAIN ─────────────────────────────────────────
async def main():
    init_db()
    print("✅ Bot ishga tushdi — Bismillah!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
