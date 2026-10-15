"""Bots educativos: memes por tema y consejos para reducir residuos."""
import asyncio
import os
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent
MEMES = BASE / 'images'
RESIDUOS = {
    'papel': 'Reutiliza ambas caras y separa el papel limpio y seco para reciclar.',
    'plastico': 'Reduce envases de un solo uso. Limpia y separa los aceptados por tu reciclador local.',
    'vidrio': 'Reutiliza frascos y entrega los envases en un punto de reciclaje.',
    'pilas': 'Lleva las pilas a un centro de recogida especial; no las mezcles con la basura común.',
    'organico': 'Los restos vegetales pueden aprovecharse en compost si dispones de un sistema adecuado.',
}

def consejo(material):
    key = material.strip().lower().replace('á', 'a').replace('ó', 'o')
    return RESIDUOS.get(key, 'Prueba: papel, plastico, vidrio, pilas u organico.')

def seleccionar_meme(tema='programacion', rng=random):
    if tema not in {'programacion', 'animales'}:
        raise ValueError('Tema no válido')
    archivos = sorted(p for p in (MEMES / tema).glob('*') if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif'})
    if not archivos:
        raise FileNotFoundError('Añade imágenes en la carpeta del tema.')
    # Los nombres que empiezan por raro_ tienen menor probabilidad.
    return rng.choices(archivos, weights=[1 if p.name.startswith('raro_') else 5 for p in archivos], k=1)[0]

def crear_bot():
    import discord
    from discord.ext import commands
    import requests

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    async def enviar_meme(ctx, tema):
        try:
            await ctx.send(file=discord.File(seleccionar_meme(tema)))
        except (ValueError, FileNotFoundError) as error:
            await ctx.send(str(error))

    @bot.command()
    async def mem(ctx):
        await enviar_meme(ctx, 'programacion')

    @bot.command()
    async def animales(ctx):
        await enviar_meme(ctx, 'animales')

    @bot.command()
    async def reciclar(ctx, *, material=''):
        await ctx.send(consejo(material))

    @bot.command()
    async def reto(ctx):
        await ctx.send(random.choice(['Lleva una botella reutilizable.', 'Reutiliza una hoja antes de desecharla.', 'Separa los residuos que acepte tu centro local.']))

    @bot.command()
    async def duck(ctx):
        def obtener():
            response = requests.get('https://random-d.uk/api/random', timeout=15)
            response.raise_for_status()
            url = response.json()['url']
            if not url.startswith('https://'):
                raise ValueError('La API devolvió una dirección no válida')
            return url
        try:
            await ctx.send(await asyncio.to_thread(obtener))
        except (requests.RequestException, KeyError, ValueError):
            await ctx.send('No se pudo obtener la imagen del pato. Intenta más tarde.')

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Escribe $help para ver los comandos.')
        else:
            await ctx.send('No se pudo completar el comando. Revisa los datos e inténtalo otra vez.')
    return bot

if __name__ == '__main__':
    token = os.environ.get('DISCORD_TOKEN')
    if not token:
        raise SystemExit('Configura DISCORD_TOKEN antes de iniciar el bot.')
    crear_bot().run(token)
