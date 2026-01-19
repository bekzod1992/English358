"""
Start and Help command handlers with registration flow
"""

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from utils.db import add_user, get_user, get_user_stats, is_user_registered, complete_registration, update_user_grade, get_daily_top_users, get_weekly_top_users
from utils.states import RegistrationStates
from utils.notifications import notify_admin_new_user

start_router = Router()


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Create main menu inline keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 O'quv materiallari", callback_data="menu_materials")],
        [InlineKeyboardButton(text="📝 Testlar", callback_data="menu_tests")],
        [InlineKeyboardButton(text="🧠 Amaliy topshiriqlar", callback_data="menu_tasks")],
        [InlineKeyboardButton(text="🎯 IELTS va Sertifikatlar", callback_data="menu_ielts")],
        [InlineKeyboardButton(text="📊 Mening natijalarim", callback_data="menu_stats")],
        [InlineKeyboardButton(text="🏆 Reyting", callback_data="menu_leaderboard")],
        [InlineKeyboardButton(text="⚙️ Sinfni o'zgartirish", callback_data="menu_change_grade")]
    ])
    return keyboard


def get_home_button_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard with just home button"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")]
    ])
    return keyboard


def get_leaderboard_text() -> str:
    """Generate leaderboard text with daily and weekly top users"""
    daily_top = get_daily_top_users(3)
    weekly_top = get_weekly_top_users(10)

    text = ""

    # Daily top 3
    if daily_top:
        text += "📅 <b>Bugungi TOP 3:</b>\n"
        medals = ["🥇", "🥈", "🥉"]
        for i, user in enumerate(daily_top):
            medal = medals[i] if i < 3 else f"{i+1}."
            name = user.get('full_name', 'Noma\'lum')
            tests = user.get('tests_count', 0)
            avg = user.get('avg_score', 0)
            text += f"{medal} {name} - {tests} ta test, {avg}%\n"
        text += "\n"

    # Weekly top
    if weekly_top:
        text += "📆 <b>Haftalik TOP:</b>\n"
        for i, user in enumerate(weekly_top):
            if i < 3:
                medals = ["🥇", "🥈", "🥉"]
                prefix = medals[i]
            else:
                prefix = f"{i+1}."
            name = user.get('full_name', 'Noma\'lum')
            tests = user.get('tests_count', 0)
            avg = user.get('avg_score', 0)
            text += f"{prefix} {name} - {tests} ta test, {avg}%\n"

    if not daily_top and not weekly_top:
        text = "📊 Hozircha reyting bo'sh. Birinchi bo'lib test yeching!\n"

    return text


def get_grade_selection_keyboard() -> InlineKeyboardMarkup:
    """Create grade selection keyboard"""
    buttons = []
    row = []
    for i in range(1, 12):
        row.append(InlineKeyboardButton(text=f"{i}-sinf", callback_data=f"grade_{i}"))
        if len(row) == 4 or i == 11:
            buttons.append(row)
            row = []
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Create phone request keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


