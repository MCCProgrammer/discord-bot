import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bane um membro do servidor.")
    @app_commands.describe(member="Membro a ser banido", reason="Motivo do banimento")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("🚫 Você não tem permissão para banir membros.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message("❌ Eu não tenho permissão para banir membros.", ephemeral=True)
            return

        reason = reason or "Nenhum motivo especificado"

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"✅ {member.mention} foi banido.\n📝 Motivo: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não consegui banir esse membro. Verifique as permissões e hierarquia de cargos.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Ocorreu um erro ao tentar banir o membro: {e}", ephemeral=True)

    @app_commands.command(name="unban", description="Desbane um usuário usando o ID de usuário.")
    @app_commands.describe(user_id="ID do usuário (ex: 123456789012345678)")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        # Verificando permissões do usuário
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("🚫 Você não tem permissão para desbanir membros.", ephemeral=True)
            return

        # Verificando permissões do bot
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message("❌ Eu não tenho permissão para desbanir membros.", ephemeral=True)
            return

        # Verificando se o ID é válido
        try:
            user_id = int(user_id)  # Converte o ID para inteiro
        except ValueError:
            await interaction.response.send_message("⚠️ ID inválido. Certifique-se de usar um ID numérico.", ephemeral=True)
            return

        try:
            # Iterando sobre o gerador assíncrono usando async for
            async for ban_entry in interaction.guild.bans():
                if ban_entry.user.id == user_id:
                    await interaction.guild.unban(ban_entry.user)
                    await interaction.response.send_message(f"✅ O usuário {ban_entry.user.mention} foi desbanido com sucesso.")
                    return

            # Caso o usuário não seja encontrado na lista de banidos
            await interaction.response.send_message("🔍 Usuário não encontrado na lista de banidos.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não tenho permissões para realizar essa ação.", ephemeral=True)
        except Exception as e:
            # Em caso de outro erro
            await interaction.response.send_message(f"⚠️ Ocorreu um erro inesperado: {e}", ephemeral=True)

    @app_commands.command(name="kick", description="Expulsa um membro do servidor.")
    @app_commands.describe(member="Membro a ser expulso", reason="Motivo da expulsão")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("🚫 Você não tem permissão para expulsar membros.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message("❌ Eu não tenho permissão para expulsar membros.", ephemeral=True)
            return

        reason = reason or "Nenhum motivo especificado."

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"✅ {member.mention} foi expulso.\n📝 Motivo: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não consegui expulsar esse membro. Verifique a hierarquia de cargos.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Ocorreu um erro ao tentar expulsar o membro: {e}", ephemeral=True)


    @app_commands.command(name="mute", description="Silencia um membro (cria cargo se necessário).")
    @app_commands.describe(member="Membro a ser silenciado", reason="Motivo do mute")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        guild = interaction.guild

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("🚫 Você não tem permissão para silenciar membros.", ephemeral=True)
            return

        if not guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("❌ Eu não tenho permissão para gerenciar cargos.", ephemeral=True)
            return

        reason = reason or "Nenhum motivo especificado."

        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            try:
                muted_role = await guild.create_role(name="Muted", reason="Criado para silenciar membros.")
                for channel in guild.channels:
                    try:
                        await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
                    except Exception as e:
                        print(f"Erro ao definir permissões no canal {channel.name}: {e}")
            except Exception as e:
                await interaction.response.send_message(f"⚠️ Não consegui criar o cargo Muted: {e}", ephemeral=True)
                return

        if muted_role in member.roles:
            await interaction.response.send_message("🔇 Esse membro já está silenciado.", ephemeral=True)
            return

        try:
            await member.add_roles(muted_role, reason=reason)
            await interaction.response.send_message(f"✅ {member.mention} foi silenciado.\n📝 Motivo: {reason}")

            try:
                await member.send(f"Você foi silenciado no servidor **{guild.name}**.\nMotivo: {reason}")
            except:
                pass  # Usuário com DMs fechadas
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não consegui silenciar esse membro. Verifique a hierarquia de cargos.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Ocorreu um erro ao aplicar o mute: {e}", ephemeral=True)


    @app_commands.command(name="unmute", description="Remove o silêncio de um membro.")
    @app_commands.describe(member="Membro a ser desmutado")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("🚫 Você não tem permissão para desmutar membros.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("❌ Eu não tenho permissão para gerenciar cargos.", ephemeral=True)
            return

        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")

        if not muted_role:
            await interaction.response.send_message("⚠️ Cargo 'Muted' não encontrado. Não é possível desmutar membros.", ephemeral=True)
            return

        if muted_role not in member.roles:
            await interaction.response.send_message("🔊 Esse membro não está silenciado.", ephemeral=True)
            return

        try:
            await member.remove_roles(muted_role)
            await interaction.response.send_message(f"✅ {member.mention} não está mais silenciado.")

            try:
                await member.send(f"Você foi desmutado no servidor **{interaction.guild.name}**.")
            except:
                pass  # Caso o usuário tenha DMs fechadas
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não consegui desmutar esse membro. Verifique a hierarquia de cargos.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Ocorreu um erro ao remover o silêncio: {e}", ephemeral=True)


# Esta função é necessária para que o bot consiga adicionar este cog
async def setup(bot):
    await bot.add_cog(Moderation(bot))

    # Comandos de banwords podem ser implementados assim:
    # @app_commands.command(name="addbanword", description="Adiciona uma palavra à lista de banidas.")
    # async def addbanword(self, interaction: discord.Interaction, word: str):
    #     ...

    # @app_commands.command(name="removebanword", description="Remove uma palavra da lista de banidas.")
    # async def removebanword(self, interaction: discord.Interaction, word: str):
    #     ...
