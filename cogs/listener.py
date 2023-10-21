import asyncio
import collections
import random
import re

import discord
from discord.ext import commands
import utils.datamanager as manager

wallet = manager.wallet
config = manager.config

class Listener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_timers = collections.defaultdict(asyncio.Event)

    async def create_user_timer(self, member: discord.Member) -> None:
        while not self.user_timers[str(member.id)].is_set():
            if config.VOICE_ENABLE:
                coins: int = random.randint(config.VOICE_MIN, config.VOICE_MAX)
            else:
                coins: int = config.VOICE_COINS
            await asyncio.sleep(delay=config.VOICE_COOLDOWN)
            wallet.give_money(user_id=member.id, amount=coins)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        if after.channel:
            self.user_timers[str(member.id)].clear()
            await self.create_user_timer(member=member)
        elif before.channel:
            self.user_timers[f"{member.id}"].set()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        coins: float = 0
        if config.CHAT_ENABLE:
            if len(message.content) >= config.CHAT_CON_SYMBOLS:
                coins = len(message.content) * (config.CHAT_STABILIZER / config.CHAT_MULTIPLIER)
        elif not config.CHAT_BLACK_WORDS:
            if len(message.content) >= config.CHAT_DEF_SYMBOLS:
                coins = config.CHAT_COINS

        if config.CHAT_BLACK_WORDS:
            if len(message.content) >= config.CHAT_CON_SYMBOLS:
                for black_words in config.CHAT_BLACK_WORDS:
                    if re.search(re.escape(black_words.split("; ")[0]), message.content):
                        coins = (len(message.content) * (config.CHAT_STABILIZER / config.CHAT_MULTIPLIER)) - float(black_words.split("; ")[1])
                        break
                else:
                    coins = len(message.content) * (config.CHAT_STABILIZER / config.CHAT_MULTIPLIER)
        elif not config.CHAT_ENABLE:
            if len(message.content) >= config.CHAT_DEF_SYMBOLS:
                coins = config.CHAT_COINS
        wallet.give_money(user_id=message.author.id, amount=int(coins))

async def setup(bot: commands.Bot):
    await bot.add_cog(Listener(bot))