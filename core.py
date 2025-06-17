# реально кор
# украдено из моего секретного репозитория
# никто его не увидит

import discord
from discord.ext import commands
from discord import app_commands
import json
import logging
import os
import asyncio

# КРУТОЙ ЛОГГЕР
import logging
import sys

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # blue
        'INFO': '\033[92m',     # green
        'WARNING': '\033[93m',  # yellow
        'ERROR': '\033[91m',    # red
        'CRITICAL': '\033[1;91m',  # uhhh pizdec red
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)

def setup_logger(name: str = __name__) -> logging.Logger:
    formatter = ColoredFormatter(
        fmt="[{asctime}] {levelname} - {name}: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) 
    logger.addHandler(handler)
    logger.propagate = False

    return logger

logger = setup_logger(__name__)



TOKEN = os.getenv('DISCORD_TOKEN')

class CoreBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.loaded_cogs_status = {} # Для отслеживания статуса когов

    async def setup_hook(self):
        """Выполняется перед запуском бота для загрузки когов."""
        self.logger.info("Запускаю setup_hook для загрузки начальных когов...")
        # ОНО ПРОПАЛО СОЗДАЕТ СНОВА
        if not os.path.exists("cogs"):
            os.makedirs("cogs")
            self.logger.info("на лови где все модули")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                cog_name = f'cogs.{filename[:-3]}'
                try:
                    await self.load_extension(cog_name)
                    self.logger.info(f"он выжил, {cog_name}")
                    self.loaded_cogs_status[filename[:-3]] = True
                except Exception as e:
                    self.logger.error(f"сдохнул {cog_name}: {e}", exc_info=True)
                    self.loaded_cogs_status[filename[:-3]] = False
        
        self.logger.info('крутой дискорд сихронизирует кмд')
        try:
            synced_commands = await self.tree.sync()
            self.logger.info(f'просихронизировано сколько там({len(synced_commands)}) какихто команд')
        except Exception as e:
            self.logger.error(f"МЫ ВСЕ УМРЕМ: {e}")

bot = CoreBot(command_prefix='!', intents=discord.Intents.all())

# КРУТЫЕ БОТ ИВЕНТС
@bot.event
async def on_ready():
    logger.info(f'ОН ВОШЕЛ В ЧУВААААААААААААК: {bot.user.name} ({bot.user.id})')
    logger.info(f'ВЕРСИЯ ДИСКОРД ПИТОН: {discord.__version__}')
    logger.info('ОН ГОТОВ К РАБОТАЕ ЧТОООО')

# чтото тут должно быть но я забыл

if __name__ == "__main__":
    if TOKEN:
        try:
            # Запуск бота теперь асинхронный из-за setup_hook
            async def main():
                async with bot:
                    await bot.start(TOKEN)
            
            asyncio.run(main())

        except discord.LoginFailure:
            logger.critical("КРИТИЧЕСКАЯ ОШИБКА: НЕВЕРНЫЙ ТОКЕН!", exc_info=True)
        except Exception as e:
            logger.critical(f"КОРАБЛЬ ПОТОНУЛ ПОД ДОБРЫМ МОРЕМ: {e}", exc_info=True)
    else:
        logger.critical("ТОКЕН НЕ НАЙДЕН! ИДИ НАХУЙ!") 