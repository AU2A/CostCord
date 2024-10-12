from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from src.history import History
import datetime, discord, os

load_dotenv()

TOKEN = os.getenv("TOKEN")

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


@bot.event
async def on_message(message):
    if "Send from iPhone" in message.content and message.author.id == bot.user.id:
        msg = message.content.split("Send from iPhone, ")[1]
        ID = message.channel.id
        name = msg.split("name=")[1].split(" ")[0]
        price = int(msg.split("price=")[1])
        time = history.append(ID, name, price)
        print(f"Time: {time}, Action: Added, ID: {ID}, Name: {name}, Price: {price}")
        embed = discord.Embed(
            title="Expense added",
            description=f"Name: {name}\nPrice: {price}",
            color=discord.Color.gray(),
        )
        await message.edit(content="", embed=embed)


@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="add")
@app_commands.describe(name="Name", price="Price")
async def add(interaction: discord.Interaction, name: str, price: int):
    ID = interaction.channel_id
    time = history.append(ID, name, price)
    print(f"Time: {time}, Action: Added, ID: {ID}, Name: {name}, Price: {price}")
    embed = discord.Embed(
        title="Expense added",
        description=f"Name: {name}\nPrice: {price}",
        color=discord.Color.orange(),
    )
    await interaction.response.send_message(embed=embed)


@tasks.loop(minutes=1)
async def notify():
    await bot.wait_until_ready()
    delta = datetime.datetime.now() - datetime.datetime.combine(
        datetime.date.today(), notify_time
    )
    delta = delta.total_seconds()
    if 0 <= delta and delta < 60:
        channels = history.get_channels()
        for channelID in channels:
            channel = bot.get_channel(int(channelID))
            embed = discord.Embed(
                title="Reminder",
                description="Don't forget to log your expenses today!",
                color=discord.Color.green(),
            )
            await channel.send(embed=embed)


bot.run(TOKEN)
