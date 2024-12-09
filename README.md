# CostCord

This is a Discord bot that can help you keep your expenses.

## Installation

### Set your bot token

Copy the `.env.example` file to `.env` and set your bot token. Inside the `.env` file, you should have a line like this:

```env
TOKEN=your_bot_token
```

### Docker

You can run the bot using Docker. Just run the following command:

```bash
docker compose up -d
```

### Manual

You can also run the bot manually. First, install the dependencies:

```bash
pip install -r src/requirements.txt
```

Then, run the bot:

```bash
python src/main.py
```

## Usage

To use the bot, you can send the following commands:

- `/add <name> <value> (past_days)`: Add an expense. If you provide the `past_days` argument, the expense will be added to the past days.
- `/list (length)`: List the expenses. If you provide the `length` argument, the expenses from the last `length` items will be listed.
- `/set-notify-time <hour> <minute>`: Set the time when the bot will notify you every day.
- `/ping`: Check if the bot is alive.
