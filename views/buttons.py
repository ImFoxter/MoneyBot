import discord
import utils.datamanager as manager
import utils.auxiliary as auxiliary

config = manager.config
wallet = manager.wallet

class PayMenu(discord.ui.View):
    def __init__(self,
                 user: discord.Member = None,
                 target: discord.Member = None,
                 amount: int = None,
                 datetime: str = None
                 ):
        super().__init__(timeout=config.PAY_TIME)
        self.user = user
        self.target = target
        self.amount = amount
        self.datetime = datetime

        self.button_confirm = discord.ui.Button(
            label=config.PAY_CONFIRM_LABLE,
            custom_id="PayButton-button_confirm",
            style=auxiliary.check_style(style=config.PAY_CONFIRM_STYLE),
            disabled=False
        )
        self.button_center = discord.ui.Button(
            label=config.PAY_CENTER_LABLE,
            custom_id="PayButton-button_center", style=discord.ButtonStyle.gray,
            disabled=True
        )
        self.button_cancel = discord.ui.Button(
            label=config.PAY_CANCEL_LABLE,
            custom_id="PayButton-button_cancel",
            style=auxiliary.check_style(style=config.PAY_CANCEL_STYLE),
            disabled=False
        )

        self.add_item(self.button_confirm)
        if config.PAY_CENTER_ENABLE:
            self.add_item(self.button_center)
        self.add_item(self.button_cancel)

        self.button_confirm.callback = self.__button_confirm
        self.button_cancel.callback = self.__button_cancel

    async def __button_confirm(self, interact: [discord.Interaction, discord.InteractionResponse], /) -> None:
        if self.user.id == interact.user.id:
            await interact.message.edit(view=None)
            wallet.pay_money(user_id=self.user.id, target_id=self.target.id, amount=self.amount, datatime=self.datetime)
            embed_user = await auxiliary.build_msg(
                content=config.MSG_PAY_ME,
                placeholders={"{target}": self.target.mention, "{amount}": self.amount, "{balance}": wallet.get_balance(user_id=self.user.id)}
            )
            embed_target = await auxiliary.build_msg(
                content=config.MSG_PAY_TARGET,
                placeholders={"{target}": self.user.mention, "{amount}": self.amount, "{balance}": wallet.get_balance(user_id=self.target.id) }
            )
            await interact.response.send_message(embed=embed_user)
            await self.target.send(embed=embed_target)
        else:
            embed = await auxiliary.build_msg(
                content=config.MSG_PAY_SESSION
            )
            await interact.response.send_message(embed=embed)
    async def __button_cancel(self, interact: [discord.Interaction, discord.InteractionResponse], /) -> None:
        if self.user.id == interact.user.id:
            await interact.message.edit(view=None)
            embed = await auxiliary.build_msg(
                content=config.MSG_PAY_CANCEL,
                placeholders={"{amount}": self.amount}
            )
            await interact.response.send_message(embed=embed)
        else:
            embed = await auxiliary.build_msg(
                content=config.MSG_PAY_SESSION
            )
            await interact.response.send_message(embed=embed)



# TODO: "Next update [Transactions] - 1.5.0"
# class TransPegeMenu(discord.ui.View):
#     def __init__(self, user: discord.Member, paginator):
#         super().__init__()
#         self.user = user
#         self.paginator = paginator
#
#         self.button_back = discord.ui.Button(label="<-", custom_id="TransPegeMenu-button_back", style=discord.ButtonStyle.red, disabled=False)
#         self.button_next = discord.ui.Button(label="->", custom_id="TransPegeMenu-button_next", style=discord.ButtonStyle.green, disabled=False)
#
#         self.add_item(self.button_back)
#         self.add_item(self.button_next)
#
#         self.button_back.callback = self.__button_back
#         self.button_next.callback = self.__button_next
#
#     async def __button_next(self, interact: discord.Interaction, /):
#         try:
#             if self.user.id == interact.user.id:
#                 t = self.paginator.next_page()
#                 embed = self.create(trans=t)
#                 await interact.message.edit(embed=embed)
#             else:
#                 await interact.response.send_message("No session!")
#         except Exception as e:
#             print(e)
#     async def __button_back(self, interact: discord.Interaction, /):
#         try:
#             if self.user.id == interact.user.id:
#                 t = self.paginator.prev_page()
#                 await interact.response.send_message(t)
#             else:
#                 await interact.response.send_message("No session!")
#         except Exception as e:
#             print(e)
#
#     def create(self, trans: list) -> discord.Embed:
#         text = [f"### Page: Transaction: {self.user.mention}"]
#         number = 0
#         for value in trans:
#             number += 1
#             user = discord.utils.get(self.user.guild.members, id=value['user'])
#             pars = f"**{number}#** ``{value['amount']}`` **->** {user.mention}, ``{value['datatime']}``"
#             text.append(pars)
#
#         embed = discord.Embed()
#         embed.description = "\n".join(text)
#         embed.colour = discord.Colour.from_rgb(204, 0, 0)
#         return embed