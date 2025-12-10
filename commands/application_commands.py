"""Команды для работы с заявками"""
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from utils.storage import get_application, update_application
from utils.logger import send_log
from models.application_button import ApplicationButton


def setup_application_commands(bot):
    """Настройка команд для работы с заявками"""
    
    @bot.tree.command(name='application_panel', description='Создать панель для подачи заявок')
    @app_commands.default_permissions(administrator=True)
    async def application_panel(interaction: discord.Interaction):
        """Команда для создания панели заявок"""
        embed = discord.Embed(
            title='🏠 Заявка в семью',
            description='Нажмите на кнопку ниже, чтобы подать заявку на вступление в семью.\n\n'
                        '**Требования:**\n'
                        '• Заполните все поля честно\n'
                        '• Укажите реальную информацию\n'
                        '• Дождитесь рассмотрения заявки',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        
        view = ApplicationButton()
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message('✅ Панель заявок создана!', ephemeral=True)
        
        await send_log(
            interaction.guild,
            f'🔧 **Панель заявок создана**\nМодератор: {interaction.user.mention}\nКанал: {interaction.channel.mention}',
            discord.Color.blue()
        )
    
    @bot.command(name='accept')
    @commands.has_permissions(manage_guild=True)
    async def accept_application(ctx, app_id: int):
        """Принять заявку"""
        app = get_application(app_id)
        
        if not app:
            await ctx.send(f'❌ Заявка #{app_id} не найдена!')
            return
        
        if app['status'] != 'pending':
            await ctx.send(f'❌ Заявка #{app_id} уже обработана (статус: {app["status"]})!')
            return
        
        # Обновление статуса
        update_application(app_id, {
            'status': 'accepted',
            'processed_by': ctx.author.id,
            'processed_at': datetime.utcnow().isoformat()
        })
        
        # Отправка уведомления пользователю
        try:
            user = await bot.fetch_user(app['user_id'])
            embed = discord.Embed(
                title='✅ Заявка принята!',
                description=f'Ваша заявка #{app_id} в семью была принята!',
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Принял', value=f'{ctx.author.mention} ({ctx.author.name})', inline=False)
            embed.add_field(name='Имя и Фамилия', value=app['full_name'], inline=False)
            
            await user.send(embed=embed)
        except Exception as e:
            await ctx.send(f'⚠️ Не удалось отправить уведомление пользователю: {e}')
        
        # Ответ в канал
        await ctx.send(f'✅ Заявка #{app_id} от пользователя <@{app["user_id"]}> принята!')
        
        # Лог
        await send_log(
            ctx.guild,
            f'✅ **Заявка принята #{app_id}**\nПринял: {ctx.author.mention}\nПодавал: <@{app["user_id"]}>\nИмя: {app["full_name"]}',
            discord.Color.green()
        )
    
    @bot.command(name='decline')
    @commands.has_permissions(manage_guild=True)
    async def decline_application(ctx, app_id: int, *, reason: str):
        """Отклонить заявку"""
        app = get_application(app_id)
        
        if not app:
            await ctx.send(f'❌ Заявка #{app_id} не найдена!')
            return
        
        if app['status'] != 'pending':
            await ctx.send(f'❌ Заявка #{app_id} уже обработана (статус: {app["status"]})!')
            return
        
        # Обновление статуса
        update_application(app_id, {
            'status': 'declined',
            'processed_by': ctx.author.id,
            'decline_reason': reason,
            'processed_at': datetime.utcnow().isoformat()
        })
        
        # Отправка уведомления пользователю
        try:
            user = await bot.fetch_user(app['user_id'])
            embed = discord.Embed(
                title='❌ Заявка отклонена',
                description=f'Ваша заявка #{app_id} в семью была отклонена.',
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Отклонил', value=f'{ctx.author.mention} ({ctx.author.name})', inline=False)
            embed.add_field(name='Причина', value=reason, inline=False)
            embed.add_field(name='Имя и Фамилия', value=app['full_name'], inline=False)
            
            await user.send(embed=embed)
        except Exception as e:
            await ctx.send(f'⚠️ Не удалось отправить уведомление пользователю: {e}')
        
        # Ответ в канал
        await ctx.send(f'❌ Заявка #{app_id} от пользователя <@{app["user_id"]}> отклонена.\nПричина: {reason}')
        
        # Лог
        await send_log(
            ctx.guild,
            f'❌ **Заявка отклонена #{app_id}**\nОтклонил: {ctx.author.mention}\nПодавал: <@{app["user_id"]}>\nИмя: {app["full_name"]}\nПричина: {reason}',
            discord.Color.red()
        )
    
    # Обработка ошибок команд
    @accept_application.error
    async def accept_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ У вас нет прав для выполнения этой команды!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❌ Использование: `l.accept <номер заявки>`')
        else:
            await ctx.send(f'❌ Произошла ошибка: {error}')
    
    @decline_application.error
    async def decline_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ У вас нет прав для выполнения этой команды!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❌ Использование: `l.decline <номер заявки> <причина>`')
        else:
            await ctx.send(f'❌ Произошла ошибка: {error}')