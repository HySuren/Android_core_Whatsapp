from core.activity_scanner import ActivityScanner
import uiautomator2 as u2
import time


while True:
    d = u2.connect()
    d.reset_uiautomator()
    a = ActivityScanner(d)

    print(a.scan())
    time.sleep(2)