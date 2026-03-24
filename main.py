import ctypes
import sys
import subprocess
import os
from time import sleep
from pynput.keyboard import Key

from utils import tsleep, CustomMouse, CustomKeyboard, load_config
from hoyolab import check_dailies_status
from common import confirm, claim, watch_the_loader
from dailies import coffee, dinivation, store_mgmt

mouse = CustomMouse()
keyboard = CustomKeyboard()
config = load_config()


def collect_rewards():
    print('Collecting daily rewards...')
    # Daily menu
    sleep(2)
    keyboard.softPress(Key.f2)
    sleep(2)
    mouse.goToPointAndClick(1571, 275)
    sleep(2)
    confirm()
    keyboard.softPress(Key.esc)

    # City Pass
    print('Claiming city pass...')
    sleep(2)
    keyboard.softPress(Key.f3)
    sleep(2)
    mouse.goToPointAndClick(1500, 50)
    sleep(2)
    if claim():
        keyboard.softPress(Key.esc)


def login():
    print('Logging in...')
    for attempt in range(10):
        default = (1000, 900) if attempt == 9 else (0, 0)
        pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=default)
        if pt != (0, 0):
            break
        print(f'Attempt {attempt + 1}/10 failed, retrying in 5s...')
        tsleep(5)
    mouse.goToPointAndClick(pt[0], pt[1])
    watch_the_loader(pics=['pics/loading_config.png'], min_time=15, max_time=90)

    if confirm():
        pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=(1000, 900))
        mouse.goToPointAndClick(pt[0], pt[1])
        tsleep(60)

    pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=(1000, 900))
    mouse.goToPointAndClick(pt[0], pt[1])
    tsleep(5)
    pt = mouse.findPointByImage(candidates=['pics/p2p.png', 'pics/p2p_2.png'], default=(1000, 900))
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
    tsleep(10)
    watch_the_loader()


def monthly():
    print('Checking monthly bonus...')
    pt = mouse.findPointByImage(candidates=['pics/monthly.png', 'pics/monthly_2.png'])
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
        sleep(2)


def login_rewards():
    print('Claiming login rewards...')
    if claim():
        confirm()
        keyboard.softPress(Key.esc)


def confirm_login() -> bool:
    for _ in range(5):
        if mouse.findPointByImage(candidates=['pics/login_confirm.png']):
            print('Logged in successfully')
            return True
        sleep(1)
    return False


def launch_app():
    print('Launching game...')

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        subprocess.Popen([config['game_path']], cwd=os.path.dirname(config['game_path']))
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, f'"{__file__}"', None, 1
        )
        sys.exit()


def main():
    print("Checking dailies' status...")
    if check_dailies_status():
        print('Dailies are already complete.')
        return
    print('Dailies not complete — starting tasks.')

    launch_app()
    tsleep(30)
    login()

    login_rewards()
    monthly()

    if not confirm_login():
        print('Login failed — aborting.')
        return

    tsleep(5, desc='Starting in')

    print('Running dailies...')
    print("Coffee - daily task #1")
    coffee()
    print("Dinivation - daily task #2")
    dinivation()
    print("Store management - daily task #3")
    store_mgmt()

    collect_rewards()

    if check_dailies_status():
        print('All dailies complete ✓')

    print('Closing game...')
    tsleep(5, desc='Closing in')
    keyboard.holdKey([Key.alt, Key.f4], hold_time=0.4)

    print('Done.')


if __name__ == '__main__':
    main()
