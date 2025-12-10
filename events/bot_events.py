"""События бота"""
import discord
from config.settings import PANEL_CHANNEL_ID
from models.application_button import ApplicationButton
from utils.storage import load_applications
from utils.logger import send_log


def setup_bot_events(bot):
    """Настройка событий бота"""
    
    @bot.event
    async def on_ready():
        """Событие при запуске бота"""
        load_applications()
        print(f'Бот запущен как {bot.user}')
        
        # Синхронизация команд
        try:
            synced = await bot.tree.sync()
            print(f'Синхронизировано {len(synced)} команд')
        except Exception as e:
            print(f'Ошибка синхронизации команд: {e}')
        
        # Автоматическая очистка канала панели и создание новой панели
        for guild in bot.guilds:
            try:
                panel_channel = guild.get_channel(PANEL_CHANNEL_ID)
                if panel_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in panel_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            print(f'Не удалось удалить сообщение: {e}')
                    
                    print(f'Удалено {deleted} сообщений из канала панели')
                    
                    # Создание новой панели заявок
                    embed = discord.Embed(
                        title='🏠 Заявка в семью',
                        description='Нажмите на кнопку ниже, чтобы подать заявку на вступление в семью.\n\n'
                                    '**Требования:**\n'
                                    '• Заполните все поля честно\n'
                                    '• Укажите реальную информацию\n'
                                    '• Дождитесь рассмотрения заявки',
                        color=discord.Color.blue()
                    )
                    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
                    
                    view = ApplicationButton()
                    await panel_channel.send(embed=embed, view=view)
                    print(f'Панель заявок создана в канале {panel_channel.name}')
                    
                    # Лог о создании панели
                    await send_log(
                        guild,
                        f'🔧 **Панель заявок автоматически создана**\nКанал: {panel_channel.mention}\nУдалено старых сообщений: {deleted}',
                        discord.Color.blue()
                    )
            except Exception as e:
                print(f'Ошибка при работе с каналом панели: {e}')
        
        # Логирование запуска
        for guild in bot.guilds:
            await send_log(
                guild,
                f'✅ **Бот запущен**\nБот {bot.user.mention} успешно запущен и готов к работе!',
                discord.Color.green()
            )