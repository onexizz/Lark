"""Кнопки для правил сервера"""
import discord

class RulesButton(discord.ui.View):
    """Кнопка для показа ссылки на правила"""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label='Узнать правила',
            style=discord.ButtonStyle.link,
            url='https://docs.google.com/document/d/1eZWV6J8NwFgPeK_vhD6woovznuvxj10Gwcv6-QmnNow/'
        ))