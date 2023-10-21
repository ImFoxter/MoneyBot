import datetime

import discord
from discord.ext import commands
from discord import app_commands

import utils.auxiliary as auxiliary
import utils.datamanager as manager
import views.buttons as buttons

config = auxiliary.config
wallet = auxiliary.wallet
timely = manager.timely

class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Команда для перевірки свого або ж чужого баланса.")
    @app_commands.describe(target="Учасник якого ви бажаєте перевірити баланс.")
    async def __command_balance(self, interact: [discord.Interaction, discord.InteractionResponse], target: discord.Member = None) -> None:
        if target:
            if not target.bot:
                balance = wallet.get_balance(user_id=target.id)
                embed = await auxiliary.build_msg(
                    content=config.MSG_BALANCE_TARGET,
                    placeholders={"{target}": target.mention, "{balance}": balance}
                )
                await interact.response.send_message(embed=embed)
            else:
                embed = await auxiliary.build_msg(
                    content=config.MSG_TARGET_BOT,
                    placeholders={"{target}": target.mention}
                )
                await interact.response.send_message(embed=embed)
        else:
            balance = wallet.get_balance(user_id=interact.user.id)
            embed = await auxiliary.build_msg(
                content=config.MSG_BALANCE_ME,
                placeholders={"{balance}": balance}
            )
            await interact.response.send_message(embed=embed)


    @app_commands.command(name="timely", description="Get timely.")
    async def __command_timely(self, interact: [discord.Interaction, discord.InteractionResponse]) -> None:
        try:
            user =  interact.user
            if timely.check_cooldown(user_id=user.id):
                current_time, cooldown_time = datetime.datetime.now(), datetime.datetime.strptime(
                    timely.get_cooldown(user_id=user.id), "%Y-%m-%d %H:%M:%S.%f"
                )
                if current_time <= cooldown_time:
                    cooldown = auxiliary.countdown(cooldown_time=cooldown_time, current_time=current_time)
                    embed = await auxiliary.build_msg(
                        content=config.MSG_TIMELY_COOLDOWN,
                        placeholders={"{cooldown}": cooldown}
                    )
                    await interact.response.send_message(embed=embed)
            else:
                wallet.give_money(user_id=user.id, amount=config.TIMELY_COINS)
                timely.set_cooldown(
                    user_id=user.id,
                    cooldown=str(datetime.datetime.now() + datetime.timedelta(
                        seconds=config.TIMELY_COOLDOWN
                    ))
                )
                embed = await auxiliary.build_msg(
                    content=config.MSG_TIMELY_ME,
                    placeholders={"{amount}": config.TIMELY_COINS}
                )
                await interact.response.send_message(embed=embed)
        except Exception as e:
            print(e)


    @app_commands.command(name="pay", description="Команда для передачі монет певному учаснику.")
    @app_commands.describe(target="Учасник якому потрібно передати монети.", amount="Кількісь монет.")
    async def __command_pay(self, interact: [discord.Interaction, discord.InteractionResponse], target: discord.Member, amount: int) -> None:
        user = interact.user
        balance = wallet.get_balance(user_id=user.id)
        if balance < amount:
            embed = await auxiliary.build_msg(
                content=config.MSG_PAY_NO,
                placeholders={"{amount_shortage}": amount - balance, "{balance}": balance}
            )
            await interact.response.send_message(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = config.PAY_TITLE.replace("{amount}", str(amount))
            embed.add_field(name=config.PAY_USER, value=user.mention, inline=True)
            embed.add_field(name=config.PAY_TARGET, value=target.mention, inline=True)
            if config.PAY_ICON:
                embed.set_thumbnail(url=user.avatar.url if user.avatar.url else config.PAY_DEFAULT)
            r, g, b = auxiliary.hex_in_rgb(hex_code=config.PAY_COLOR)
            embed.colour = discord.Colour.from_rgb(r=r, g=g, b=b)
            await interact.response.send_message(
                embed=embed,
                view=buttons.PayMenu(
                    user=user,
                    target=target,
                    amount=amount,
                    datetime=datetime.datetime.now().strftime("%H:%M:%S, %d.%m, %Y")
                )
            )


    @app_commands.command(name="give", description="Команда для видавання монет певному учаснику.")
    @app_commands.describe(target="Учасник якому потрібно видати монети.", amount="Кількісь монет.")
    async def __command_give(self, interact: [discord.Interaction, discord.InteractionResponse], target: discord.Member, amount: int) -> None:
        if not target.bot:
            balance = wallet.give_money(user_id=target.id, amount=amount)
            embed_user = await auxiliary.build_msg(
                content=config.MSG_GIVE_ME,
                placeholders={"{target}": target.mention, "{amount}": amount, "{balance}": balance}
            )
            await interact.response.send_message(embed=embed_user)
            embed_target = await auxiliary.build_msg(
                content=config.MSG_GIVE_TARGET,
                placeholders={"{admin}": interact.user.mention, "{amount}": amount, "{balance}": balance}
            )
            await target.send(embed=embed_target)
        else:
            embed = await auxiliary.build_msg(
                content=config.MSG_TARGET_BOT,
                placeholders={"{target}": target.mention}
            )
            await interact.response.send_message(embed=embed)


    @app_commands.command(name="take", description="Команда для позбавлення певної кількості монет в певного учасника.")
    @app_commands.describe(target="Учасник якого потрібно позбавити монети.", amount="Кількісь монет.")
    async def __command_take(self, interact: [discord.Interaction, discord.InteractionResponse], target: discord.Member, amount: int) -> None:
        if not target.bot:
            balance = wallet.get_balance(user_id=target.id)
            if balance > amount:
                new_balance = wallet.take_money(target_id=target.id, amount=amount)
                embed_user = await auxiliary.build_msg(
                    content=config.MSG_TAKE_ME,
                    placeholders={"{target}": target.mention, "{amount}": amount, "{balance}": new_balance}
                )
                await interact.response.send_message(embed=embed_user)
                embed_target = await auxiliary.build_msg(
                    content=config.MSG_TAKE_TARGET,
                    placeholders={"{admin}": interact.user.mention, "{amount}": amount, "{balance}": new_balance}
                )
                await target.send(embed=embed_target)
            else:
                embed = await auxiliary.build_msg(
                    content=config.MSG_TAKE_NO,
                    placeholders={"{target}": target.mention, "{amount}": amount, "{balance}": balance}
                )
                await interact.response.send_message(embed=embed)
        else:
            embed = await auxiliary.build_msg(
                content=config.MSG_TARGET_BOT,
                placeholders={"{target}": target.mention}
            )
            await interact.response.send_message(embed=embed)


    # TODO: "Next update [Transactions] - 1.5.0"
    # @app_commands.command(name="transactions", description="Take money in member.")
    # @commands.command(name="q")
    # async def __command_transactions(self, ifx: commands.Context) -> None:
    #     try:
    #         paginator = auxiliary.Paginator(user=ifx.author)
    #         await ifx.send(content="Go", view=bti.TransPegeMenu(user=ifx.author, paginator=paginator))
    #     except Exception as e:
    #         print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot), guild=None)