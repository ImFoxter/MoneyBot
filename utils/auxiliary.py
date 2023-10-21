import os
from typing import Tuple

import discord
import utils.datamanager as manager

config = manager.config
wallet = manager.wallet

# TODO: "Next update [Transactions] - 1.5.0"
# class Paginator:
#     def __init__(self, user: discord.Member):
#         self.user = user
#         self.items = wallet.get_transactions(user_id=user.id)
#         self.items_per_page = 5
#         self.current_page = 0
#
#     def get_current_page_items(self):
#         start_idx = self.current_page * self.items_per_page
#         end_idx = start_idx + self.items_per_page
#         return self.items[start_idx:end_idx]
#
#     def next_page(self):
#         if self.current_page < len(self.items) // self.items_per_page:
#             self.current_page += 1
#         return self.get_current_page_items()
#
#     def prev_page(self):
#         if self.current_page > 0:
#             self.current_page -= 1
#         return self.get_current_page_items()


# TODO: "Message builder with PLACEHOLDERS."
async def build_msg(content: dict, placeholders: dict = None) -> discord.Embed:
    description = "\n".join(content["text"])

    if placeholders:
        for placeholder, value in placeholders.items():
            description = description.replace(placeholder, str(value))

    embed = discord.Embed()
    embed.description = description
    r, g, d = hex_in_rgb(hex_code=content["color"])
    embed.colour = discord.Colour.from_rgb(r=r, g=g, b=d)
    return embed

# TODO: "Countdown."
def countdown(cooldown_time, current_time) -> str:
    time_difference = (cooldown_time - current_time)
    remaining_days = time_difference.days
    remaining_seconds = time_difference.seconds
    remaining_hours, remaining_seconds = divmod(remaining_seconds, 3600)
    remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
    return format_duration(remaining_days, remaining_hours, remaining_minutes, remaining_seconds)

# TODO: "Formatting units."
def format_units(num: int, singular: str, plural_one: str, plural_two: str) -> str:
    if 10 <= num % 100 <= 20:
        return f"{num}{plural_one}"
    elif num % 10 == 1:
        return f"{num} {singular}"
    elif 2 <= num % 10 <= 4:
        return f"{num}{plural_one}"
    else:
        return f"{num}{plural_two}"

# TODO: "Duration formatting."
def format_duration(days: int, hours: int, minutes: int, seconds: int) -> str:
    result = []
    if days > 0:
        result.append(format_units(days,
            config.TIME_FORM_DAYS[0],
            config.TIME_FORM_DAYS[1],
            config.TIME_FORM_DAYS[2])
        )
    if hours > 0:
        result.append(format_units(hours,
            config.TIME_FORM_HOURS[0],
            config.TIME_FORM_HOURS[1],
            config.TIME_FORM_HOURS[2]
            )
        )
    if minutes > 0:
        result.append(format_units(minutes,
            config.TIME_FORM_MINUTES[0],
            config.TIME_FORM_MINUTES[1],
            config.TIME_FORM_MINUTES[2]
        )
        )
    if seconds > 0:
        result.append(format_units(seconds,
            config.TIME_FORM_SECONDS[0],
            config.TIME_FORM_SECONDS[1],
            config.TIME_FORM_SECONDS[2]
        )
        )
    return "".join(result)

# TODO: "Conversion of HEX to RGB."
def hex_in_rgb(hex_code: str) -> Tuple[int, int, int]:
    r, g, b = tuple(int(hex_code.strip("#")[i:i+2], 16) for i in (0, 2, 4))
    return r, g, b

def check_style(style: str) -> discord.ButtonStyle:
    if style == "primary":
        return discord.ButtonStyle.primary
    elif style == "green":
        return discord.ButtonStyle.green
    elif style == "red":
        return discord.ButtonStyle.red
    elif style == "gray":
        return discord.ButtonStyle.gray
    else:
        raise ValueError("[ERROR]: Button style", style, "not found. Please check the configuration!")

# TODO: "Manager of management of COGS."
async def cog_manager(bot, dirk: str, mode: str) -> None:
    for file_name in os.listdir(dirk):
        if not file_name.startswith("__") and file_name.endswith(".py"):
            cog = (dirk + file_name[:-3]).replace("/", ".")
            try:
                if  mode == "load":
                    await bot.load_extension(cog)
                elif  mode == "unload":
                    await bot.unload_extension(cog)
                elif  mode == "reload":
                    await bot.reload_extension(cog)
                else:
                    raise ValueError("[ERROR]: Mode:", mode, "not found.")
            except Exception as error:
                raise error