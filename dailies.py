from pynput.mouse import Button
from pynput.keyboard import Key
from random import random
from time import sleep

from utils import CustomMouse, CustomKeyboard, load_config
from common import confirm, watch_the_loader

mouse = CustomMouse()
keyboard = CustomKeyboard()
config = load_config()


def initiate_errand():
    keyboard.press(Key.alt)
    sleep(0.5)
    mouse.slowlyMoveTo(1000, 400, 1)
    keyboard.release(Key.alt)
    keyboard.softPress(Key.f2)
    sleep(2)

    if not mouse.findPointByImage(candidates=['pics/errands2.png'], confidence=0.9):
        errand_pt = mouse.findPointByImage(candidates=['pics/errands1.png', 'pics/errands2.png'], default=(973, 148))
        mouse.goToPointAndClick(errand_pt[0], errand_pt[1], 1)
        sleep(1)
    sleep(0.5)
    mouse.goToPointAndClick(1050, 834)
    sleep(2)
    mouse.goToPointAndClick(1121, 628)  # Teleport


def coffee():
    initiate_errand()
    watch_the_loader(min_time=10)
    keyboard.softPress('w', hold_time=1)
    keyboard.softPress('f')
    sleep(2)
    keyboard.softPress('1')
    sleep(1.5)
    confirm()


def dinivation():
    initiate_errand()
    watch_the_loader(min_time=4)
    keyboard.softPress('f')
    sleep(3)
    mouse.goToPointAndClick(1500, 500)
    sleep(2)

    drag_check = lambda: bool(mouse.findPointByImage(candidates=['pics/confirm.png', 'pics/confirm2.png']))

    # Dragging
    mouse.press(Button.left)
    for _ in range(7):
        for x, y in [(400 + random() * 50, 500 + random() * 50),
                     (900 + random() * 50, 500 - random() * 50)]:
            mouse.slowlyMoveTo(x, y, 0.6)
            if drag_check():
                break
        else:
            continue
        break

    mouse.release(Button.left)
    sleep(1)
    confirm()
    for _ in range(2):
        keyboard.softPress(Key.esc)
        sleep(2)


def store_mgmt():
    initiate_errand()
    watch_the_loader(min_time=4)
    keyboard.softPress('w', hold_time=1)
    keyboard.softPress('f')
    sleep(2)
    keyboard.softPress('1')
    sleep(2)
    if not mouse.findPointByImage(candidates=['pics/store_mgmt.png']):
        sleep(2)
        keyboard.softPress(Key.esc)

    # Select Character
    sleep(2)
    pt = mouse.findPointByImage(candidates=['pics/store_mgmt.png'], default=(900, 750))
    mouse.goToPointAndClick(pt[0], pt[1])

    sleep(2)
    pt = mouse.findPointByImage(candidates=['pics/waifu.png'])
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
    
    confirm()

    # Select movies
    mouse.goToPointAndClick(1200, 750)
    pt = mouse.findPointByImage(candidates=['pics/store_mgmt_movies.png'], default=(1400, 1030))
    mouse.goToPointAndClick(pt[0], pt[1])

    sleep(2)
    mouse.goToPointAndClick(1700, 980)
    sleep(2)
    confirm()
    confirm()


def complete_dailies():
    coffee()
    dinivation()
    store_mgmt()


if __name__ == "__main__":
    sleep(10)
    complete_dailies()
