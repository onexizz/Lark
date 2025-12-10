"""Модуль логирования событий"""
import discord
from datetime import datetime
from config.settings import LOG_CHANNEL_ID


async def send_log(guild, message, color=discord.Color.blue()):
    """Отправка логов в канал логов"""
    try:
        log_channel = guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                description=message,
                color=color,
                timestamp=datetime.utcnow()
            )
            await log_channel.send(embed=embed)
    except Exception as e:
        print(f"Ошибка при отправке лога: {e}")