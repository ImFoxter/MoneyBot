import re
import json
import yaml

class ConfigYML:
    def __init__(self) -> None:
        self.path_to_file = "./assets/data/config.yml"
        self.data = self.__data()

        # TODO: "Bot settings."
        self.BOT_TOKEN: str = self.data["settings"]["bot-token"]
        self.CONSOLE_HELP: bool = self.data["settings"]["console-msg"]

        # TODO: "Timely getter."
        self.TIMELY_COOLDOWN: int = self.data["timely-getter"]["cooldown"]
        self.TIMELY_COINS: int = self.data["timely-getter"]["coins"]

        # TODO: "Voice getter."
        self.VOICE_COOLDOWN: int = self.data["voice-getter"]["default"]["cooldown"]
        self.VOICE_COINS: int = self.data["voice-getter"]["default"]["coins"]
        self.VOICE_ENABLE: bool  = self.data["voice-getter"]["random"]["enable"]
        self.VOICE_MIN: int = self.data["voice-getter"]["random"]["min-coins"]
        self.VOICE_MAX: int = self.data["voice-getter"]["random"]["max-coins"]

        # TODO: "Chat getter."
        self.CHAT_DEF_SYMBOLS: int = self.data["chat-getter"]["default"]["symbols"]
        self.CHAT_COINS: int = self.data["chat-getter"]["default"]["coins"]
        self.CHAT_ENABLE: bool  = self.data["chat-getter"]["count"]["enable"]
        self.CHAT_CON_SYMBOLS: int = self.data["chat-getter"]["count"]["symbols"]
        self.CHAT_STABILIZER: int = self.data["chat-getter"]["count"]["stabilizer"]
        self.CHAT_MULTIPLIER: int = self.data["chat-getter"]["count"]["multiplier"]
        self.CHAT_BLACK_WORDS: list[str] = self.data["chat-getter"]["black_words"]

        # TODO: "Time formatted."
        self.TIME_FORM_DAYS = self.data["time-formatted"]["days"]
        self.TIME_FORM_HOURS = self.data["time-formatted"]["hours"]
        self.TIME_FORM_MINUTES = self.data["time-formatted"]["minutes"]
        self.TIME_FORM_SECONDS = self.data["time-formatted"]["seconds"]

        # # TODO: "Transactions menu."
        # self.TRANSFER_ARROW: int = self.data["transfer-menu"]["arrow"]
        # self.TRANSFER_COLOR: str = self.data["transfer-menu"]["color"]
        # self.TRANSFER_FORMATTED: str = self.data["transfer-menu"]["formatted"]
        # self.TRANSFER_NEXT: str = self.data["transfer-menu"]["button-next"]
        # self.TRANSFER_EXIT: str = self.data["transfer-menu"]["button-exit"]

        # TODO: "Pay menu."
        self.PAY_COLOR: str = self.data["pay-menu"]["color"]
        self.PAY_TIME: int = self.data["pay-menu"]["time"]
        self.PAY_TITLE: str = self.data["pay-menu"]["title"]
        self.PAY_USER: str = self.data["pay-menu"]["user"]
        self.PAY_TARGET: str = self.data["pay-menu"]["target"]
        self.PAY_ICON: bool = self.data["pay-menu"]["icon-avatar"]
        self.PAY_DEFAULT: str = self.data["pay-menu"]["default-avatar"]
        self.PAY_CONFIRM_LABLE: str = self.data["pay-menu"]["button-confirm"]["lable"]
        self.PAY_CONFIRM_STYLE: str = self.data["pay-menu"]["button-confirm"]["style"]
        self.PAY_CENTER_ENABLE: bool = self.data["pay-menu"]["button-center"]["enable"]
        self.PAY_CENTER_LABLE: str = self.data["pay-menu"]["button-center"]["lable"]
        self.PAY_CANCEL_LABLE: str = self.data["pay-menu"]["button-cancel"]["lable"]
        self.PAY_CANCEL_STYLE: str = self.data["pay-menu"]["button-cancel"]["style"]

        # TODO: "Messages text."
        self.MSG_BALANCE_ME: str = self.data["messages"]["balance-me"]
        self.MSG_BALANCE_TARGET: str = self.data["messages"]["balance-target"]
        self.MSG_TIMELY_ME: str = self.data["messages"]["timely-me"]
        self.MSG_TIMELY_COOLDOWN: str = self.data["messages"]["timely-cooldown"]
        self.MSG_PAY_ME: str = self.data["messages"]["pay-me"]
        self.MSG_PAY_TARGET: str = self.data["messages"]["pay-target"]
        self.MSG_PAY_CANCEL: str = self.data["messages"]["pay-cancel"]
        self.MSG_PAY_SESSION: str = self.data["messages"]["pay-session"]
        self.MSG_PAY_NO: str = self.data["messages"]["pay-no"]
        self.MSG_GIVE_ME: str = self.data["messages"]["give-me"]
        self.MSG_GIVE_TARGET: str = self.data["messages"]["give-target"]
        self.MSG_TAKE_ME: str = self.data["messages"]["take-me"]
        self.MSG_TAKE_TARGET: str = self.data["messages"]["take-target"]
        self.MSG_TAKE_NO: str = self.data["messages"]["take-no"]
        self.MSG_RESET_ME: str = self.data["messages"]["reset-me"]
        self.MSG_RESET_TARGET: str = self.data["messages"]["reset-target"]
        self.MSG_RESET_NO: str = self.data["messages"]["reset-no"]
        self.MSG_TARGET_BOT: str = self.data["messages"]["target-bot"]

    def __data(self) -> dict:
        with open(file=self.path_to_file, mode="r", encoding="UTF-8") as file:
            return yaml.safe_load(stream=file)
