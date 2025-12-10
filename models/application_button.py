"""Кнопка для открытия модального окна заявки"""
import discord
from models.application_modal import FamilyApplicationModal


class ApplicationButton(discord.ui.View):
    """Кнопка для открытия модального окна заявки"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label='📝 Подать заявку в семью',
        style=discord.ButtonStyle.primary,
        custom_id='family_application_button'
    )
    async def application_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FamilyApplicationModal())