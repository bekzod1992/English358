"""
Test handler - handles all test-related functionality with celebration effects
"""

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import random

from utils.db import save_test_result, save_user_progress, get_user_progress, clear_user_progress, get_user
from utils.notifications import notify_admin_test_completed

test_router = Router()

# Load tests from JSON file
TESTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tests.json")


def load_tests_data():
    """Load tests from JSON file"""
    try:
        with open(TESTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tests: {e}")
        return {}


def get_test_questions(grade: int, topic: str):
    """Get test questions for grade and topic from JSON"""
    data = load_tests_data()
    grade_str = str(grade)

    # Check in grades
    if "grades" in data and grade_str in data["grades"]:
        if topic in data["grades"][grade_str]:
            return data["grades"][grade_str][topic]

    # Check similar grades
    similar = {
        "2": "1", "3": "1", "4": "1",
        "6": "5", "7": "5",
        "9": "8",
        "11": "10"
    }
    if grade_str in similar:
        base_grade = similar[grade_str]
        if "grades" in data and base_grade in data["grades"]:
            if topic in data["grades"][base_grade]:
                return data["grades"][base_grade][topic]

    return None


def get_ielts_test(test_type: str):
    """Get IELTS test questions from JSON"""
    data = load_tests_data()
    if "ielts" in data and test_type in data["ielts"]:
        return data["ielts"][test_type]
    return None


def get_cefr_test(level: str):
    """Get CEFR test questions from JSON"""
    data = load_tests_data()
    if "cefr" in data and level in data["cefr"]:
        return data["cefr"][level]
    return None


def get_task_test(task_type: str):
    """Get task test questions from JSON"""
    data = load_tests_data()
    if "tasks" in data and task_type in data["tasks"]:
        return data["tasks"][task_type]
    return None


# Celebration effects
CELEBRATION_EFFECTS = [
    "🎉🎊🎉🎊🎉\n\n✨ <b>AJOYIB!</b> ✨\n\n🎉🎊🎉🎊🎉",
    "🎆🎇🎆🎇🎆\n\n⭐ <b>ZO'R!</b> ⭐\n\n🎆🎇🎆🎇🎆",
    "🥳🎈🥳🎈🥳\n\n🌟 <b>BARAKALLA!</b> 🌟\n\n🥳🎈🥳🎈🥳",
    "🏆✨🏆✨🏆\n\n💫 <b>MUKAMMAL!</b> 💫\n\n🏆✨🏆✨🏆",
    "🌈⭐🌈⭐🌈\n\n🎯 <b>TO'G'RI!</b> 🎯\n\n🌈⭐🌈⭐🌈",
]

WRONG_MESSAGES = [
    "😔 Afsuski noto'g'ri...",
    "❌ Noto'g'ri javob",
    "🤔 To'g'ri javob boshqacha",
    "📚 Biroz ko'proq o'qish kerak",
]


def get_celebration_message():
    """Get random celebration effect"""
    return random.choice(CELEBRATION_EFFECTS)


def get_wrong_message():
    """Get random wrong answer message"""
    return random.choice(WRONG_MESSAGES)


def get_question_keyboard(question_index: int, total: int, test_id: str) -> InlineKeyboardMarkup:
    """Create answer options keyboard"""
    options = ["A", "B", "C", "D"]
    buttons = []
    row = []

    for opt in options:
        row.append(InlineKeyboardButton(
            text=opt,
            callback_data=f"answer_{test_id}_{question_index}_{opt}"
        ))
    buttons.append(row)

    # Navigation buttons
    nav_row = []
    nav_row.append(InlineKeyboardButton(
        text="❌ Bekor qilish",
        callback_data="cancel_test"
    ))
    buttons.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_question(question: dict, index: int, total: int, correct_count: int = 0) -> str:
    """Format question for display"""
    text = f"📝 <b>Savol {index + 1}/{total}</b>\n"
    text += f"✅ To'g'ri: {correct_count}\n\n"
    text += f"<b>{question['question']}</b>\n\n"

    options = question.get("options", {})
    for key, value in options.items():
        text += f"<b>{key}.</b> {value}\n"

    return text


# Handle test topic selection
@test_router.callback_query(F.data.startswith("tests_topic_"))
async def start_test(callback: CallbackQuery):
    """Start a test for selected topic"""
    parts = callback.data.split("_")
    grade = int(parts[2])
    topic = parts[3]

    test_id = f"{grade}_{topic}"
    questions = get_test_questions(grade, topic)

    if not questions:
        await callback.message.edit_text(
            "❌ Bu mavzu bo'yicha test hali tayyor emas.\n"
            "Tez orada qo'shiladi!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"tests_grade_{grade}")]
            ])
        )
        await callback.answer()
        return

    # Clear any existing progress and start fresh
    clear_user_progress(callback.from_user.id)
    save_user_progress(callback.from_user.id, test_id, 0, 0, "{}")

    # Show first question
    question_text = format_question(questions[0], 0, len(questions), 0)
    keyboard = get_question_keyboard(0, len(questions), test_id)

    await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("Test boshlandi! Omad! 🍀")


