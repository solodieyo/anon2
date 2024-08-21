from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    await _set_default_ru_commands(bot)
    await _set_default_en_commands(bot)
    await _set_default_de_commands(bot)
    await _set_default_uk_commands(bot)


async def _set_default_ru_commands(bot: Bot):
    commands = [

        BotCommand(command="start", description="Меню"),
        BotCommand(command="profile", description="Профиль"),
        BotCommand(command="language", description="Изменить язык"),
        BotCommand(command="premium", description="Премиум"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
        language_code='ru'
    )


async def _set_default_en_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Menu"),
        BotCommand(command="profile", description="Profile"),
        BotCommand(command="language", description="Change language"),
        BotCommand(command="premium", description="Premium"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
        language_code='en'
    )


async def _set_default_uk_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Меню"),
        BotCommand(command="profile", description="Профіль"),
        BotCommand(command="language", description="Змінити мову"),
        BotCommand(command="premium", description="Преміум"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
        language_code='uk'
    )

async def _set_default_de_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Menü"),
        BotCommand(command="profile", description="Profil"),
        BotCommand(command="language", description="Sprache ändern"),
        BotCommand(command="premium", description="Premium"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
        language_code='de'
    )
