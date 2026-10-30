from setting import SETTINGS
import discord
import random
import os
import json
import requests
from database_tempo_decomposizione import tempi_decomposizione
from colori_indifferenziata import colori
from discord.ext import commands
from green_tips import green_tip
from quests import daily_missions


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Abbiamo fatto l'accesso come {bot.user}")
    canale = bot.get_channel(1555861319788273726)
    await canale.send("🌍 Ciao a tutti! Proteggiamo il pianeta! ♻️")
    with open(r"image_robot.png", 'rb') as f:
        picture = discord.File(f)
        await canale.send(file=picture)
    
    
@bot.command()
async def cosa_è_inquinamento(ctx):
    await ctx.send("L'inquinamento è l'introduzione di sostanze, rifiuti o forme di energia dannose (chimiche, fisiche o biologiche) in un ambiente naturale (aria, acqua, suolo), che altera gli equilibri ecologici e risulta nocivo per la salute umana, animale e vegetale.")

@bot.command()
async def dopo_quanto_decompone(ctx, materiale:str):
    if materiale in tempi_decomposizione:
        if tempi_decomposizione[materiale][1] == None:
            massimo = "non si sa"
        else:
            massimo = tempi_decomposizione[materiale][1]
        await ctx.send(f"{materiale} ci mette minimo {tempi_decomposizione[materiale][0]} anni e massimo {massimo}")
    else:
        await ctx.send("il materiale non è nel database, scrivi materiali_database per vedere quali esistono")
        

@bot.command()
async def materiali_database(ctx):
    for materiale in tempi_decomposizione:
        await ctx.send(materiale)

@bot.command()
async def colori_raccolta_differenziata(ctx):
    for colore,materiale in colori.items():
        await ctx.send(f"{colore} → {materiale}")
    
@bot.command()
async def green_tips(ctx):
    await ctx.send(random.choice(green_tip))
    
with open("account.json", "r") as file:
    account = json.load(file)
    
def salva_account():
    with open("account.json", "w") as file:
        json.dump(account, file, indent=4)
    
@bot.command()
async def crea_account(ctx, nome:str):
    if nome not in account:
        account[nome] = 0
        salva_account()
        await ctx.send("Account aggiunto correttamente!")

    elif nome in account:
        await ctx.send("Account già esistente!")
    
@bot.command()
async def aggiungi_punti(ctx, nome:str, punti:int):
    if nome in account:
        account[nome] += punti
        salva_account()
        await ctx.send("punti aggiunti correttamente")
    else:
        await ctx.send("l'account non esiste")
     
@bot.command()
async def missione_giornaliera(ctx):
    missione = random.choice(daily_missions)
    valore = random.randint(10,30)
    await ctx.send(f"""{missione}
                   se completata, questa missione vale, {valore}""")
    
@bot.command()
async def utenti(ctx):
    for nome, punti in account.items():
        await ctx.send(f"{nome}: {punti} ECO")
        
@bot.command()
async def utente(ctx, nome:str):
    if nome not in account:
        await ctx.send("l'account non esiste")
    else:
        await ctx.send(account[nome])










bot.run(SETTINGS["TOKEN"])