# Handle answer selection
@test_router.callback_query(F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery, bot: Bot):
    """Process user's answer with celebration effects"""
    parts = callback.data.split("_")
    test_id = f"{parts[1]}_{parts[2]}"
    question_index = int(parts[3])
    selected_answer = parts[4]

    # Get test info
    grade, topic = test_id.split("_")
    grade = int(grade)
    questions = get_test_questions(grade, topic)

    if not questions:
        await callback.answer("Test topilmadi!")
        return

    # Get current progress
    progress = get_user_progress(callback.from_user.id)
    if progress:
        answers = json.loads(progress.get("answers", "{}"))
        correct_count = progress.get("correct_count", 0)
    else:
        answers = {}
        correct_count = 0

    # Check answer
    current_question = questions[question_index]
    correct_answer = current_question.get("correct", "A")

    is_correct = selected_answer == correct_answer
    if is_correct:
        correct_count += 1

    # Save answer
    answers[str(question_index)] = {
        "selected": selected_answer,
        "correct": correct_answer,
        "is_correct": is_correct
    }

    # Check if this is the last question
    if question_index >= len(questions) - 1:
        # Test completed - show results
        score = (correct_count / len(questions)) * 100

        # Save to database
        save_test_result(
            user_id=callback.from_user.id,
            test_id=test_id,
            grade=grade,
            topic=topic,
            correct_answers=correct_count,
            total_questions=len(questions)
        )
        clear_user_progress(callback.from_user.id)

        # Get user info for admin notification
        user = get_user(callback.from_user.id)
        full_name = user.get("full_name", "Noma'lum") if user else "Noma'lum"

        # Notify admin
        await notify_admin_test_completed(
            bot=bot,
            telegram_id=callback.from_user.id,
            full_name=full_name,
            test_name=f"{grade}-sinf {topic}",
            score=score,
            correct=correct_count,
            total=len(questions)
        )

        # Create result message with effects
        if score >= 90:
            emoji = "🏆🎉🎊"
            message = "A'lo natija! Siz juda yaxshi tayyorlangansiz!"
            effect = "🎆🎇🎆🎇🎆🎇🎆🎇🎆"
        elif score >= 70:
            emoji = "👍🌟"
            message = "Yaxshi natija! Biroz ko'proq mashq qiling."
            effect = "⭐✨⭐✨⭐"
        elif score >= 50:
            emoji = "📚💪"
            message = "O'rtacha natija. Ko'proq o'qish kerak."
            effect = "📖📚📖"
        else:
            emoji = "💪🔥"
            message = "Hafsalangiz pir bo'lmasin! Yana urinib ko'ring."
            effect = "💪🔥💪"

        result_text = f"""
{effect}

{emoji} <b>Test yakunlandi!</b>

📊 <b>Natijalaringiz:</b>

✅ To'g'ri javoblar: <b>{correct_count}/{len(questions)}</b>
📈 Ball: <b>{score:.1f}%</b>

{message}

{effect}
"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Yana test", callback_data=f"tests_grade_{grade}")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")]
        ])

        await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")

        if is_correct:
            await callback.answer("✅ To'g'ri! Test yakunlandi! 🎉", show_alert=True)
        else:
            await callback.answer(f"❌ Noto'g'ri. Javob: {correct_answer}. Test yakunlandi!", show_alert=True)

    else:
        # Move to next question
        next_index = question_index + 1
        save_user_progress(callback.from_user.id, test_id, next_index, correct_count, json.dumps(answers))

        if is_correct:
            # Show celebration effect
            celebration = get_celebration_message()
            await callback.message.edit_text(celebration, parse_mode="HTML")

            # Wait and show next question
            import asyncio
            await asyncio.sleep(1)

            next_question = questions[next_index]
            question_text = format_question(next_question, next_index, len(questions), correct_count)
            keyboard = get_question_keyboard(next_index, len(questions), test_id)
            await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
            await callback.answer("✅ To'g'ri! 🎉")
        else:
            # Show wrong message with correct answer
            wrong_text = f"""
{get_wrong_message()}