@start_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    """Handle /start command"""
    user = message.from_user

    # Add user to database (initial)
    add_user(telegram_id=user.id, username=user.username)

    # Check if user is already registered
    if is_user_registered(user.id):
        # User is registered, show main menu
        db_user = get_user(user.id)

        welcome_text = f"""
🎓 <b>358-maktab Ingliz tili botiga xush kelibsiz!</b>

Assalomu alaykum, <b>{db_user.get('full_name', user.first_name)}</b>! 👋

Bu bot sizga ingliz tilini o'rganishda yordam beradi:
• 📘 Sinf bo'yicha o'quv materiallari
• 📝 Interaktiv testlar
• 🧠 Amaliy mashqlar
• 🎯 IELTS va boshqa sertifikat testlari

"""
        # Add leaderboard
        leaderboard = get_leaderboard_text()
        welcome_text += leaderboard + "\n"

        if db_user and db_user.get("grade"):
            welcome_text += f"📚 Sizning sinfingiz: <b>{db_user['grade']}-sinf</b>\n\n"
            welcome_text += "Quyidagi bo'limlardan birini tanlang:"
            await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
        else:
            welcome_text += "Iltimos, avval sinfingizni tanlang:"
            await message.answer(welcome_text, reply_markup=get_grade_selection_keyboard(), parse_mode="HTML")
    else:
        # User not registered, start registration
        welcome_text = f"""
🎓 <b>358-maktab Ingliz tili botiga xush kelibsiz!</b>

Assalomu alaykum, <b>{user.first_name}</b>! 👋

Botdan foydalanish uchun ro'yxatdan o'ting.

📱 <b>Iltimos, telefon raqamingizni yuboring:</b>

Quyidagi tugmani bosing:
"""
        await message.answer(
            welcome_text,
            reply_markup=get_phone_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(RegistrationStates.waiting_for_phone)


@start_router.message(RegistrationStates.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone number from contact"""
    phone = message.contact.phone_number

    # Save phone to state
    await state.update_data(phone=phone)

    await message.answer(
        "✅ Telefon raqam qabul qilindi!\n\n"
        "👤 <b>Endi ism va familiyangizni yozing:</b>\n\n"
        "Masalan: <i>Aliyev Vali</i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(RegistrationStates.waiting_for_name)


@start_router.message(RegistrationStates.waiting_for_phone)
async def process_phone_text(message: Message, state: FSMContext):
    """Process phone number as text"""
    phone = message.text.strip()

    # Simple validation
    if not phone or len(phone) < 9:
        await message.answer(
            "❌ Noto'g'ri format!\n\n"
            "📱 Iltimos, telefon raqamingizni to'g'ri kiriting yoki tugmani bosing:",
            reply_markup=get_phone_keyboard()
        )
        return

    # Save phone to state
    await state.update_data(phone=phone)

    await message.answer(
        "✅ Telefon raqam qabul qilindi!\n\n"
        "👤 <b>Endi ism va familiyangizni yozing:</b>\n\n"
        "Masalan: <i>Aliyev Vali</i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(RegistrationStates.waiting_for_name)


@start_router.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext, bot: Bot):
    """Process full name"""
    full_name = message.text.strip()

    if not full_name or len(full_name) < 3:
        await message.answer(
            "❌ Ism juda qisqa!\n\n"
            "👤 Iltimos, to'liq ism va familiyangizni yozing:"
        )
        return

    # Get phone from state
    data = await state.get_data()
    phone = data.get("phone", "")

    user = message.from_user

    # Complete registration in database
    complete_registration(
        telegram_id=user.id,
        phone=phone,
        full_name=full_name
    )

    # Notify admin about new user
    await notify_admin_new_user(
        bot=bot,
        telegram_id=user.id,
        username=user.username,
        phone=phone,
        full_name=full_name
    )

    # Clear state
    await state.clear()

    # Show success and grade selection
    await message.answer(
        f"🎉 <b>Tabriklaymiz, {full_name}!</b>\n\n"
        "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n\n"
        "📚 Endi sinfingizni tanlang:",
        reply_markup=get_grade_selection_keyboard(),
        parse_mode="HTML"
    )


@start_router.callback_query(F.data.startswith("grade_"))
async def process_grade_selection(callback: CallbackQuery):
    """Process grade selection"""
    grade = int(callback.data.split("_")[1])

    update_user_grade(callback.from_user.id, grade)

    await callback.message.edit_text(
        f"✅ Siz <b>{grade}-sinf</b>ni tanladingiz!\n\n"
        "Endi quyidagi bo'limlardan birini tanlang:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@start_router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = """
📖 <b>Yordam - 358-maktab Ingliz tili boti</b>

<b>Asosiy buyruqlar:</b>
/start - Botni ishga tushirish
/help - Yordam olish
/menu - Asosiy menyuni ko'rish
/stats - Statistikani ko'rish

<b>Bo'limlar:</b>

📘 <b>O'quv materiallari</b>
Sinf bo'yicha ingliz tili darsliklari va qo'shimcha materiallar

📝 <b>Testlar</b>
Sinf va mavzu bo'yicha test savollari. Har bir testdan keyin natijangiz saqlanadi.

🧠 <b>Amaliy topshiriqlar</b>
Grammatika, lug'at va boshqa amaliy mashqlar

🎯 <b>IELTS va Sertifikatlar</b>
IELTS, CEFR va boshqa xalqaro imtihonlarga tayyorlanish uchun namunaviy testlar

📊 <b>Mening natijalarim</b>
O'zingizning test natijalari va statistikangizni ko'ring

<b>Test yechish:</b>
1. Testni tanlang
2. Har bir savolga javob bering (A, B, C, D)
3. Test oxirida natijangizni ko'ring

✅ To'g'ri javob - salyut effekti!
❌ Noto'g'ri javob - to'g'ri javob ko'rsatiladi

Savollar bo'lsa @admin ga yozing!
"""
    await message.answer(help_text, parse_mode="HTML")


@start_router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Handle /menu command"""
    if not is_user_registered(message.from_user.id):
        await message.answer(
            "⚠️ Avval ro'yxatdan o'ting!\n\n/start buyrug'ini yuboring.",
            parse_mode="HTML"
        )
        return

    await message.answer(
        "📋 <b>Asosiy menyu</b>\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@start_router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Handle /stats command"""
    if not is_user_registered(message.from_user.id):
        await message.answer(
            "⚠️ Avval ro'yxatdan o'ting!\n\n/start buyrug'ini yuboring.",
            parse_mode="HTML"
        )
        return

    stats = get_user_stats(message.from_user.id)
    user = get_user(message.from_user.id)

    stats_text = f"""
📊 <b>Sizning statistikangiz</b>

👤 Ism: <b>{user.get('full_name', 'Noma\'lum')}</b>
📚 Sinf: <b>{user.get('grade', 0)}-sinf</b>

📝 Yechilgan testlar: <b>{stats['total_tests']}</b>
📈 O'rtacha ball: <b>{stats['avg_score']}%</b>
✅ Bajarilgan topshiriqlar: <b>{stats['total_tasks']}</b>
"""
    await message.answer(stats_text, parse_mode="HTML")


@start_router.callback_query(F.data == "menu_stats")
async def show_stats(callback: CallbackQuery):
    """Show user statistics"""
    stats = get_user_stats(callback.from_user.id)
    user = get_user(callback.from_user.id)

    stats_text = f"""
📊 <b>Sizning statistikangiz</b>

👤 Ism: <b>{user.get('full_name', 'Noma\'lum') if user else 'Noma\'lum'}</b>
📚 Sinf: <b>{user.get('grade', 0) if user else 0}-sinf</b>

📝 Yechilgan testlar: <b>{stats['total_tests']}</b>
📈 O'rtacha ball: <b>{stats['avg_score']}%</b>
✅ Bajarilgan topshiriqlar: <b>{stats['total_tasks']}</b>
"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(stats_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@start_router.callback_query(F.data == "menu_change_grade")
async def change_grade(callback: CallbackQuery):
    """Change user's grade"""
    await callback.message.edit_text(
        "📚 Yangi sinfingizni tanlang:",
        reply_markup=get_grade_selection_keyboard()
    )
    await callback.answer()


@start_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Go back to main menu"""
    db_user = get_user(callback.from_user.id)

    welcome_text = "📋 <b>Asosiy menyu</b>\n\n"

    # Add leaderboard
    leaderboard = get_leaderboard_text()
    welcome_text += leaderboard + "\n"

    if db_user and db_user.get("grade"):
        welcome_text += f"📚 Sizning sinfingiz: <b>{db_user['grade']}-sinf</b>\n\n"

    welcome_text += "Quyidagi bo'limlardan birini tanlang:"

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@start_router.callback_query(F.data == "menu_leaderboard")
async def show_leaderboard(callback: CallbackQuery):
    """Show full leaderboard"""
    leaderboard = get_leaderboard_text()

    text = "🏆 <b>Reyting</b>\n\n" + leaderboard

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
