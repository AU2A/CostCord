from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from src.history import History
import datetime, discord, os

load_dotenv()

TOKEN = os.getenv("TOKEN")
channelID = os.getenv("Notification-Channel-ID")

notify_time = datetime.time(20, 0, 0)

history = History()

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        notify.start()
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="add")
@app_commands.describe(name="Name", price="Price")
async def add(interaction: discord.Interaction, name: str, price: int):
    history.append(name, price)
    await interaction.response.send_message(f"Name: {name}, Price: {price}")


@tasks.loop(minutes=1)
async def notify():
    delta = datetime.datetime.now() - datetime.datetime.combine(
        datetime.date.today(), notify_time
    )
    delta = delta.total_seconds()
    if 0 <= delta and delta < 60:
        channel = bot.get_channel(int(channelID))
        await channel.send("Time to update your expenses!")


bot.run(TOKEN)
