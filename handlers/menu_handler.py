"""
Menu navigation handler
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db import get_user

menu_router = Router()


def get_grade_menu_keyboard(menu_type: str) -> InlineKeyboardMarkup:
    """Create grade selection for specific menu"""
    buttons = []
    row = []
    for i in range(1, 12):
        row.append(InlineKeyboardButton(
            text=f"{i}-sinf",
            callback_data=f"{menu_type}_grade_{i}"
        ))
        if len(row) == 4 or i == 11:
            buttons.append(row)
            row = []
    buttons.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_topic_keyboard(grade: int, menu_type: str) -> InlineKeyboardMarkup:
    """Create topic selection keyboard based on grade"""
    # Topics vary by grade level
    if grade <= 4:
        topics = [
            ("🔤 Alifbo va harflar", "alphabet"),
            ("🔢 Sonlar", "numbers"),
            ("🎨 Ranglar", "colors"),
            ("👨‍👩‍👧‍👦 Oila", "family"),
            ("🍎 Mevalar va sabzavotlar", "fruits"),
            ("🐾 Hayvonlar", "animals"),
        ]
    elif grade <= 7:
        topics = [
            ("📝 Present Simple", "present_simple"),
            ("📝 Present Continuous", "present_continuous"),
            ("📝 Past Simple", "past_simple"),
            ("📖 Reading Comprehension", "reading"),
            ("✍️ Writing", "writing"),
            ("🗣 Speaking", "speaking"),
        ]
    elif grade <= 9:
        topics = [
            ("📝 Present Perfect", "present_perfect"),
            ("📝 Past Perfect", "past_perfect"),
            ("📝 Future Tenses", "future"),
            ("📝 Conditionals", "conditionals"),
            ("📝 Passive Voice", "passive"),
            ("📖 Reading & Vocabulary", "reading_vocab"),
        ]
    else:  # 10-11 grades
        topics = [
            ("📝 Advanced Grammar", "advanced_grammar"),
            ("📝 Conditionals (All types)", "conditionals_adv"),
            ("📝 Reported Speech", "reported_speech"),
            ("📖 Academic Reading", "academic_reading"),
            ("✍️ Essay Writing", "essay"),
            ("🎧 Listening Skills", "listening"),
        ]

    buttons = []
    for topic_name, topic_id in topics:
        buttons.append([InlineKeyboardButton(
            text=topic_name,
            callback_data=f"{menu_type}_topic_{grade}_{topic_id}"
        )])

    buttons.append([
        InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"menu_{menu_type.replace('_grade', '')}"),
        InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Materials menu
@menu_router.callback_query(F.data == "menu_materials")
async def show_materials_menu(callback: CallbackQuery):
    """Show materials grade selection"""
    user = get_user(callback.from_user.id)
    current_grade = user.get("grade", 1) if user else 1

    await callback.message.edit_text(
        f"📘 <b>O'quv materiallari</b>\n\n"
        f"Hozirgi sinfingiz: <b>{current_grade}-sinf</b>\n\n"
        "Sinf tanlang:",
        reply_markup=get_grade_menu_keyboard("materials"),
        parse_mode="HTML"
    )
    await callback.answer()


# Tests menu
@menu_router.callback_query(F.data == "menu_tests")
async def show_tests_menu(callback: CallbackQuery):
    """Show tests grade selection"""
    user = get_user(callback.from_user.id)
    current_grade = user.get("grade", 1) if user else 1

    await callback.message.edit_text(
        f"📝 <b>Testlar</b>\n\n"
        f"Hozirgi sinfingiz: <b>{current_grade}-sinf</b>\n\n"
        "Sinf tanlang:",
        reply_markup=get_grade_menu_keyboard("tests"),
        parse_mode="HTML"
    )
    await callback.answer()


# Tasks menu
@menu_router.callback_query(F.data == "menu_tasks")
async def show_tasks_menu(callback: CallbackQuery):
    """Show practical tasks grade selection"""
    user = get_user(callback.from_user.id)
    current_grade = user.get("grade", 1) if user else 1

    await callback.message.edit_text(
        f"🧠 <b>Amaliy topshiriqlar</b>\n\n"
        f"Hozirgi sinfingiz: <b>{current_grade}-sinf</b>\n\n"
        "Sinf tanlang:",
        reply_markup=get_grade_menu_keyboard("tasks"),
        parse_mode="HTML"
    )
    await callback.answer()


# IELTS menu
@menu_router.callback_query(F.data == "menu_ielts")
async def show_ielts_menu(callback: CallbackQuery):
    """Show IELTS and certificates menu"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 IELTS Practice", callback_data="ielts_practice")],
        [InlineKeyboardButton(text="📜 CEFR A1-A2", callback_data="cefr_a")],
        [InlineKeyboardButton(text="📜 CEFR B1-B2", callback_data="cefr_b")],
        [InlineKeyboardButton(text="📜 CEFR C1-C2", callback_data="cefr_c")],
        [InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        "🎯 <b>IELTS va Sertifikatlar</b>\n\n"
        "Xalqaro imtihonlarga tayyorlanish uchun namunaviy testlar.\n\n"
        "Bo'limni tanlang:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


# Process grade selection for materials
@menu_router.callback_query(F.data.startswith("materials_grade_"))
async def materials_grade_selected(callback: CallbackQuery):
    """Handle materials grade selection"""
    grade = int(callback.data.split("_")[-1])

    await callback.message.edit_text(
        f"📘 <b>{grade}-sinf O'quv materiallari</b>\n\n"
        "Mavzuni tanlang:",
        reply_markup=get_topic_keyboard(grade, "materials"),
        parse_mode="HTML"
    )
    await callback.answer()


# Process grade selection for tests
@menu_router.callback_query(F.data.startswith("tests_grade_"))
async def tests_grade_selected(callback: CallbackQuery):
    """Handle tests grade selection"""
    grade = int(callback.data.split("_")[-1])

    await callback.message.edit_text(
        f"📝 <b>{grade}-sinf Testlar</b>\n\n"
        "Mavzuni tanlang:",
        reply_markup=get_topic_keyboard(grade, "tests"),
        parse_mode="HTML"
    )
    await callback.answer()


# Process grade selection for tasks
@menu_router.callback_query(F.data.startswith("tasks_grade_"))
async def tasks_grade_selected(callback: CallbackQuery):
    """Handle tasks grade selection"""
    grade = int(callback.data.split("_")[-1])

    await callback.message.edit_text(
        f"🧠 <b>{grade}-sinf Amaliy topshiriqlar</b>\n\n"
        "Mavzuni tanlang:",
        reply_markup=get_topic_keyboard(grade, "tasks"),
        parse_mode="HTML"
    )
    await callback.answer()
