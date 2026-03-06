from time import sleep
from utils import CustomMouse, CustomKeyboard

mouse = CustomMouse()
keyboard = CustomKeyboard()


def confirm() -> bool:
    """Looks for a confirm button and clicks it. Returns True if found."""
    pt = mouse.findPointByImage(candidates=['pics/confirm.png', 'pics/confirm2.png'])
    if pt is None:
        return False
    mouse.goToPointAndClick(pt[0], pt[1])
    sleep(2)
    return True

def claim() -> bool:
    pt = mouse.findPointByImage(candidates=['pics/claim3.png', 'pics/claim4.png', 'pics/claim.png', 'pics/claim2.png', ], confidence=0.85)
    if pt:
        mouse.goToPointAndClick(pt[0], pt[1])
        sleep(2)
        return True
    return False

def watch_the_loader(max_time: int = 20, min_time: int = 5, pics: list = None):
    """Waits for a loading screen to disappear, then ensures a minimum wait time."""
    if pics is None:
        pics = ['pics/loading.png']

    elapsed = 0
    while elapsed < max_time:
        sleep(2)
        pt = mouse.findPointByImage(candidates=pics)
        if pt is None:
            break
        elapsed += 1

    if elapsed < min_time:
        sleep(min_time - elapsed)