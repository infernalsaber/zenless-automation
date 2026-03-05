import ipdb
import ctypes
import sys
import subprocess
import os
from time import sleep
from pynput.keyboard import Key

from utils import tsleep, CustomMouse, CustomKeyboard, load_config
from hoyolab import check_dailies_status
from common import confirm, watch_the_loader
from dailies import complete_dailies

mouse = CustomMouse()
keyboard = CustomKeyboard()
config = load_config()


def collect_rewards():
    # Daily menu
    sleep(2)
    keyboard.softPress(Key.f2)
    sleep(2)
    mouse.goToPointAndClick(1571, 275)
    sleep(2)
    confirm()
    keyboard.softPress(Key.esc)

    # City Pass
    sleep(2)
    keyboard.softPress(Key.f3)
    sleep(2)
    mouse.goToPointAndClick(1500, 50)
    sleep(2)
    pt = mouse.findPointByImage(candidates=['pics/claim_all.png'])
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
        sleep(2)
        keyboard.softPress(Key.esc)


def login():
    pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=(1000, 900))
    mouse.goToPointAndClick(pt[0], pt[1])
    watch_the_loader(pics=['pics/loading_config.png'], min_time=15, max_time=90)

    if confirm():
        pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=(1000, 900))
        mouse.goToPointAndClick(pt[0], pt[1])
        tsleep(60)

    pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=(1000, 900))
    mouse.goToPointAndClick(pt[0], pt[1])
    tsleep(15)
    watch_the_loader()


def monthly():
    pt = mouse.findPointByImage(candidates=['pics/monthly.png', 'pics/monthly_2.png'])
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
        sleep(2)


def login_rewards():
    pt = mouse.findPointByImage(candidates=['pics/claim.png', 'pics/claim2.png'])
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
        sleep(2)
        confirm()
        sleep(2)

def confirm_login() -> bool:
    for _ in range(5):
        if mouse.findPointByImage(candidates=['pics/login_confirm.png']):
            print("Logged in")
            return True
        sleep(1)
    return False


def launch_app():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        subprocess.Popen([config['game_path']], cwd=os.path.dirname(config['game_path']))
    else:
        # Re-launch this script with admin rights (triggers UAC once)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{__file__}"', None, 1
        )


def main():
    if check_dailies_status():
        print("Dailies are complete")
        return
    else:
        print("Dailies are not complete, starting tasks")

    launch_app()
    tsleep(30)
    login()
    login_rewards()
    monthly()
    if not confirm_login():
        print("Login failed")
        return

    tsleep(5, desc="Starting in")

    complete_dailies()
    collect_rewards()

    if check_dailies_status():
        print("Dailies are complete")

    tsleep(5, desc="Closing in")
    keyboard.holdKey([Key.alt, Key.f4], hold_time=0.4)


if __name__ == "__main__":
    main()
