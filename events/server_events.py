"""События сервера для логирования"""
import discord
from utils.logger import send_log
from utils.role_manager import setup_new_member


async def get_audit_info(guild, action_type, target_id=None, limit=5):
    """Получение информации из аудит логов"""
    try:
        async for entry in guild.audit_logs(limit=limit, action=action_type):
            if target_id and hasattr(entry.target, 'id') and entry.target.id != target_id:
                continue
            if entry.created_at.timestamp() > (discord.utils.utcnow().timestamp() - 300):  # Последние 5 минут
                return entry.user, entry.reason or 'Причина не указана'
    except Exception as e:
        print(f"Ошибка при получении аудит логов: {e}")
    return None, None


def setup_server_events(bot):
    """Настройка событий для логирования"""
    
    @bot.event
    async def on_member_join(member):
        """Лог входа участника"""
        # Выдача роли заявителя новому участнику
        await setup_new_member(member)
        
        await send_log(
            member.guild,
            f'➕ **Участник присоединился**\n{member.mention} ({member.name}#{member.discriminator})\nID: {member.id}\nАккаунт создан: <t:{int(member.created_at.timestamp())}:R>\nВыдана роль заявителя',
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
        
        # Получение информации из аудит логов
        moderator, reason = await get_audit_info(
            message.guild, 
            discord.AuditLogAction.message_delete,
            message.id
        )
        
        content = message.content[:1000] if message.content else '*[Нет текста]*'
        
        if moderator:
            await send_log(
                message.guild,
                f'🗑️ **Сообщение удалено**\nАвтор: {message.author.mention}\nКанал: {message.channel.mention}\nУдалил: {moderator.mention}\nПричина: {reason}\nСодержание: {content}',
                discord.Color.dark_gray()
            )
        else:
            await send_log(
                message.guild,
                f'🗑️ **Сообщение удалено**\nАвтор: {message.author.mention}\nКанал: {message.channel.mention}\nСодержание: {content}\n*Информация об удалившем недоступна*',
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
        moderator, reason = await get_audit_info(guild, discord.AuditLogAction.ban, user.id)
        
        if moderator:
            await send_log(
                guild,
                f'🔨 **Участник забанен**\nЗабанен: {user.mention} ({user.name}#{user.discriminator})\nID: {user.id}\nМодератор: {moderator.mention}\nПричина: {reason}',
                discord.Color.dark_red()
            )
        else:
            await send_log(
                guild,
                f'🔨 **Участник забанен**\nЗабанен: {user.mention} ({user.name}#{user.discriminator})\nID: {user.id}\n*Информация о модераторе недоступна*',
                discord.Color.dark_red()
            )
    
    @bot.event
    async def on_member_unban(guild, user):
        """Лог разбана участника"""
        moderator, reason = await get_audit_info(guild, discord.AuditLogAction.unban, user.id)
        
        if moderator:
            await send_log(
                guild,
                f'🔓 **Участник разбанен**\nРазбанен: {user.mention} ({user.name}#{user.discriminator})\nID: {user.id}\nМодератор: {moderator.mention}\nПричина: {reason}',
                discord.Color.green()
            )
        else:
            await send_log(
                guild,
                f'🔓 **Участник разбанен**\nРазбанен: {user.mention} ({user.name}#{user.discriminator})\nID: {user.id}\n*Информация о модераторе недоступна*',
                discord.Color.green()
            )
    
    @bot.event
    async def on_guild_role_create(role):
        """Лог создания роли"""
        moderator, reason = await get_audit_info(role.guild, discord.AuditLogAction.role_create, role.id)
        
        if moderator:
            await send_log(
                role.guild,
                f'🎭 **Роль создана**\nНазвание: {role.mention}\nID: {role.id}\nЦвет: {role.color}\nСоздал: {moderator.mention}\nПричина: {reason}',
                discord.Color.green()
            )
        else:
            await send_log(
                role.guild,
                f'🎭 **Роль создана**\nНазвание: {role.mention}\nID: {role.id}\nЦвет: {role.color}\n*Информация о создателе недоступна*',
                discord.Color.green()
            )
    
    @bot.event
    async def on_guild_role_delete(role):
        """Лог удаления роли"""
        moderator, reason = await get_audit_info(role.guild, discord.AuditLogAction.role_delete, role.id)
        
        if moderator:
            await send_log(
                role.guild,
                f'🎭 **Роль удалена**\nНазвание: {role.name}\nID: {role.id}\nУдалил: {moderator.mention}\nПричина: {reason}',
                discord.Color.red()
            )
        else:
            await send_log(
                role.guild,
                f'🎭 **Роль удалена**\nНазвание: {role.name}\nID: {role.id}\n*Информация об удалившем недоступна*',
                discord.Color.red()
            )
    
    @bot.event
    async def on_guild_channel_create(channel):
        """Лог создания канала"""
        moderator, reason = await get_audit_info(channel.guild, discord.AuditLogAction.channel_create, channel.id)
        
        if moderator:
            await send_log(
                channel.guild,
                f'📁 **Канал создан**\nНазвание: {channel.mention}\nТип: {channel.type}\nID: {channel.id}\nСоздал: {moderator.mention}\nПричина: {reason}',
                discord.Color.green()
            )
        else:
            await send_log(
                channel.guild,
                f'📁 **Канал создан**\nНазвание: {channel.mention}\nТип: {channel.type}\nID: {channel.id}\n*Информация о создателе недоступна*',
                discord.Color.green()
            )
    
    @bot.event
    async def on_guild_channel_delete(channel):
        """Лог удаления канала"""
        moderator, reason = await get_audit_info(channel.guild, discord.AuditLogAction.channel_delete, channel.id)
        
        if moderator:
            await send_log(
                channel.guild,
                f'📁 **Канал удален**\nНазвание: {channel.name}\nТип: {channel.type}\nID: {channel.id}\nУдалил: {moderator.mention}\nПричина: {reason}',
                discord.Color.red()
            )
        else:
            await send_log(
                channel.guild,
                f'📁 **Канал удален**\nНазвание: {channel.name}\nТип: {channel.type}\nID: {channel.id}\n*Информация об удалившем недоступна*',
                discord.Color.red()
            )
    
    @bot.event
    async def on_member_update(before, after):
        """Лог изменения участника (роли, никнейм)"""
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            
            if added_roles:
                # Получение информации о том, кто добавил роли
                moderator, reason = await get_audit_info(after.guild, discord.AuditLogAction.member_role_update, after.id)
                
                if moderator:
                    await send_log(
                        after.guild,
                        f'➕ **Роли добавлены**\nУчастник: {after.mention}\nРоли: {", ".join([r.mention for r in added_roles])}\nМодератор: {moderator.mention}\nПричина: {reason}',
                        discord.Color.green()
                    )
                else:
                    await send_log(
                        after.guild,
                        f'➕ **Роли добавлены**\nУчастник: {after.mention}\nРоли: {", ".join([r.mention for r in added_roles])}\n*Информация о модераторе недоступна*',
                        discord.Color.green()
                    )
            
            if removed_roles:
                # Получение информации о том, кто убрал роли
                moderator, reason = await get_audit_info(after.guild, discord.AuditLogAction.member_role_update, after.id)
                
                if moderator:
                    await send_log(
                        after.guild,
                        f'➖ **Роли удалены**\nУчастник: {after.mention}\nРоли: {", ".join([r.mention for r in removed_roles])}\nМодератор: {moderator.mention}\nПричина: {reason}',
                        discord.Color.orange()
                    )
                else:
                    await send_log(
                        after.guild,
                        f'➖ **Роли удалены**\nУчастник: {after.mention}\nРоли: {", ".join([r.mention for r in removed_roles])}\n*Информация о модераторе недоступна*',
                        discord.Color.orange()
                    )
        
        if before.nick != after.nick:
            # Получение информации о том, кто изменил никнейм
            moderator, reason = await get_audit_info(after.guild, discord.AuditLogAction.member_update, after.id)
            
            if moderator:
                await send_log(
                    after.guild,
                    f'✏️ **Никнейм изменен**\nУчастник: {after.mention}\nМодератор: {moderator.mention}\nБыло: {before.nick or "Нет"}\nСтало: {after.nick or "Нет"}\nПричина: {reason}',
                    discord.Color.blue()
                )
            else:
                await send_log(
                    after.guild,
                    f'✏️ **Никнейм изменен**\nУчастник: {after.mention}\nБыло: {before.nick or "Нет"}\nСтало: {after.nick or "Нет"}\n*Информация о модераторе недоступна*',
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
