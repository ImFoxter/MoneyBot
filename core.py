import asyncio
import json
import os

import discord
from discord.ext import commands
from colorama import init, Fore, Back
from utils.auxiliary import cog_manager, config
from views.buttons import PayMenu

init(autoreset=True)

async def print_on_start():
    create_wallet = ""
    path_to_wallet: str = "./assets/data/user_wallet.json"
    path_to_timely: str = "./assets/data/user_timely.json"
    path_to_config: str = "./assets/data/config.yml"
    if not os.path.exists(path=path_to_wallet):
        with open(file=path_to_wallet, mode="w", encoding="UTF-8") as file:
            json.dump({"WALLET": {}}, fp=file, indent=5, sort_keys=False, ensure_ascii=False)
            create_wallet: str = """\n[INFO] >> File "user_wallet.json" created."""
    elif not os.path.exists(path=path_to_timely):
        with open(file=path_to_timely, mode="w", encoding="UTF-8") as file:
            json.dump({"COOLDOWN":{}}, fp=file, indent=5, sort_keys=False, ensure_ascii=False)
            create_wallet: str = """\n[INFO] >> File "user_timely.json" created."""

    # elif not os.path.exists(path=path_to_config):
    #     with open(file=path_to_config, mode="w", encoding="UTF-8") as file:
    #         yaml.dump({"WALLET": {}}, fp=file, indent=5, sort_keys=False, ensure_ascii=False)
    #         create_wallet: str = """\n[INFO] >> File "user_wallet.json" created."""

    print(
""" __       __                                                _______               __     
/  \     /  |                                              /       \             /  |    
$$  \   /$$ |  ______   _______    ______   __    __       $$$$$$$  |  ______   _$$ |_   
$$$  \ /$$$ | /      \ /       \  /      \ /  |  /  |      $$ |__$$ | /      \ / $$   |  
$$$$  /$$$$ |/$$$$$$  |$$$$$$$  |/$$$$$$  |$$ |  $$ |      $$    $$< /$$$$$$  |$$$$$$/   
$$ $$ $$/$$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$ |      $$$$$$$  |$$ |  $$ |  $$ | __ 
$$ |$$$/ $$ |$$ \__$$ |$$ |  $$ |$$$$$$$$/ $$ \__$$ |      $$ |__$$ |$$ \__$$ |  $$ |/  |
$$ | $/  $$ |$$    $$/ $$ |  $$ |$$       |$$    $$ |      $$    $$/ $$    $$/   $$  $$/ 
$$/      $$/  $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$$ |      $$$$$$$/   $$$$$$/     $$$$/  
                                           /  \__$$ |                                    
                                           $$    $$/                                     
                                            $$$$$$/
    """.replace("$", Back.LIGHTYELLOW_EX + Fore.LIGHTYELLOW_EX + "$" + Back.RESET)
        .replace("_", Fore.YELLOW + "_" + Fore.RESET)
        .replace("-", Fore.YELLOW + "-" + Fore.RESET)
        .replace("/", Fore.YELLOW + "/" + Fore.RESET)
        .replace("\\", Fore.YELLOW + "\\" + Fore.RESET)
        .replace("|", Fore.YELLOW + "|" + Fore.RESET)
    )
    print(
f"""[INFO] >> Bot started...{create_wallet}
[INFO] >> Bot launched successfully.
    """.replace("[", Fore.WHITE + "[" + Fore.RESET)
        .replace("]", Fore.WHITE + "]" + Fore.RESET)
        .replace("INFO", Fore.YELLOW + "INFO" + Fore.RESET)
        .replace(">", Fore.LIGHTCYAN_EX + ">" + Fore.WHITE)
        .replace("user_wallet.json", Fore.YELLOW + "user_wallet.json" + Fore.WHITE)
    )

class ImFoxterBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents, description="My bot!", )

    async def on_ready(self) -> None:
        if config.CONSOLE_HELP:
            await print_on_start()
        else:
            print("Bot is ready!")
        await bot.tree.sync(guild=None)

bot = ImFoxterBot()

async def core():
    await asyncio.gather(
        cog_manager(bot=bot, dirk="cogs/", mode="load"),
        bot.start(str(config.BOT_TOKEN), reconnect=True)
    )
asyncio.run(core())