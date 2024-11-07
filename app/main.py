from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from src.history import History
import datetime
import discord
import os

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
    if (
        "Expense added from iPhone" in message.content
        and message.author.id == bot.user.id
    ):
        msg = message.content.split("Expense added from iPhone, ")[1]
        ID = message.channel.id
        name = msg.split("name: ")[1].split(" ")[0]
        price = int(msg.split("price: ")[1])
        time = history.append(ID, name, price)
        print(f"Time: {time}, Action: Added, ID: {ID}, Name: {name}, Price: {price}")
        embed = discord.Embed(
            title="Expense added from iPhone",
            description=f"Name: {name}\nPrice: {price}",
            color=discord.Color.from_str("#FF8A5B"),
        )
        await message.edit(content="", embed=embed)


@bot.tree.command(name="add")
@app_commands.describe(name="Name", price="Price")
async def add(interaction: discord.Interaction, name: str, price: int):
    ID = interaction.channel_id
    time = history.append(ID, name, price)
    print(f"Time: {time}, Action: Added, ID: {ID}, Name: {name}, Price: {price}")
    embed = discord.Embed(
        title="Expense added from Discord",
        description=f"Name: {name}\nPrice: {price}",
        color=discord.Color.from_str("#FCEADE"),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="list")
@app_commands.describe(length="Length")
async def list(interaction: discord.Interaction, length: int = 5):
    ID = interaction.channel_id
    expenses = history.get(ID, length)
    description = ""
    for expense in expenses:
        description += f"{expense['name']} - {expense['price']} - {expense['time'].split(' ')[0]}\n"
    embed = discord.Embed(
        title="Expenses History",
        description=description,
        color=discord.Color.from_str("#FCEADE"),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="set-notify-time")
@app_commands.describe(hour="Hour", minute="Minute")
async def set_notify_time(interaction: discord.Interaction, hour: int, minute: int):
    global notify_time
    try:
        notify_time = datetime.time(hour, minute, 0)
        await interaction.response.send_message(f"Notify time set to {hour}:{minute}")
    except:
        await interaction.response.send_message("Invalid time format")


@tasks.loop(minutes=1)
async def notify():
    await bot.wait_until_ready()
    now = datetime.datetime.now()
    print(f"Checking for notifications at {now.strftime('%H:%M:%S')}", end="\r")
    delta = now - datetime.datetime.combine(datetime.date.today(), notify_time)
    delta = delta.total_seconds()
    # Daily reminder
    if 0 <= delta and delta < 60:
        channels = history.get_channels()
        for channelID in channels:
            channel = bot.get_channel(int(channelID))
            embed = discord.Embed(
                title="Reminder",
                description="Don't forget to log your expenses today!",
                color=discord.Color.from_str("#FCEADE"),
            )
            await channel.send(embed=embed)
    # Monthly reminder
    if now.day == 1 and now.hour == 0 and now.minute == 0:
        channels = history.get_channels()
        for channelID in channels:
            channel = bot.get_channel(int(channelID))
            monthly_payments = history.append_monthly_payments(channelID)
            if len(monthly_payments) > 0:
                description = ""
                for name, price in monthly_payments:
                    description += f"{name} - {price}\n"
                embed = discord.Embed(
                    title="Monthly Payments",
                    description=description,
                    color=discord.Color.from_str("#FCEADE"),
                )
                await channel.send(embed=embed)


bot.run(TOKEN)
