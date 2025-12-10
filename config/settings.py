"""Настройки бота"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
TOKEN = os.getenv('DISCORD_TOKEN')

# ID каналов
APPLICATION_CHANNEL_ID = 1448168154235666502  # Канал для заявок
LOG_CHANNEL_ID = 1448195966573346827          # Канал для логов
PANEL_CHANNEL_ID = 1448019782614909090        # Канал для панели заявок

# Файл хранения заявок
APPLICATIONS_FILE = 'data/applications.json'