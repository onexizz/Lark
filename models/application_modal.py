"""Модальное окно для заявки в семью"""
import discord
from datetime import datetime
from config.settings import APPLICATION_CHANNEL_ID, STATIC_CHANNEL_ID
from utils.storage import get_next_app_id, add_application
from utils.logger import send_log
from utils.role_manager import set_applicant_nickname, give_applicant_role


class FamilyApplicationModal(discord.ui.Modal, title='Заявка в семью'):
    """Модальное окно для заявки в семью"""
    
    full_name = discord.ui.TextInput(
        label='Имя и Фамилия',
        placeholder='Введите ваше имя и фамилию...',
        required=True,
        max_length=100
    )
    
    passport = discord.ui.TextInput(
        label='Номер паспорта(Static)',
        placeholder='Введите номер паспорта...',
        required=True,
        max_length=50
    )
    
    usefulness = discord.ui.TextInput(
        label='Чем будете полезны в семье?',
        style=discord.TextStyle.paragraph,
        placeholder='Расскажите, чем вы можете помочь семье...',
        required=True,
        max_length=1000,
        min_length=10
    )
    
    ooc_name = discord.ui.TextInput(
        label='OOC Имя',
        placeholder='Введите ваше OOC имя...',
        required=True,
        max_length=100
    )


    async def on_submit(self, interaction: discord.Interaction):
        app_id = get_next_app_id()
        
        # Сохранение заявки
        app_data = {
            'id': app_id,
            'user_id': interaction.user.id,
            'full_name': self.full_name.value,
            'passport': self.passport.value,
            'usefulness': self.usefulness.value,
            'ooc_name': self.ooc_name.value,
            'status': 'pending',
            'timestamp': datetime.utcnow().isoformat()
        }
        add_application(app_data)
        
        # Создание embed для заявки
        embed = discord.Embed(
            title=f'📋 Новая заявка в семью #{app_id}',
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name='👤 Имя и Фамилия', value=self.full_name.value, inline=False)
        embed.add_field(name='🆔 Номер паспорта', value=self.passport.value, inline=False)
        embed.add_field(name='💼 Чем будет полезен', value=self.usefulness.value, inline=False)
        embed.add_field(name='🎮 OOC Имя', value=self.ooc_name.value, inline=False)
        embed.set_footer(text=f'Заявка от {interaction.user.name}', icon_url=interaction.user.display_avatar.url)
        
        static_id = interaction.guild.get_channel(STATIC_CHANNEL_ID)
        if static_id:
            await static_id.send(
                content=f'Статический ID пользователя {interaction.user.mention} - {self.passport.value}'
            )

        # Отправка в канал заявок
        app_channel = interaction.guild.get_channel(APPLICATION_CHANNEL_ID)
        if app_channel:
            await app_channel.send(
                content=f'{interaction.user.mention} подал заявку в семью!',
                embed=embed
            )
        
        # Ответ пользователю
        await interaction.response.send_message(
            f'✅ Ваша заявка #{app_id} успешно отправлена! Ожидайте рассмотрения.',
            ephemeral=True
        )

        # Выдача роли заявителя
        await give_applicant_role(interaction.user)
        
        # Лог
        await send_log(
            interaction.guild,
            f'📋 **Новая заявка #{app_id}**\nПользователь: {interaction.user.mention} ({interaction.user.id})\nИмя: {self.full_name.value}\nOOC: {self.ooc_name.value}\nНикнейм изменен на: {self.full_name.value} | {self.ooc_name.value}',
            discord.Color.gold()
        )