config = ConfigYML()


class WalletJSON:
    def __init__(self) -> None:
        self.file_name = "./assets/data/user_wallet.json"
        self.wallet = self.__data()

    def check_user_wallet(self, user_id: int) -> bool:
        return self.wallet["WALLET"].get(str(user_id), None)

    def get_balance(self, user_id: int) -> int:
        if self.check_user_wallet(user_id=user_id):
            return self.wallet["WALLET"][str(user_id)]["MONEY"]
        else:
            return 0

    def take_money(self, user_id: int, amount: int) -> int:
        self.wallet["WALLET"][str(user_id)]["MONEY"] -= amount
        self.__save(data=self.wallet)
        return self.get_balance(user_id=user_id)

    def pay_money(self, user_id: int, target_id: int, amount: int, datatime: str) -> None:
        session: str = re.sub(r'\D', '', datatime)
        transactions = {
            session: {
                "user": target_id,
                "amount": amount,
                "datatime": datatime
            }
        }
        wallets = {
            str(target_id): {
                "MONEY": amount,
                "TRANSFER": transactions
            }
        }
        if self.check_user_wallet(user_id=target_id):
            self.wallet["WALLET"][str(user_id)]["MONEY"] -= amount
            self.wallet["WALLET"][str(target_id)]["MONEY"] += amount
            self.wallet["WALLET"][str(user_id)]["TRANSFER"] |= transactions
            self.wallet["WALLET"][str(target_id)]["TRANSFER"] |= transactions
        else:
            self.wallet["WALLET"] |= wallets
            self.wallet["WALLET"][str(user_id)]["MONEY"] -= amount
            self.wallet["WALLET"][str(user_id)]["TRANSFER"] |= transactions
        self.__save(data=self.wallet)

    def give_money(self, user_id: int, amount: int) -> int:
        if self.check_user_wallet(user_id=user_id):
            self.wallet["WALLET"][str(user_id)]["MONEY"] += amount
        else:
            self.wallet["WALLET"] |= {str(user_id): {"MONEY": amount,"TRANSFER": {}}}
        self.__save(data=self.wallet)
        return self.get_balance(user_id=user_id)

    def get_transactions(self, user_id: int) -> list | None:
        if self.check_user_wallet(user_id=user_id):
            return list(self.wallet["WALLET"][str(user_id)]["TRANSFER"].values())
        else:
            return None

    def __save(self, data: dict) -> None:
        with open(file=self.file_name, mode="w", encoding="UTF-8") as file:
            json.dump(data, fp=file, indent=5, sort_keys=False, ensure_ascii=False)

    def __data(self) -> dict:
        with open(file=self.file_name, mode="r", encoding="UTF-8") as file:
            return json.load(fp=file)
wallet = WalletJSON()


class TimelyJSON:
    def __init__(self) -> None:
        self.file_name = "./assets/data/user_timely.json"
        self.timely = self.__data()

    def check_cooldown(self, user_id: int) -> bool:
        if self.timely["COOLDOWN"].get(str(user_id)):
            return True
        else:
            return False

    def get_cooldown(self, user_id: int) -> str | None:
        if self.timely["COOLDOWN"].get(str(user_id)):
            return self.timely["COOLDOWN"][str(user_id)]
        else:
            return None

    def set_cooldown(self, user_id: int, cooldown: str) -> None:
        if self.timely["COOLDOWN"].get(str(user_id)):
            self.timely["COOLDOWN"][str(user_id)] = cooldown
        else:
            self.timely["COOLDOWN"] |= {str(user_id): cooldown}
        self.__save(data=self.timely)

    def __save(self, data: dict) -> None:
        with open(file=self.file_name, mode="w", encoding="UTF-8") as file:
            json.dump(data, fp=file, indent=5, sort_keys=False, ensure_ascii=False)

    def __data(self) -> dict:
        with open(file=self.file_name, mode="r", encoding="UTF-8") as file:
            return json.load(fp=file)
timely = TimelyJSON()