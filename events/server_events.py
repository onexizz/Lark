"""События сервера для логирования"""
import discord
from utils.logger import send_log


def setup_server_events(bot):
    """Настройка событий для логирования"""
    
    @bot.event
    async def on_member_join(member):
        """Лог входа участника"""
        await send_log(
            member.guild,
            f'➕ **Участник присоединился**\n{member.mention} ({member.name}#{member.discriminator})\nID: {member.id}\nАккаунт создан: <t:{int(member.created_at.timestamp())}:R>',
            discord.Color.green()
        )
    
    @bot.event
    async def on_member_remove(member):
        """Лог выхода участника"""
        await send_log(
            member.guild,
            f'➖ **Участник покинул сервер**\n{member.mention} ({member.name}#{member.discriminator})\nID: {member.id}',
            discord.Color.orange()
        )
    
    @bot.event
    async def on_message_delete(message):
        """Лог удаления сообщения"""
        if message.author.bot:
            return
        
        content = message.content[:1000] if message.content else '*[Нет текста]*'
        await send_log(
            message.guild,
            f'🗑️ **Сообщение удалено**\nАвтор: {message.author.mention}\nКанал: {message.channel.mention}\nСодержание: {content}',
            discord.Color.dark_gray()
        )
    
    @bot.event
    async def on_message_edit(before, after):
        """Лог редактирования сообщения"""
        if before.author.bot or before.content == after.content:
            return
        
        before_content = before.content[:500] if before.content else '*[Нет текста]*'
        after_content = after.content[:500] if after.content else '*[Нет текста]*'
        
        await send_log(
            before.guild,
            f'✏️ **Сообщение изменено**\nАвтор: {before.author.mention}\nКанал: {before.channel.mention}\n**До:** {before_content}\n**После:** {after_content}',
            discord.Color.blue()
        )
    
    @bot.event
    async def on_member_ban(guild, user):
        """Лог бана участника"""
        await send_log(
            guild,
            f'🔨 **Участник забанен**\n{user.mention} ({user.name}#{user.discriminator})\nID: {user.id}',
            discord.Color.dark_red()
        )
    
    @bot.event
    async def on_member_unban(guild, user):
        """Лог разбана участника"""
        await send_log(
            guild,
            f'🔓 **Участник разбанен**\n{user.mention} ({user.name}#{user.discriminator})\nID: {user.id}',
            discord.Color.green()
        )
    
    @bot.event
    async def on_guild_role_create(role):
        """Лог создания роли"""
        await send_log(
            role.guild,
            f'🎭 **Роль создана**\nНазвание: {role.mention}\nID: {role.id}\nЦвет: {role.color}',
            discord.Color.green()
        )
    
    @bot.event
    async def on_guild_role_delete(role):
        """Лог удаления роли"""
        await send_log(
            role.guild,
            f'🎭 **Роль удалена**\nНазвание: {role.name}\nID: {role.id}',
            discord.Color.red()
        )
    
    @bot.event
    async def on_guild_channel_create(channel):
        """Лог создания канала"""
        await send_log(
            channel.guild,
            f'📁 **Канал создан**\nНазвание: {channel.mention}\nТип: {channel.type}\nID: {channel.id}',
            discord.Color.green()
        )
    
    @bot.event
    async def on_guild_channel_delete(channel):
        """Лог удаления канала"""
        await send_log(
            channel.guild,
            f'📁 **Канал удален**\nНазвание: {channel.name}\nТип: {channel.type}\nID: {channel.id}',
            discord.Color.red()
        )
    
    @bot.event
    async def on_member_update(before, after):
        """Лог изменения участника (роли, никнейм)"""
        if before.roles != after.roles:
            added_roles = [role.mention for role in after.roles if role not in before.roles]
            removed_roles = [role.mention for role in before.roles if role not in after.roles]
            
            if added_roles:
                await send_log(
                    after.guild,
                    f'➕ **Роли добавлены**\nУчастник: {after.mention}\nРоли: {", ".join(added_roles)}',
                    discord.Color.green()
                )
            
            if removed_roles:
                await send_log(
                    after.guild,
                    f'➖ **Роли удалены**\nУчастник: {after.mention}\nРоли: {", ".join(removed_roles)}',
                    discord.Color.orange()
                )
        
        if before.nick != after.nick:
            await send_log(
                after.guild,
                f'✏️ **Никнейм изменен**\nУчастник: {after.mention}\nБыло: {before.nick or "Нет"}\nСтало: {after.nick or "Нет"}',
                discord.Color.blue()
            )
    
    @bot.event
    async def on_voice_state_update(member, before, after):
        """Лог изменения голосового статуса"""
        if before.channel != after.channel:
            if before.channel is None:
                await send_log(
                    member.guild,
                    f'🔊 **Участник присоединился к голосовому каналу**\n{member.mention} → {after.channel.mention}',
                    discord.Color.green()
                )
            elif after.channel is None:
                await send_log(
                    member.guild,
                    f'🔇 **Участник покинул голосовой канал**\n{member.mention} ← {before.channel.mention}',
                    discord.Color.orange()
                )
            else:
                await send_log(
                    member.guild,
                    f'🔄 **Участник переместился**\n{member.mention}\n{before.channel.mention} → {after.channel.mention}',
                    discord.Color.blue()
                )