from datetime import datetime

def format_stats(stats: dict) -> str:
    """
    Formats a dictionary of statistics into a readable message.
    """
    total = stats.get("total", 0)
    subscribed = stats.get("subscribed", 0)
    unsubscribed = stats.get("unsubscribed", 0)

    return (
        "📊 <b>Statistics</b>\n\n"
        f"👥 Total users: <b>{total}</b>\n"
        f"✅ Subscribed: <b>{subscribed}</b>\n"
        f"🚫 Unsubscribed: <b>{unsubscribed}</b>"
    )


def format_datetime(dt: datetime | None) -> str:
    """
    Returns the date in DD.MM.YYYY HH:MM format.
    """
    if not dt:
        return "—"
    return dt.strftime("%d.%m.%Y %H:%M")


def extract_username(user) -> str:
    """
    Safely get a user's username for logs or DB.
    """
    if hasattr(user, "username") and user.username:
        return f"@{user.username}"
    if hasattr(user, "first_name"):
        return user.first_name
    return "Nameless"


def clean_channel_name(name: str) -> str:
    """
    Brings the channel name to the correct form @channelname.
    """
    if not name.startswith("@"):
        name = f"@{name}"
    return name.strip()


def split_message(text: str, limit: int = 4096) -> list[str]:
    """
    Splits a long message into parts if it exceeds the Telegram limit (4096 characters).
    """
    return [text[i:i+limit] for i in range(0, len(text), limit)]
