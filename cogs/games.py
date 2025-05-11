from discord.ext import commands
import random
import requests
import json
import asyncio
import discord
from discord import app_commands

# API Trivia URL
trivia_api_url = "https://opentdb.com/api.php?amount=1"

categories = {
    "Geral": 0,
    "Livros": 10,
    "Filmes": 11,
    "Música": 12,
    "Teatro": 13,
    "Televisão": 14,
    "Vídeo games": 15,
    "Ciência e natureza": 17,
    "Computadores": 18,
    "Matemática": 19,
    "Mitologia": 20,
    "Esportes": 21,
    "Geografia": 22,
    "História": 23,
    "Política": 24,
    "Arte": 25,
    "Celebridades": 26,
    "Animais": 27,
    "Veículos": 28,
    "Quadrinhos": 29,
    "Desenhos animados": 32
}

# Definindo os jogadores e itens do RPG
jogadores = {}

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.nivel = 1
        self.experiencia = 0
        self.saude = 100
        self.ataque = 10
        self.defesa = 10
        self.dinheiro = 0

    def subir_nivel(self):
        if self.experiencia >= self.nivel * 10:
            self.nivel += 1
            self.experiencia = 0
            self.saude += 10
            self.ataque += 5
            self.defesa += 5
            return True
        return False

poderes = {
    "fogo": {"ataque": 20, "custo": 10},
    "cura": {"saúde": 20, "custo": 10},
    "escudo": {"defesa": 20, "custo": 10}
}

itens = {
    "espada": {"ataque": 10},
    "escudo": {"defesa": 10},
    "poção": {"saúde": 10}
}

monsters = [
    {"name": "Goblin", "health": 20, "attack": 5},
    {"name": "Orc", "health": 30, "attack": 10},
    {"name": "Dragon", "health": 50, "attack": 15}
]

# Definindo a classe do cog para o bot
class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------- /roll ----------------------------------------------------
    @app_commands.command(name="roll", description="Rola um dado de 6 lados.")
    async def roll(self, interaction: discord.Interaction, arg: int = None):
        if arg is None:
            result = ', '.join(str(random.randint(1, 6)) for _ in range(1))
            await interaction.response.send_message(result)
        else:    
            if arg.isdigit():
                n = int(arg)
                if n > 10:
                    n = 10
                    await interaction.response.send_message("Máximo de rolls ao mesmo tempo excedido. (10)")
                result = '\n'.join(str(random.randint(1, 6)) for _ in range(n))
                await interaction.response.send_message(result)
            else:
                await interaction.response.send_message("Argumento mal introduzido")

    @app_commands.command(name="guess", description="Tente adivinhar o número entre 1 e 100.")
    async def guess(self, interaction: discord.Interaction):
        number = random.randint(1, 100)
        await interaction.response.send_message("Adivinhe um número entre 1 e 100!")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()

        for i in range(10):
            try:
                guess = await self.bot.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await interaction.followup.send("Você não respondeu a tempo. Fim de jogo!")
                return

            user_guess = int(guess.content)
            if user_guess == number:
                await interaction.followup.send("Você acertou! Parabéns!")
                return
            elif user_guess < number:
                await interaction.followup.send("O número é maior!")
            else:
                await interaction.followup.send("O número é menor!")

        await interaction.followup.send(f"Suas tentativas acabaram! O número era {number}.")


    @app_commands.command(name="trivia", description="Jogo de trivia com perguntas e respostas.")
    async def trivia(self, interaction: discord.Interaction, category: str = "Geral", difficulty: str = "easy", num_questions: int = 1):
        if category not in categories:
            await interaction.response.send_message(f"Desculpe, {interaction.user.mention}, categoria inválida. Escolha uma das seguintes categorias: {', '.join(categories.keys())}")
            return

        if difficulty not in ["easy", "medium", "hard"]:
            await interaction.response.send_message(f"Desculpe, {interaction.user.mention}, dificuldade inválida. Escolha entre: easy, medium, hard.")
            return

        if num_questions < 1 or num_questions > 50:
            await interaction.response.send_message(f"Desculpe, {interaction.user.mention}, número de perguntas inválido. Escolha entre 1 e 50.")
            return

        # Primeira resposta obrigatória da interaction
        await interaction.response.send_message(f"Iniciando trivia com {num_questions} perguntas na categoria **{category}** e dificuldade **{difficulty}**...")
        
        params = {
            "amount": num_questions,
            "category": categories[category],
            "difficulty": difficulty,
            "type": "multiple"
        }

        response = requests.get(trivia_api_url, params=params)
        data = json.loads(response.text)
        results = data['results']

        num_correct = 0

        def check_answer(message):
            return message.author == interaction.user and message.channel == interaction.channel and message.content.isdigit()

        for idx, result in enumerate(results):
            question = result['question']
            correct_answer = result['correct_answer']
            incorrect_answers = result['incorrect_answers']
            answers = incorrect_answers + [correct_answer]
            random.shuffle(answers)

            answer_string = "\n".join([f"{i+1}. {answers[i]}" for i in range(len(answers))])
            await interaction.followup.send(f"**Pergunta {idx+1} de {len(results)}:** {question}\n\n{answer_string}")

            try:
                msg = await self.bot.wait_for('message', check=check_answer, timeout=30.0)
            except asyncio.TimeoutError:
                await interaction.followup.send(f"Tempo esgotado! A resposta correta era: **{correct_answer}**")
                continue

            user_answer = int(msg.content)
            if user_answer == answers.index(correct_answer) + 1:
                await interaction.followup.send(f"✅ Correto! A resposta era: **{correct_answer}**")
                num_correct += 1
            else:
                await interaction.followup.send(f"❌ Errado. A resposta correta era: **{correct_answer}**")

        await interaction.followup.send(f"🏁 Fim da trivia! Você acertou **{num_correct}** de **{len(results)}** perguntas.")


# Função para carregar o cog
async def setup(bot):
    await bot.add_cog(games(bot))
