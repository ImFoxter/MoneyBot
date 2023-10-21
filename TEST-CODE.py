# import cv2
# import pyautogui
# import numpy as np
# import mss
#
# # Ініціалізація захоплення екрану гри
# game_screen = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # Змініть розміри та координати на власні
# sct = mss.mss()
#
# # Ініціалізація алгоритму відстеження голови (може знадобитися навчання моделі)
# head_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#
# while True:
#     # Захоплюємо ігровий екран
#     screenshot = sct.grab(game_screen)
#
#     # Конвертуємо зображення в формат NumPy array
#     frame = np.array(screenshot)
#
#     # Пошук голови в кадрі
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     heads = head_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
#
#     for (x, y, w, h) in heads:
#         # Обчислюємо координати центру голови
#         head_x = x + w // 2
#         head_y = y + h // 2
#
#         # Рисуємо квадрат навколо голови (або інший маркер)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#         # Спрямовуємо курсор мишки до центру голови
#         pyautogui.moveTo(head_x, head_y)
#
#     # Відображаємо оброблений кадр
#     cv2.imshow('Game Capture', frame)
#
#     # Виходьте з циклу, якщо натиснуто 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Звільнення ресурсів та закриття захоплення екрану
# cv2.destroyAllWindows()
import time

tranc = [
    "111",
    "222",
    "333",
    "444",
    "555",
    "666",
    "777",
    "777"
]

page_num = 0


def next_p():
    global page_num
    result = []
    for _ in range(2):
        if page_num < len(tranc):
            result.append(tranc[page_num])
            page_num += 1
        else:
            break
    print(result, page_num)

def back_p():
    global page_num
    result = []
    for _ in range(2):
        if page_num > 0:
            page_num -= 1
            result.insert(0, tranc[page_num - 2])
        else:
            break
    print(result, page_num)


if __name__ == "__main__":
    next_p()
    time.sleep(2)
    next_p()
    time.sleep(2)
    back_p()








# import asyncio
# import openai
#
#
# class NeiroIA:
#     def __init__(self, module: str, role: str, key: str):
#         self.key = key
#         self.module = module
#         self.role = role
#         self.chat = []
#
#     async def request(self, prompt: str):
#         openai.api_key = self.key
#         response  = await self.create_chat_completion(prompt=prompt)
#         message = response.choices[0].message.content
#
#         self.chat.append({"role": self.role, "content": message})
#         # print(self.chat)
#         return message
#
#     async def create_chat_completion(self, prompt: str):
#         if not self.chat:
#             self.chat = [{"role": self.role, "content": prompt}]
#         else:
#             self.chat = [{"role": item["role"], "content": item["content"]} for item in self.chat]
#             self.chat.append({"role": self.role, "content": prompt})
#
#         return openai.ChatCompletion.create(
#             model=self.module,
#             messages=self.chat
#         )
#
#
#
# async def core():
#     chatbot = NeiroIA(
#         module="gpt-3.5-turbo-16k-0613",
#         role="system",
#         key="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"
#     )
#     pass
#
#     while True:
#         user_input = input("Користувач: ")
#         answer = await chatbot.request(user_input)
#         print("ChatGPT", answer)
#
#
# asyncio.run(core())