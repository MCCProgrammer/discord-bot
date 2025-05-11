from discord import app_commands, Interaction, Embed
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree  # Facilita o acesso aos slash commands registrados

    @app_commands.command(name="help", description="Mostra ajuda para comandos ou um comando específico.")
    async def help(self, interaction: Interaction, command: str = None):
        if command:
            # Procurar por comandos de barra com esse nome
            for cmd in self.tree.get_commands():
                if command.lower() == cmd.name.lower():
                    paramString = ", ".join([param.name for param in cmd.parameters])
                    if not paramString:
                        paramString = "Nenhum"
                    embed = Embed(title=f"Ajuda - /{cmd.name}", description=cmd.description or "Sem descrição")
                    embed.add_field(name="Parâmetros", value=paramString)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            await interaction.response.send_message(f"Comando `{command}` não encontrado.", ephemeral=True)

        else:
            embed = Embed(title="Ajuda", description="Lista de comandos disponíveis:")
            for cmd in self.tree.get_commands():
                embed.add_field(name=f"/{cmd.name}", value=cmd.description or "Sem descrição", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

# Função para carregar o cog
async def setup(bot):
    await bot.add_cog(Help(bot))
