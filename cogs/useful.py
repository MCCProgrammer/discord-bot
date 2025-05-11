import discord
from discord.ext import commands
from discord import app_commands

class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Limpa mensagens no canal atual.")
    @app_commands.describe(
        amount="Número de mensagens para limpar (1 a 100). Use 0 para limpar só o comando."
    )
    async def clear(self, interaction: discord.Interaction, amount: int = 0):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("🚫 Você não tem permissão para apagar mensagens.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ Eu não tenho permissão para apagar mensagens.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            limit = 1 if amount <= 0 else min(amount, 100)

            # Função check que garante que todas as mensagens, incluindo as do bot, sejam apagadas
            deleted = await interaction.channel.purge(
                limit=limit,
                check=lambda msg: True  # Inclui todas as mensagens, inclusive as do bot
            )

            await interaction.followup.send(f"✅ {len(deleted)} mensagens foram apagadas.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send("⚠️ Ocorreu um erro ao tentar apagar as mensagens.", ephemeral=True)
            print(f"Erro no comando /clear: {e}")




# Esta função é necessária para que o bot consiga adicionar este cog
async def setup(bot):
    await bot.add_cog(Useful(bot))

