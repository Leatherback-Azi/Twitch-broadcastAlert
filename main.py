# Python default
import time

# Installed External Libs
import requests

# Custom
from config import *

# About RPi
import drivers
import RPi.GPIO as GPIO


class rpi:
    class exception:
        class SecondStringIsAlreadyInUse(Exception):
            def __init__(self, msg=''):
                self.msg = msg

            def __str__(self):
                return self.msg + '\nFirst String is already using more than 16 characters\n'

        class NotEnoughString(Exception):
            def __init__(self, msg=''):
                self.msg = msg

            def __str__(self):
                return self.msg + '\nString length is too much to print string.\n'

    def __init__(self):
        # Setup GPIO Call method
        if config.PIN_CALL == 'BOARD':
            GPIO.setmode(GPIO.BOARD)
        elif config.PIN_CALL == 'BCM':
            GPIO.setmode(GPIO.BCM)

        # Setup GPIO Pins
        GPIO.setup(config.LED_1_OUT, GPIO.OUT)      # LED Setup.
        GPIO.setup(config.BUZZER_1_OUT, GPIO.OUT)   # Buzzer Setup
        self.BUZZER_1 = GPIO.PWM(config.BUZZER_1_OUT, 1.0)
        self.display = drivers.Lcd()                # LCD Display Setup.

    def __del__(self):
        print('Cleaning Up...')
        self.display.lcd_clear()
        GPIO.cleanup()

    def print_Display(self, firstString='', secondString=''):
        if len(firstString) > 16:
            string = firstString
            firstString_Extend = string[16:]                        # It will be printed at second string
            firstString = string[:len(firstString_Extend)*-1]       # It will be printed at first string
            self.display.lcd_display_string(firstString.center(16, ' '), 1)             # Print First String
            self.display.lcd_display_string(firstString_Extend.center(16, ' '), 2)      # Print Second String
            if secondString:
                raise self.exception.SecondStringIsAlreadyInUse
        else:
            self.display.lcd_display_string(firstString.center(16, ' '), 1)
            if secondString:
                self.display.lcd_display_string(secondString.center(16, ' '), 2)

    def cleanup_Display(self):
        self.display.lcd_display_string('', 1)
        self.display.lcd_display_string('', 2)

    def clearAll(self):
        self.cleanup_Display()
        self.LOW_BUZZER_1()
        self.LOW_LED_1()

    def HIGH_LED_1(self):
        GPIO.output(config.LED_1_OUT, True)

    def LOW_LED_1(self):
        GPIO.output(config.LED_1_OUT, False)

    def HIGH_BUZZER_1(self, freq=523, playtime=1.0):
        self.BUZZER_1.start(100)
        self.BUZZER_1.ChangeFrequency(freq)
        time.sleep(playtime)

    def LOW_BUZZER_1(self):
        # GPIO.output(config.BUZZER_1_OUT, False)
        self.BUZZER_1.stop()



class twitchAPI:
    def __init__(self):
        # API INFO
        if config.DEBUG:
            self.URL = config.DEBUG_URL
        else:
            self.URL = config.URL
        self.HEADERS = config.HEADERS
        self.NAME = config.NAME_1
        # Streamer INFO
        self.ID = ''
        # Stream INFO
        self.isItLive = False
        self.Title = ''
        self.Game = ''
        # Action
        self.twitchServerConnErr = self.getChannelInfo()
        self.connErr = self.getStreamINFO()

    def getChannelInfo(self):
        try:
            url = 'https://api.twitch.tv/kraken/users?login=' + self.NAME
            response = requests.get(url, headers=self.HEADERS)
            response = response.json()
            self.ID = response['users'][0]['_id']
            return 0
        except requests.exceptions.ConnectionError:
            print('Connection Error! (Debug == ' + str(config.DEBUG) + ')')
            return 1
        except Exception as E:
            print(str(E))
            return 0

    def getStreamINFO(self):
        try:
            url = self.URL + 'streams/' + self.ID
            response = requests.get(url, headers=self.HEADERS)
            response = response.json()
            if response['stream']:
                self.isItLive = True
                # self.Title = response['stream']['channel']['status']
                self.Game = response['stream']['channel']['game']
                print(self.Game)
                return 0
            else:
                self.isItLive = False
                print('OffLine')
                return 0
        except requests.exceptions.ConnectionError:
            print('Connection Error! (Debug == ' + str(config.DEBUG) + ')')
            return 1
        except Exception as E:
            self.isItLive = False
            print(str(E))
            return 1


class broadcastAlarm:
    def __init__(self):
        self.RPi = rpi()
        self.RPi.print_Display(firstString='Welcome!', secondString='Starting...')
        self.RPi.HIGH_LED_1()
        self.RPi.HIGH_BUZZER_1()
        time.sleep(0.1)
        self.RPi.LOW_LED_1()
        self.RPi.LOW_BUZZER_1()
        self.RPi.clearAll()
        self.isItOnBroadCast = False

    def getBroadcast(self):
        while True:
            self.broadCastStatus = twitchAPI()
            if self.broadCastStatus.connErr or self.broadCastStatus.twitchServerConnErr:
                print('Errno')
                self.RPi.print_Display(firstString='** WARNING! **', secondString='CHECK ETHERNET')
                time.sleep(1)
                break
            self.broadCastStatus.connErr = False
            break

    def isNotOnStream(self):            # 방송중이지 않을 때 실행하는 메서드
        self.RPi.print_Display(firstString=config.NAME_1 + ' is', secondString='* OFFLINE *')
        self.RPi.LOW_LED_1()
        time.sleep(config.REFRESH_RATE)

    def isOnStream(self, cnt=0):        # 방송중일 때 실행되는 메서드
        self.RPi.HIGH_LED_1()
        if not cnt % 2:
            self.RPi.print_Display(firstString=config.NAME_1 + ' is', secondString='* ON STREAM *')
        else:
            self.RPi.print_Display(firstString=self.broadCastStatus.Game)
        if cnt == 0:
            self.playBuzzer_1(config.BUZZER_SCALE_1, config.BUZZER_PLAYTIME_1, config.BUZZER_SLEEPTIME_1)  # Play buzzer
        time.sleep(config.REFRESH_RATE)

    def playBuzzer_1(self, SCALE, PLAYTIME, SLEEPTIME):
        for i in range(len(config.BUZZER_SCALE_1)):
            self.RPi.HIGH_BUZZER_1(freq=SCALE[i], playtime=PLAYTIME[i])
            self.RPi.LOW_BUZZER_1()
            time.sleep(SLEEPTIME[i])


if __name__ == '__main__':
    try:
        app = broadcastAlarm()
        count = 0
        while True:
            app.getBroadcast()
            if app.broadCastStatus.isItLive:
                app.isItOnBroadCast = True
                app.isOnStream(count)
                count += 1
            elif app.broadCastStatus.connErr or app.broadCastStatus.twitchServerConnErr:
                pass
            else:
                if app.isItOnBroadCast:
                    app.RPi.HIGH_BUZZER_1(playtime=0.5)
                    app.RPi.LOW_BUZZER_1()
                count = 0
                app.isItOnBroadCast = False
                app.isNotOnStream()
    except KeyboardInterrupt:
        pass
