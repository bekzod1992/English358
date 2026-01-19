"""
Materials and Tasks handler
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.materials import get_material_content, get_task_content
from utils.db import save_completed_task

material_router = Router()


def get_back_keyboard(grade: int, menu_type: str) -> InlineKeyboardMarkup:
    """Create back button keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"{menu_type}_grade_{grade}"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])


def get_task_complete_keyboard(grade: int, topic: str) -> InlineKeyboardMarkup:
    """Create task completion keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Bajardim",
            callback_data=f"task_done_{grade}_{topic}"
        )],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"tasks_grade_{grade}"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])


# Handle material topic selection
@material_router.callback_query(F.data.startswith("materials_topic_"))
async def show_material(callback: CallbackQuery):
    """Show material content for selected topic"""
    parts = callback.data.split("_")
    grade = int(parts[2])
    topic = parts[3]

    content = get_material_content(grade, topic)

    await callback.message.edit_text(
        content,
        reply_markup=get_back_keyboard(grade, "materials"),
        parse_mode="HTML"
    )
    await callback.answer()


# Handle task topic selection
@material_router.callback_query(F.data.startswith("tasks_topic_"))
async def show_task(callback: CallbackQuery):
    """Show task content for selected topic"""
    parts = callback.data.split("_")
    grade = int(parts[2])
    topic = parts[3]

    content = get_task_content(grade, topic)

    await callback.message.edit_text(
        content,
        reply_markup=get_task_complete_keyboard(grade, topic),
        parse_mode="HTML"
    )
    await callback.answer()


# Handle task completion
@material_router.callback_query(F.data.startswith("task_done_"))
async def task_completed(callback: CallbackQuery):
    """Mark task as completed"""
    parts = callback.data.split("_")
    grade = int(parts[2])
    topic = parts[3]

    # Save to database
    save_completed_task(
        user_id=callback.from_user.id,
        task_id=f"{grade}_{topic}",
        task_type="practice",
        grade=grade
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📝 Yana topshiriq",
            callback_data=f"tasks_grade_{grade}"
        )],
        [InlineKeyboardButton(
            text="🔙 Asosiy menyu",
            callback_data="back_to_menu"
        )]
    ])

    await callback.message.edit_text(
        "✅ <b>Ajoyib! Topshiriq bajarildi!</b>\n\n"
        "Sizning natijangiz saqlandi. Davom eting! 💪",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer("Tabriklaymiz! 🎉")


# IELTS Practice handler
@material_router.callback_query(F.data == "ielts_practice")
async def show_ielts_practice(callback: CallbackQuery):
    """Show IELTS practice sections"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Reading Test", callback_data="ielts_test_reading")],
        [InlineKeyboardButton(text="🎧 Listening Tips", callback_data="ielts_material_listening")],
        [InlineKeyboardButton(text="✍️ Writing Task 1", callback_data="ielts_material_writing1")],
        [InlineKeyboardButton(text="✍️ Writing Task 2", callback_data="ielts_material_writing2")],
        [InlineKeyboardButton(text="🗣 Speaking Tips", callback_data="ielts_material_speaking")],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="menu_ielts"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])

    await callback.message.edit_text(
        "🎯 <b>IELTS Practice</b>\n\n"
        "IELTS imtihoniga tayyorlanish uchun bo'limni tanlang:\n\n"
        "• Reading - 60 daqiqa, 40 savol\n"
        "• Listening - 30 daqiqa, 40 savol\n"
        "• Writing - 60 daqiqa, 2 ta vazifa\n"
        "• Speaking - 11-14 daqiqa, 3 qism",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


# CEFR handlers
@material_router.callback_query(F.data == "cefr_a")
async def show_cefr_a(callback: CallbackQuery):
    """Show CEFR A1-A2 content"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 A1 Test", callback_data="cefr_test_a1")],
        [InlineKeyboardButton(text="📝 A2 Test", callback_data="cefr_test_a2")],
        [InlineKeyboardButton(text="📖 A1-A2 Grammar", callback_data="cefr_material_a_grammar")],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="menu_ielts"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])

    await callback.message.edit_text(
        "📜 <b>CEFR A1-A2 Darajasi</b>\n\n"
        "<b>A1 - Beginner (Boshlang'ich)</b>\n"
        "• Oddiy so'z va iboralar\n"
        "• O'zini tanishtirish\n"
        "• Kundalik mavzular\n\n"
        "<b>A2 - Elementary (Elementar)</b>\n"
        "• Oddiy jumlalar\n"
        "• Kundalik vaziyatlar\n"
        "• Asosiy grammatika",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@material_router.callback_query(F.data == "cefr_b")
async def show_cefr_b(callback: CallbackQuery):
    """Show CEFR B1-B2 content"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 B1 Test", callback_data="cefr_test_b1")],
        [InlineKeyboardButton(text="📝 B2 Test", callback_data="cefr_test_b2")],
        [InlineKeyboardButton(text="📖 B1-B2 Grammar", callback_data="cefr_material_b_grammar")],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="menu_ielts"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])

    await callback.message.edit_text(
        "📜 <b>CEFR B1-B2 Darajasi</b>\n\n"
        "<b>B1 - Intermediate (O'rta)</b>\n"
        "• Sayohat mavzulari\n"
        "• Fikr bildirish\n"
        "• Tajriba haqida gapirish\n\n"
        "<b>B2 - Upper-Intermediate</b>\n"
        "• Murakkab matnlar\n"
        "• Texnik munozaralar\n"
        "• Ravon nutq",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@material_router.callback_query(F.data == "cefr_c")
async def show_cefr_c(callback: CallbackQuery):
    """Show CEFR C1-C2 content"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 C1 Test", callback_data="cefr_test_c1")],
        [InlineKeyboardButton(text="📝 C2 Test", callback_data="cefr_test_c2")],
        [InlineKeyboardButton(text="📖 C1-C2 Advanced", callback_data="cefr_material_c_grammar")],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="menu_ielts"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])

    await callback.message.edit_text(
        "📜 <b>CEFR C1-C2 Darajasi</b>\n\n"
        "<b>C1 - Advanced (Yuqori)</b>\n"
        "• Murakkab matnlarni tushunish\n"
        "• Ravon va spontan nutq\n"
        "• Akademik va professional maqsadlar\n\n"
        "<b>C2 - Proficiency (Mukammal)</b>\n"
        "• Ona tilidek daraja\n"
        "• Har qanday mavzuda nutq\n"
        "• Murakkab nuanslarni tushunish",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


# IELTS Material handlers
@material_router.callback_query(F.data.startswith("ielts_material_"))
async def show_ielts_material(callback: CallbackQuery):
    """Show IELTS tips and materials"""
    material_type = callback.data.split("_")[-1]

    materials = {
        "listening": """
🎧 <b>IELTS Listening Tips</b>

<b>Umumiy ma'lumot:</b>
• 4 ta bo'lim, 40 ta savol
• 30 daqiqa + 10 daqiqa javoblarni ko'chirish

<b>Maslahatlar:</b>
1. Savollarni oldindan o'qing
2. Kalit so'zlarni belgilang
3. Spelling'ga e'tibor bering
4. Javobni darhol yozing
5. Yo'qotgan savolga qaytmang

<b>Savol turlari:</b>
• Multiple choice
• Matching
• Plan/Map labeling
• Form completion
• Note completion
""",
        "writing1": """
✍️ <b>IELTS Writing Task 1</b>

<b>Umumiy ma'lumot:</b>
• 150+ so'z
• 20 daqiqa
• Grafik/jadval/diagramma tavsifi

<b>Struktura:</b>
1. <b>Introduction</b> - Grafikni umumiy tasvirlang
2. <b>Overview</b> - Asosiy tendensiyalar
3. <b>Body 1</b> - Birinchi guruh ma'lumotlar
4. <b>Body 2</b> - Ikkinchi guruh ma'lumotlar

<b>Foydali iboralar:</b>
• The graph shows/illustrates...
• According to the data...
• There was a significant increase/decrease...
• The highest/lowest point was...
""",
        "writing2": """
✍️ <b>IELTS Writing Task 2</b>

<b>Umumiy ma'lumot:</b>
• 250+ so'z
• 40 daqiqa
• Essay yozish

<b>Struktura:</b>
1. <b>Introduction</b> (40-50 so'z)
   - Mavzuni paraphrase qiling
   - O'z fikringizni ayting

2. <b>Body 1</b> (80-100 so'z)
   - Topic sentence
   - Explanation
   - Example

3. <b>Body 2</b> (80-100 so'z)
   - Topic sentence
   - Explanation
   - Example

4. <b>Conclusion</b> (30-40 so'z)
   - Fikrni umumlashtiring
""",
        "speaking": """
🗣 <b>IELTS Speaking Tips</b>

<b>3 ta qism:</b>

<b>Part 1</b> (4-5 daqiqa)
• O'zingiz haqida savollar
• Qisqa, aniq javoblar
• 2-3 jumla

<b>Part 2</b> (3-4 daqiqa)
• Cue card bo'yicha gapirish
• 1 daqiqa tayyorgarlik
• 2 daqiqa gapirish

<b>Part 3</b> (4-5 daqiqa)
• Chuqur muhokama
• Fikr bildirish
• Tahlil qilish

<b>Maslahatlar:</b>
• Ravon gapiring, to'xtamang
• Fillers ishlating: Well, Actually, To be honest
• Complex structures ishlating
• Pronunciation'ga e'tibor bering
"""
    }

    content = materials.get(material_type, "Material topilmadi.")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="ielts_practice"),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])

    await callback.message.edit_text(content, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


# CEFR Material handlers
@material_router.callback_query(F.data.startswith("cefr_material_"))
async def show_cefr_material(callback: CallbackQuery):
    """Show CEFR grammar materials"""
    parts = callback.data.split("_")
    level = parts[2]  # a, b, or c

    materials = {
        "a": """
📖 <b>A1-A2 Grammar</b>

<b>A1 Grammatika:</b>
• To be (am/is/are)
• Present Simple
• Articles (a/an/the)
• Pronouns (I, you, he, she...)
• Basic prepositions (in, on, at)
• There is/There are

<b>A2 Grammatika:</b>
• Past Simple
• Future (will, going to)
• Comparatives/Superlatives
• Modal verbs (can, must, should)
• Present Continuous
• Countable/Uncountable nouns

<b>Namuna:</b>
✅ She <b>is</b> a student.
✅ I <b>went</b> to school yesterday.
✅ He <b>can</b> speak English.
""",
        "b": """
📖 <b>B1-B2 Grammar</b>

<b>B1 Grammatika:</b>
• Present Perfect
• Past Continuous
• First Conditional
• Relative clauses (who, which, that)
• Passive Voice (simple)
• Used to

<b>B2 Grammatika:</b>
• Past Perfect
• Second/Third Conditionals
• Reported Speech
• Passive (all tenses)
• Wish/If only
• Modal perfects (could have, should have)

<b>Namuna:</b>
✅ I <b>have lived</b> here for 5 years.
✅ If I <b>were</b> you, I <b>would study</b> harder.
✅ She said she <b>had finished</b> the work.
""",
        "c": """
📖 <b>C1-C2 Advanced Grammar</b>

<b>C1 Grammatika:</b>
• Mixed Conditionals
• Inversion
• Cleft sentences
• Advanced passive structures
• Subjunctive mood
• Ellipsis and substitution

<b>C2 Grammatika:</b>
• Nuanced modal usage
• Advanced clause types
• Emphatic structures
• Idiomatic expressions
• Register and style shifts

<b>Namuna:</b>
✅ <b>Had I known</b>, I would have helped. (Inversion)
✅ <b>It was John who</b> broke the window. (Cleft)
✅ <b>Not until</b> midnight <b>did</b> he arrive. (Inversion)
"""
    }

    content = materials.get(level, "Material topilmadi.")

    back_callback = f"cefr_{level}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data=back_callback),
            InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")
        ]
    ])

    await callback.message.edit_text(content, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
