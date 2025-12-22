from datetime import datetime

def format_stats(stats: dict) -> str:
    """
    Форматирует словарь статистики в читаемое сообщение.
    """
    total = stats.get("total", 0)
    subscribed = stats.get("subscribed", 0)
    unsubscribed = stats.get("unsubscribed", 0)

    return (
        "📊 <b>Статистика</b>\n\n"
        f"👥 Всего пользователей: <b>{total}</b>\n"
        f"✅ Подписаны: <b>{subscribed}</b>\n"
        f"🚫 Не подписаны: <b>{unsubscribed}</b>"
    )


def format_datetime(dt: datetime | None) -> str:
    """
    Возвращает дату в формате DD.MM.YYYY HH:MM.
    """
    if not dt:
        return "—"
    return dt.strftime("%d.%m.%Y %H:%M")


def extract_username(user) -> str:
    """
    Безопасно получить username пользователя для логов или БД.
    """
    if hasattr(user, "username") and user.username:
        return f"@{user.username}"
    if hasattr(user, "first_name"):
        return user.first_name
    return "Без имени"


def clean_channel_name(name: str) -> str:
    """
    Приводит имя канала к корректному виду @channelname.
    """
    if not name.startswith("@"):
        name = f"@{name}"
    return name.strip()


def split_message(text: str, limit: int = 4096) -> list[str]:
    """
    Разбивает длинное сообщение на части, если оно превышает лимит Telegram (4096 символов).
    """
    return [text[i:i+limit] for i in range(0, len(text), limit)]
