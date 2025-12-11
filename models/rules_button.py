"""Кнопки для правил сервера с большим изображением"""
import discord

class RulesButton(discord.ui.View):
    """Кнопка для показа ссылки на правила с большим изображением"""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label='Узнать правила 📜',
            style=discord.ButtonStyle.link,
            url='https://docs.google.com/document/d/1eZWV6J8NwFgPeK_vhD6woovznuvxj10Gwcv6-QmnNow/'
        ))
    
    
    @staticmethod
    def create_simple_rules_embed():
        """Упрощенный embed с изображением (без дополнительных полей)"""
        embed = discord.Embed(
            title="📜 Правила сервера",
            description="Нажмите на кнопку ниже, чтобы ознакомиться с полными правилами",
            color=discord.Color.blurple()
        )
        
        # Просто большое изображение без лишних деталей
        embed.set_image(url="https://your-image-url-here.com/rules-image.png")
        
        return embed