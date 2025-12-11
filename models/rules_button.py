"""Кнопки для правил сервера с изображением"""
import discord

class RulesButton(discord.ui.View):
    """Кнопка для показа ссылки на правила с изображением"""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label='Узнать правила',
            style=discord.ButtonStyle.link,
            url='https://docs.google.com/document/d/1eZWV6J8NwFgPeK_vhD6woovznuvxj10Gwcv6-QmnNow/'
        ))

    @staticmethod
    def create_rules_embed():
        """Создать embed с изображением для правил"""
        embed = discord.Embed(
            title="📜 Правила сервера",
            description="Нажмите на кнопку ниже, чтобы ознакомиться с полными правилами нашего сервера.",
            color=discord.Color.blue()
        )
        
        # Добавьте URL изображения здесь
        embed.set_thumbnail(url="http://talori.pis-pis.ru/img/yznat.png")  # Замените на ваш URL
        embed.set_footer(text="Не знание правил не освобождает вас от ответственности.")
        
        return embed