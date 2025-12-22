# Boost Bot

<p align="center">
  <img src="assets/demo.gif" alt="Bot usage demonstration">
</p>

## Description

**Boost Bot** is a Telegram bot designed to enforce mandatory subscription to specified channels before granting access to content. It helps to increase the audience of your channels by requiring users to subscribe to receive exclusive materials.

## Features

-   **User Registration:** Automatically saves new users to the database.
-   **Admin Panel:** View user statistics via a command.
-   **Channel Management:** Add channels for mandatory subscription using commands.

## Technology Stack

-   **aiogram 3.x:** Asynchronous framework for creating Telegram bots.
-   **SQLAlchemy 2.0:** ORM for working with the database in asynchronous mode.
-   **aiosqlite:** Asynchronous driver for working with SQLite.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/xnskxkx/boost-bot.git
    cd boost-bot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root of the project (copy from `.env.example`) and specify your token and administrator ID:
    ```
    TG_BOT_TOKEN="YOUR_TELEGRAM_TOKEN"
    USER_ID_FOR_ADMIN="YOUR_TELEGRAM_ID"
    ```

## Running

To start the bot, run the command:
```bash
python run.py
```