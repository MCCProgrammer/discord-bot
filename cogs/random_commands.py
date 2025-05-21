from discord.ext import commands
from discord import app_commands
import discord

def admin_check(interaction: discord.Interaction):
    return interaction.user.guild_permissions.administrator

class Random_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #----------------------------- /rep ----------------------------------------------------
    @app_commands.command(name="rep", description="Repete a mensagem fornecida.")
    async def rep(self, interaction: discord.Interaction, mensagem: str):
        await interaction.response.send_message(mensagem)


    #----------------------------- /botping ----------------------------------------------------
    @app_commands.command(name="botping", description="Mostra o ping do bot.")
    async def botping(self, interaction: discord.Interaction):
        ping = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"My Ping: {ping}ms\nIf it's high, please subscribe to the premium version or donate! Thanks :)")

    
    # ----------------------------- /activity -----------------------------------------------
    @app_commands.command(name="activity", description="Muda o status do bot (admin only).")
    @app_commands.check(admin_check)
    async def activity(self, interaction: discord.Interaction, atividade: str):
        await self.bot.change_presence(activity=discord.Game(name=atividade))
        await interaction.response.send_message(f"Bot's activity changed to: {atividade}")


    # ----------------------------- /userinfo -----------------------------------------------
    @app_commands.command(name="userinfo", description="Mostra informações sobre ti.")
    async def userinfo(self, interaction: discord.Interaction):
        user = interaction.user
        embed = discord.Embed(
            title="USER INFO",
            description=f"Here is the info we retrieved about {user}",
            colour = user.colour if hasattr(user, "colour") else discord.Colour.default())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="NAME", value=user.name, inline=True)
        embed.add_field(name="NICKNAME", value=user.nick or "None", inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="STATUS", value=str(user.status), inline=True)
        await interaction.response.send_message(embed=embed)

# Esta função é necessária para que o bot consiga adicionar este cog
async def setup(bot):
    await bot.add_cog(Random_commands(bot))

