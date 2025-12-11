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
STATIC_CHANNEL_ID = 1448565203875926128
RULES_CHANNEL_ID = 1448166747189280769        # Канал для правил

# ID ролей
APPLICANT_ROLE_ID = 1448026283060760686       # Роль для подающих заявки
ACCEPTED_ROLE_1_ID = 1448026775899865240      # Первая роль принятых
ACCEPTED_ROLE_2_ID = 1448026398403985408      # Вторая роль принятых

# Файл хранения заявок
APPLICATIONS_FILE = 'data/applications.json'