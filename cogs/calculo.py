from discord.ext import commands
from discord import app_commands
import math
import discord

# implementa os commandos !calc


class Calculo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------- /calc -----------------------------
    @app_commands.command(name="calc", description="Realiza cálculos matemáticos.")
    async def calc(self, interaction: discord.Interaction, arg1: str = None, arg2: str = None, arg3: str = None):
        # Se os 3 argumentos forem fornecidos (operador e 2 números)
        if arg1 and arg2 and arg3:
            if arg1 in switcher2Args and isnumber(arg2) and isnumber(arg3):
                result, text = switcher2Args[arg1](float(arg2), float(arg3))
                embed = discord.Embed(title=str(result), description=text, color=0x00ff00)
                embed.set_footer(text="I did the calculations in my head ;)")  # Personalize como quiser
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('Argumentos inválidos ou operador inválido. Para mais informações digite /help ou /help calc.')

        # Se apenas 2 argumentos forem fornecidos (operador e 1 número)
        elif arg1 and arg2 and not arg3:
            if arg1 in switcher1Arg and isnumber(arg2):
                result, text = switcher1Arg[arg1](float(arg2))
                embed = discord.Embed(title=str(result), description=text, color=0x00ff00)
                embed.set_footer(text="I did the calculations in my head ;)")  # Personalize como quiser
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('Argumentos inválidos ou operador inválido. Para mais informações digite /help ou /help calc.')
        else:
            await interaction.response.send_message('Uso incorreto do comando. Para mais informações digite /help ou /help calc.')


async def setup(bot):
    await bot.add_cog(Calculo(bot))
#----------------------------- Funcões auxiliares ao comando calc ----------------------------------------------------


def isnumber(arg1):
    try:
        arg = float(arg1)
        return arg
    except ValueError:
        return None

def add(arg1,arg2):
    res = arg1+arg2
    return res, str(arg1)+" + "+str(arg2)+ " = "+ str(res) 

def sub(arg1,arg2):
    res = arg1-arg2
    return res, str(arg1)+" - "+str(arg2)+ " = "+ str(res)

def div(arg1,arg2):
    if arg2 == 0:
        return None,"Não é possivel dividir por 0"
    else:
        res = arg1/arg2
        return res, str(arg1)+" / "+str(arg2)+ " = "+ str(res)

def mult(arg1,arg2):
    res = arg1*arg2
    return res, str(arg1)+" * "+str(arg2)+ " = "+ str(res)

def potencia(arg1,arg2):
    res = math.pow(arg1,arg2)
    return res, str(arg1)+" ^ "+str(arg2)+ " = "+ str(res)

def raiz(arg1,arg2):
    if arg1 == 0:
        return "Não é possivel ter raiz de indice 0"
    else:
        res = math.pow(arg2,1/arg1)
        return res, "Raiz de "+str(arg2)+" de indice "+str(arg1)+ " = "+ str(res)

def permutations(arg1,arg2):
    n=arg1
    p=arg2
    for rep in range(1, n):
        result = rep * result
    if result == 0:
        result = 1

    numerador = result
    nat_p = n - p

    resultado4 = nat_p
    for rep in range(1, nat_p):
        resultado4 = rep * resultado4

    if resultado4 == 0:
        resultado4 = 1

    denominador = resultado4
    resultado = numerador / denominador

    return resultado, "Permutações de "+ str(n)+ " elementos "+ str(p)+ " a "+str(p)+ " = "+ str(resultado)

def combination(arg1,arg2):
    n = arg1
    p = arg2

    result = n
    for rep in range(1, n):
        result = rep * result

    if result == 0:
        result = 1

    numerador = result
    nat_p = n - p

    resultado4 = nat_p
    for rep in range(1, nat_p):
        resultado4 = rep * resultado4

    if resultado4 == 0:
        resultado4 = 1

    resu = p
    for repi in range(1, p):
        resu = repi * resu

    if resu == 0:
        resu = 1

    res = numerador/(resu * resultado4)
    return res, "Combinações de "+ str(n)+ " elementos "+ str(p)+ " a "+ str(p)+ " = "+ str(res)  

def fatorial(arg):
    res = math.factorial(arg)
    return res, str(arg)+ "! = " + str(res)

def ln(arg):
    res = math.log(arg)
    return res,"ln "+str(arg)+ " = "+str(res)


def log(arg):
    res = math.log10(arg)
    return res,"log10 "+str(arg)+ " = "+str(res)

def sin(arg):
    res = math.sin(arg)
    return res,"sin "+str(arg)+ " = "+str(res)

def cos(arg):
    res = math.cos(arg)
    return res,"cos"+str(arg)+ " = "+str(res)

def tan(arg):
    res = math.tan(arg)
    return res,"tan "+str(arg)+ " = "+str(res)

def exp(arg):
    res = math.exp(arg)
    return res,"e ^ "+str(arg)+ " = "+str(res)


switcher2Args = {
    "+" : add,
    "-" : sub,
    "/" : div,
    "*" : mult,
    "^" : potencia,
    "r" : raiz,
    "P" : permutations,
    "C" : combination
}
switcher1Arg = {
    "!": fatorial,
    "ln": ln,
    "log": log,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "exp": exp
}