❌ Sizning javobingiz: <b>{selected_answer}</b>
✅ To'g'ri javob: <b>{correct_answer}</b>

Keyingi savolga o'tish uchun tugmani bosing.
"""
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➡️ Keyingi savol", callback_data=f"next_{test_id}_{next_index}_{correct_count}")],
                [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_test")]
            ])
            await callback.message.edit_text(wrong_text, reply_markup=keyboard, parse_mode="HTML")
            await callback.answer(f"❌ Noto'g'ri. Javob: {correct_answer}")


# Handle next question after wrong answer
@test_router.callback_query(F.data.startswith("next_"))
async def next_question(callback: CallbackQuery):
    """Show next question after wrong answer"""
    parts = callback.data.split("_")
    test_id = f"{parts[1]}_{parts[2]}"
    next_index = int(parts[3])
    correct_count = int(parts[4])

    grade, topic = test_id.split("_")
    grade = int(grade)
    questions = get_test_questions(grade, topic)

    if not questions or next_index >= len(questions):
        await callback.answer("Xatolik!")
        return

    question_text = format_question(questions[next_index], next_index, len(questions), correct_count)
    keyboard = get_question_keyboard(next_index, len(questions), test_id)

    await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


# Cancel test
@test_router.callback_query(F.data == "cancel_test")
async def cancel_test(callback: CallbackQuery):
    """Cancel current test"""
    clear_user_progress(callback.from_user.id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Testlar", callback_data="menu_tests")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        "❌ Test bekor qilindi.\n\nQaytadan urinib ko'rishingiz mumkin.",
        reply_markup=keyboard
    )
    await callback.answer()


# IELTS Test handlers
@test_router.callback_query(F.data.startswith("ielts_test_"))
async def start_ielts_test(callback: CallbackQuery):
    """Start IELTS test"""
    test_type = callback.data.split("_")[-1]
    questions = get_ielts_test(test_type)

    if not questions:
        await callback.message.edit_text(
            "❌ Bu test hali tayyor emas.\n"
            "Tez orada qo'shiladi!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="ielts_practice")]
            ])
        )
        await callback.answer()
        return

    test_id = f"ielts_{test_type}"
    clear_user_progress(callback.from_user.id)
    save_user_progress(callback.from_user.id, test_id, 0, 0, "{}")

    question_text = format_question(questions[0], 0, len(questions), 0)
    keyboard = get_ielts_question_keyboard(0, len(questions), test_id)

    await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("IELTS test boshlandi! 🎯")


def get_ielts_question_keyboard(question_index: int, total: int, test_id: str) -> InlineKeyboardMarkup:
    """Create IELTS answer options keyboard"""
    options = ["A", "B", "C", "D"]
    buttons = []
    row = []

    for opt in options:
        row.append(InlineKeyboardButton(
            text=opt,
            callback_data=f"ieltsans_{test_id}_{question_index}_{opt}"
        ))
    buttons.append(row)

    nav_row = [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_ielts_test")]
    buttons.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@test_router.callback_query(F.data.startswith("ieltsans_"))
async def process_ielts_answer(callback: CallbackQuery, bot: Bot):
    """Process IELTS test answer with effects"""
    parts = callback.data.split("_")
    test_id = f"{parts[1]}_{parts[2]}"
    question_index = int(parts[3])
    selected_answer = parts[4]

    test_type = parts[2]
    questions = get_ielts_test(test_type)

    if not questions:
        await callback.answer("Test topilmadi!")
        return

    progress = get_user_progress(callback.from_user.id)
    if progress:
        answers = json.loads(progress.get("answers", "{}"))
        correct_count = progress.get("correct_count", 0)
    else:
        answers = {}
        correct_count = 0

    current_question = questions[question_index]
    correct_answer = current_question.get("correct", "A")

    is_correct = selected_answer == correct_answer
    if is_correct:
        correct_count += 1

    answers[str(question_index)] = {
        "selected": selected_answer,
        "correct": correct_answer,
        "is_correct": is_correct
    }

    if question_index >= len(questions) - 1:
        score = (correct_count / len(questions)) * 100

        # Estimate IELTS band score
        if score >= 90:
            band = "8.0-9.0"
            effect = "🎆🎇🎆🎇🎆"
        elif score >= 80:
            band = "7.0-7.5"
            effect = "⭐✨⭐✨⭐"
        elif score >= 70:
            band = "6.0-6.5"
            effect = "👍🌟👍"
        elif score >= 60:
            band = "5.0-5.5"
            effect = "📚💪📚"
        else:
            band = "4.0-4.5"
            effect = "💪🔥💪"

        save_test_result(
            user_id=callback.from_user.id,
            test_id=test_id,
            grade=0,
            topic=f"IELTS {test_type}",
            correct_answers=correct_count,
            total_questions=len(questions)
        )
        clear_user_progress(callback.from_user.id)

        # Admin notification
        user = get_user(callback.from_user.id)
        full_name = user.get("full_name", "Noma'lum") if user else "Noma'lum"
        await notify_admin_test_completed(
            bot=bot,
            telegram_id=callback.from_user.id,
            full_name=full_name,
            test_name=f"IELTS {test_type.capitalize()}",
            score=score,
            correct=correct_count,
            total=len(questions)
        )

        result_text = f"""
{effect}

