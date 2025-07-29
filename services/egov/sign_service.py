import time

import pyautogui
import subprocess
import keyboard


class SignXml:
    @staticmethod
    def __activate_ncalayer():

        # Перемести окно NCALayer в координаты (100, 100)
        try:
            script = '''
            tell application "System Events"
                tell process "java"
                    set position of front window to {100, 100}
                end tell
            end tell
            '''
            time.sleep(1)
            subprocess.run(["osascript", "-e", script], timeout=30)
            time.sleep(1)
            return True
        except Exception as e:
            print(e)

    def __find_window(self):
        pyautogui.moveTo(683, 444)  # Клик по продолжить
        pyautogui.click()
        self.__activate_ncalayer()
        pyautogui.moveTo(430, 255)  # Клик по полю ввода пароля
        pyautogui.click()
        # pyautogui.write("Volkin9")
        keyboard.write("Volkin9")
        pyautogui.moveTo(430, 309)  # Клик по кнопке Открыть
        pyautogui.click()
        pyautogui.moveTo(430, 565)  # Клик по кнопке Подписать
        time.sleep(3)
        pyautogui.click()

    def sign_xml(self):
        tries = 0
        time.sleep(1)
        while tries < 15:
            window = self.__activate_ncalayer()
            if window is True:
                break
            tries += 1
            time.sleep(1)
        self.__find_window()
        time.sleep(5)

# if __name__ == '__main__':
#     SignXml.sign_xml()