🎯 <b>IELTS {test_type.capitalize()} Test yakunlandi!</b>

📊 <b>Natijalaringiz:</b>

✅ To'g'ri javoblar: <b>{correct_count}/{len(questions)}</b>
📈 Ball: <b>{score:.1f}%</b>
🎓 Taxminiy IELTS Band: <b>{band}</b>

Bu natija faqat taxminiy bahodir.

{effect}
"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Yana IELTS", callback_data="ielts_practice")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")]
        ])

        await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")
        await callback.answer("Test yakunlandi! 🎉", show_alert=True)

    else:
        next_index = question_index + 1
        save_user_progress(callback.from_user.id, test_id, next_index, correct_count, json.dumps(answers))

        if is_correct:
            celebration = get_celebration_message()
            await callback.message.edit_text(celebration, parse_mode="HTML")

            import asyncio
            await asyncio.sleep(1)

            next_question = questions[next_index]
            question_text = format_question(next_question, next_index, len(questions), correct_count)
            keyboard = get_ielts_question_keyboard(next_index, len(questions), test_id)
            await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
            await callback.answer("✅ To'g'ri! 🎉")
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➡️ Keyingi savol", callback_data=f"ielts_next_{test_id}_{next_index}_{correct_count}")],
                [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_ielts_test")]
            ])
            await callback.message.edit_text(
                f"{get_wrong_message()}\n\n❌ Javobingiz: <b>{selected_answer}</b>\n✅ To'g'ri javob: <b>{correct_answer}</b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            await callback.answer(f"❌ Noto'g'ri. Javob: {correct_answer}")


@test_router.callback_query(F.data.startswith("ielts_next_"))
async def ielts_next_question(callback: CallbackQuery):
    """Show next IELTS question"""
    parts = callback.data.split("_")
    test_id = f"{parts[2]}_{parts[3]}"
    next_index = int(parts[4])
    correct_count = int(parts[5])

    test_type = parts[3]
    questions = get_ielts_test(test_type)

    if not questions or next_index >= len(questions):
        await callback.answer("Xatolik!")
        return

    question_text = format_question(questions[next_index], next_index, len(questions), correct_count)
    keyboard = get_ielts_question_keyboard(next_index, len(questions), test_id)

    await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@test_router.callback_query(F.data == "cancel_ielts_test")
async def cancel_ielts_test(callback: CallbackQuery):
    """Cancel IELTS test"""
    clear_user_progress(callback.from_user.id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 IELTS", callback_data="ielts_practice")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        "❌ Test bekor qilindi.",
        reply_markup=keyboard
    )
    await callback.answer()


# CEFR Test handlers
@test_router.callback_query(F.data.startswith("cefr_test_"))
async def start_cefr_test(callback: CallbackQuery):
    """Start CEFR test"""
    level = callback.data.split("_")[-1]
    questions = get_cefr_test(level)

    if not questions:
        level_group = level[0]
        await callback.message.edit_text(
            "❌ Bu test hali tayyor emas.\n"
            "Tez orada qo'shiladi!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"cefr_{level_group}")]
            ])
        )
        await callback.answer()
        return

    test_id = f"cefr_{level}"
    clear_user_progress(callback.from_user.id)
    save_user_progress(callback.from_user.id, test_id, 0, 0, "{}")

    question_text = format_question(questions[0], 0, len(questions), 0)
    keyboard = get_cefr_question_keyboard(0, len(questions), test_id)

    await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(f"CEFR {level.upper()} test boshlandi! 📜")


def get_cefr_question_keyboard(question_index: int, total: int, test_id: str) -> InlineKeyboardMarkup:
    """Create CEFR answer options keyboard"""
    options = ["A", "B", "C", "D"]
    buttons = []
    row = []

    for opt in options:
        row.append(InlineKeyboardButton(
            text=opt,
            callback_data=f"cefrans_{test_id}_{question_index}_{opt}"
        ))
    buttons.append(row)

    level = test_id.split("_")[-1]
    level_group = level[0]
    nav_row = [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_cefr_{level_group}")]
    buttons.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@test_router.callback_query(F.data.startswith("cefrans_"))
async def process_cefr_answer(callback: CallbackQuery, bot: Bot):
    """Process CEFR test answer with effects"""
    parts = callback.data.split("_")
    test_id = f"{parts[1]}_{parts[2]}"
    question_index = int(parts[3])
    selected_answer = parts[4]

    level = parts[2]
    questions = get_cefr_test(level)

    if not questions:
        await callback.answer("Test topilmadi!")
        return

    progress = get_user_progress(callback.from_user.id)
    if progress:
        answers = json.loads(progress.get("answers", "{}"))
        correct_count = progress.get("correct_count", 0)
    else:
        answers = {}
        correct_count = 0

    current_question = questions[question_index]
    correct_answer = current_question.get("correct", "A")

    is_correct = selected_answer == correct_answer
    if is_correct:
        correct_count += 1

    answers[str(question_index)] = {
        "selected": selected_answer,
        "correct": correct_answer,
        "is_correct": is_correct
    }

    if question_index >= len(questions) - 1:
        score = (correct_count / len(questions)) * 100

        save_test_result(
            user_id=callback.from_user.id,
            test_id=test_id,
            grade=0,
            topic=f"CEFR {level.upper()}",
            correct_answers=correct_count,
            total_questions=len(questions)
        )
        clear_user_progress(callback.from_user.id)

        if score >= 70:
            result = f"✅ Siz {level.upper()} darajasiga mos kelasiz!"
            effect = "🎉🎊🎉"
        else:
            result = f"📚 {level.upper()} darajasi uchun ko'proq mashq qiling."
            effect = "💪📚💪"

        # Admin notification
        user = get_user(callback.from_user.id)
        full_name = user.get("full_name", "Noma'lum") if user else "Noma'lum"
        await notify_admin_test_completed(
            bot=bot,
            telegram_id=callback.from_user.id,
            full_name=full_name,
            test_name=f"CEFR {level.upper()}",
            score=score,
            correct=correct_count,
            total=len(questions)
        )

        result_text = f"""
{effect}

📜 <b>CEFR {level.upper()} Test yakunlandi!</b>

📊 <b>Natijalaringiz:</b>

✅ To'g'ri javoblar: <b>{correct_count}/{len(questions)}</b>
📈 Ball: <b>{score:.1f}%</b>

{result}

{effect}
"""

        level_group = level[0]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📜 Yana CEFR", callback_data=f"cefr_{level_group}")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")]
        ])

        await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")
        await callback.answer("Test yakunlandi! 🎉", show_alert=True)

    else:
        next_index = question_index + 1
        save_user_progress(callback.from_user.id, test_id, next_index, correct_count, json.dumps(answers))

        if is_correct:
            celebration = get_celebration_message()
            await callback.message.edit_text(celebration, parse_mode="HTML")

            import asyncio
            await asyncio.sleep(1)

            next_question = questions[next_index]
            question_text = format_question(next_question, next_index, len(questions), correct_count)
            keyboard = get_cefr_question_keyboard(next_index, len(questions), test_id)
            await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
            await callback.answer("✅ To'g'ri! 🎉")
        else:
            level_group = level[0]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➡️ Keyingi savol", callback_data=f"cefr_next_{test_id}_{next_index}_{correct_count}")],
                [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_cefr_{level_group}")]
            ])
            await callback.message.edit_text(
                f"{get_wrong_message()}\n\n❌ Javobingiz: <b>{selected_answer}</b>\n✅ To'g'ri javob: <b>{correct_answer}</b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            await callback.answer(f"❌ Noto'g'ri. Javob: {correct_answer}")


@test_router.callback_query(F.data.startswith("cefr_next_"))
async def cefr_next_question(callback: CallbackQuery):
    """Show next CEFR question"""
    parts = callback.data.split("_")
    test_id = f"{parts[2]}_{parts[3]}"
    next_index = int(parts[4])
    correct_count = int(parts[5])

    level = parts[3]
    questions = get_cefr_test(level)

    if not questions or next_index >= len(questions):
        await callback.answer("Xatolik!")
        return

    question_text = format_question(questions[next_index], next_index, len(questions), correct_count)
    keyboard = get_cefr_question_keyboard(next_index, len(questions), test_id)

    await callback.message.edit_text(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@test_router.callback_query(F.data.startswith("cancel_cefr_"))
async def cancel_cefr_test(callback: CallbackQuery):
    """Cancel CEFR test"""
    level_group = callback.data.split("_")[-1]
    clear_user_progress(callback.from_user.id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 CEFR", callback_data=f"cefr_{level_group}")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        "❌ Test bekor qilindi.",
        reply_markup=keyboard
    )
    await callback.answer()
