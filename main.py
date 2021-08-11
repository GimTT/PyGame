import pygame
import random
import os
import threading
import time
import inspect
import ctypes


class Block:
    def __init__(self):
        self.IMG = pygame.image.load('IMGs/IMG-0.jpg')
        self.Num = 0
        self.bomFlag = 0
        self.BomBom = False
        self.Click = 0
        self.open = False
        self.flagNum = 0


exitFlag = 0


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name, self.counter, 99)
        print("退出线程：" + self.name)


def print_time(thread_name, delay, counter):
    global Time
    while counter:
        if exitFlag:
            thread_name.exit()
        time.sleep(delay)
        Time = Time + 1
        print(Time)
        counter -= 1

def _async_raise(tid, exctype):

    """raises the exception, performs cleanup if needed"""

    tid = ctypes.c_long(tid)

    if not inspect.isclass(exctype):

        exctype = type(exctype)

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

    if res == 0:

        raise ValueError("invalid thread id")

    elif res != 1:

        # """if it returns a number greater than one, you're in trouble,

        # and you should call it again with exc=NULL to revert the effect"""

        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):

    _async_raise(thread.ident, SystemExit)


# 创建新线程
Timer = MyThread(1, "Timer", 1)

# 导入图片
imgLost = pygame.image.load('IMGs/lost.png')
imgWin = pygame.image.load('IMGs/win.png')
img0 = pygame.image.load('IMGs/IMG-0.jpg')
img1 = pygame.image.load('IMGs/IMG-1.jpg')
img2 = pygame.image.load('IMGs/IMG-2.jpg')
img3 = pygame.image.load('IMGs/IMG-3.jpg')
img4 = pygame.image.load('IMGs/IMG-4.jpg')
img5 = pygame.image.load('IMGs/IMG-5.jpg')
img6 = pygame.image.load('IMGs/IMG-6.jpg')
img7 = pygame.image.load('IMGs/IMG-7.jpg')
img8 = pygame.image.load('IMGs/IMG-8.jpg')
imgLei = pygame.image.load('IMGs/IMG-LEI.jpg')
imgNull = pygame.image.load('IMGs/IMG-NULL.jpg')
imgFlag = pygame.image.load('IMGs/IMG-FLAG.jpg')
imgWen = pygame.image.load('IMGs/IMG-？.jpg')
imgOFF = pygame.image.load('IMGs/IMG-OFF.jpg')
imgDict = {0: imgNull, 1: img1, 2: img2, 3: img3, 4: img4, 5: img5, 6: img6, 7: img7, 8: img8, 'Lei': imgLei,
           'Null': imgNull,
           'Flag': imgFlag, 'Wen': imgWen, 'OFF': imgOFF, 'Win': imgWin, 'Lost': imgLost}

Time = 0
b = Block()
n = 13
m = 30
wordList = [[b for i in range(m)] for j in range(n)]
bom8List = []

flag8num = 0
bom8Num = 0
_8Num = 0

pygame.init()  # 初始化pygame包
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (200, 200)  # 设置窗口初始位置
pygame.display.set_caption("扫雷试做版本")  # 设置窗口标题
screen = pygame.display.set_mode((1500, 700))  # 设置窗口大小


def get_xy(i, j):
    x = j * 50
    y = i * 50 + 50
    return x, y


def get_i(y):
    i = int((y - 50) / 50)
    return i


def get_j(x):
    j = int(x / 50)
    return j


# 周围一圈有雷， 则显示数字为雷数 返回1，若没有，则显示空白 返回0
def rec(list_i, list_j):
    global bom8Num, bom8List, imgDict, _8Num
    _8Num = 0
    bom8Num = 0
    bom8List = []
    if wordList[list_i][list_j].bomFlag == 0:
        if list_i == 0 and list_j == 0:
            bom8List = [wordList[list_i + 1][list_j], wordList[list_i + 1][list_j + 1], wordList[list_i][list_j + 1]]

        elif list_i == 0 and (0 < list_j < 29):
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i][list_j + 1], wordList[list_i + 1][list_j - 1],
                        wordList[list_i + 1][list_j], wordList[list_i + 1][list_j + 1]]

        elif list_i == 0 and list_j == 29:
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i + 1][list_j - 1], wordList[list_i + 1][list_j]]

        elif list_i == 12 and list_j == 0:
            bom8List = [wordList[list_i - 1][list_j], wordList[list_i - 1][list_j + 1], wordList[list_i][list_j + 1]]

        elif list_i == 12 and (0 < list_j < 29):
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i][list_j + 1], wordList[list_i - 1][list_j - 1],
                        wordList[list_i - 1][list_j], wordList[list_i - 1][list_j + 1]]

        elif list_i == 12 and list_j == 29:
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i - 1][list_j - 1], wordList[list_i - 1][list_j]]

        elif list_j == 0 and (0 < list_i < 12):
            bom8List = [wordList[list_i - 1][list_j], wordList[list_i - 1][list_j + 1], wordList[list_i][list_j + 1],
                        wordList[list_i + 1][list_j], wordList[list_i + 1][list_j + 1]]

        elif list_j == 29 and (0 < list_i < 12):
            bom8List = [wordList[list_i - 1][list_j], wordList[list_i - 1][list_j - 1], wordList[list_i][list_j - 1],
                        wordList[list_i + 1][list_j], wordList[list_i + 1][list_j - 1]]

        else:
            bom8List = [wordList[list_i - 1][list_j - 1], wordList[list_i - 1][list_j],
                        wordList[list_i - 1][list_j + 1],
                        wordList[list_i][list_j - 1], wordList[list_i][list_j + 1],
                        wordList[list_i + 1][list_j - 1], wordList[list_i + 1][list_j],
                        wordList[list_i + 1][list_j + 1]]

        for i in bom8List:  # 统计周围的雷数
            bom8Num = bom8Num + i.bomFlag
            _8Num = _8Num + i.Num

        print(bom8Num)
        if bom8Num != 0:
            wordList[list_i][list_j].IMG = imgDict[int(bom8Num)]  # 若周围不是空白
            wordList[list_i][list_j].Num = bom8Num
            wordList[list_i][list_j].open = True
            return bom8Num

        elif bom8Num == 0:
            wordList[list_i][list_j].IMG = imgDict['Null']
            wordList[list_i][list_j].Num = bom8Num
            wordList[list_i][list_j].open = True
            for i in range(list_i - 1, list_i + 2):
                for j in range(list_j - 1, list_j + 2):
                    if 0 <= i <= 12 and 0 <= j <= 29 and wordList[i][j].open == False and wordList[i][j].flagNum == 0:
                        rec(i, j)


def go_bom(list_i, list_j):
    global bom8Num, bom8List, imgDict, flag8num
    bom8Num = 0
    bom8List = []
    flag8num = 0
    if wordList[list_i][list_j].bomFlag == 0:
        if list_i == 0 and list_j == 0:
            bom8List = [wordList[list_i + 1][list_j], wordList[list_i + 1][list_j + 1], wordList[list_i][list_j + 1]]

        elif list_i == 0 and (0 < list_j < 29):
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i][list_j + 1], wordList[list_i + 1][list_j - 1],
                        wordList[list_i + 1][list_j], wordList[list_i + 1][list_j + 1]]

        elif list_i == 0 and list_j == 29:
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i + 1][list_j - 1], wordList[list_i + 1][list_j]]

        elif list_i == 12 and list_j == 0:
            bom8List = [wordList[list_i - 1][list_j], wordList[list_i - 1][list_j + 1], wordList[list_i][list_j + 1]]

        elif list_i == 12 and (0 < list_j < 29):
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i][list_j + 1], wordList[list_i - 1][list_j - 1],
                        wordList[list_i - 1][list_j], wordList[list_i - 1][list_j + 1]]

        elif list_i == 12 and list_j == 29:
            bom8List = [wordList[list_i][list_j - 1], wordList[list_i - 1][list_j - 1], wordList[list_i - 1][list_j]]

        elif list_j == 0 and (0 < list_i < 12):
            bom8List = [wordList[list_i - 1][list_j], wordList[list_i - 1][list_j + 1], wordList[list_i][list_j + 1],
                        wordList[list_i + 1][list_j], wordList[list_i + 1][list_j + 1]]

        elif list_j == 29 and (0 < list_i < 12):
            bom8List = [wordList[list_i - 1][list_j], wordList[list_i - 1][list_j - 1], wordList[list_i][list_j - 1],
                        wordList[list_i + 1][list_j], wordList[list_i + 1][list_j - 1]]

        else:
            bom8List = [wordList[list_i - 1][list_j - 1], wordList[list_i - 1][list_j],
                        wordList[list_i - 1][list_j + 1],
                        wordList[list_i][list_j - 1], wordList[list_i][list_j + 1],
                        wordList[list_i + 1][list_j - 1], wordList[list_i + 1][list_j],
                        wordList[list_i + 1][list_j + 1]]

        for i in bom8List:  # 统计周围的雷数
            bom8Num = bom8Num + i.bomFlag

        for j in bom8List:  # 统计周围旗数
            if j.flagNum == 1:
                flag8num = flag8num + j.flagNum

        print(bom8Num)
        print(flag8num)

        if bom8Num == flag8num:

            wordList[list_i][list_j].IMG = imgDict[int(bom8Num)]
            wordList[list_i][list_j].Num = bom8Num
            wordList[list_i][list_j].open = True
            for c in bom8List:
                if c.bomFlag == 1 and c.flagNum == 0:
                    c.IMG = imgDict['Lei']
                    c.BomBom = True
                    c.open = True
                    print('踩雷')
                for i in range(list_i - 1, list_i + 2):
                    for j in range(list_j - 1, list_j + 2):
                        if 0 <= i <= 12 and 0 <= j <= 29 and wordList[i][j].open == False:
                            rec(i, j)


def show_win_lost(lost_flag, win_flag):
    if not lost_flag:
        screen.blit(imgDict['Lost'], (350, 270))

    elif not win_flag:
        screen.blit(imgDict['Win'], (350, 270))

def main():
    global Time
    global exitFlag
    global m, n, wordList
    temp_list = [0 for _ in range(390)]
    initFlag = True
    Running = True
    First = True
    temp_num = 20
    x = -1

    my_font = pygame.font.SysFont("arial", 24)

    for i in range(temp_num):
        temp_list[i] = 1

    random.shuffle(temp_list)

    for i in range(n):
        for j in range(m):
            wordList[i][j] = Block()
            wordList[i][j].IMG = imgDict['OFF']

    while initFlag:
        for i in range(n):
            for j in range(m):
                x = x + 1
                wordList[i][j].bomFlag = temp_list[x]
        initFlag = False

    bomNUM = temp_num

    FastBomNum = bomNUM
    Lost = False

    for i in range(n):
        for j in range(m):
            print(wordList[i][j].bomFlag, end=' ')
        print('')

    Timer.start()
    lost_flag = True
    win_flag = True

    while Running:

        FastNumber = 0

        data = f"Bom:{bomNUM}"
        score_render = my_font.render(data, True, (0, 0, 0), (254, 254, 254))  # 渲染分数
        screen.blit(score_render, (10, 10))

        data = f"Time:{Time}"
        score_render = my_font.render(data, True, (0, 0, 0), (254, 254, 254))  # 渲染时间
        screen.blit(score_render, (100, 10))

        for i in range(n):
            for j in range(m):
                screen.blit(wordList[i][j].IMG, get_xy(i, j))

                if wordList[i][j].BomBom:
                    Lost = True

                if wordList[i][j].open:
                    FastNumber = FastNumber + 1

        for event in pygame.event.get():  # 遍历所有事件

            if FastNumber + FastBomNum == 30 * 13:
                if win_flag:
                    win_flag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 如果按下r

                        screen.fill((0, 0, 0))

                        Time = 0
                        temp_list = [0 for _ in range(390)]
                        initFlag = True
                        Running = True
                        First = True

                        x = -1

                        for i in range(temp_num):
                            temp_list[i] = 1

                        random.shuffle(temp_list)

                        for i in range(n):
                            for j in range(m):
                                wordList[i][j] = Block()
                                wordList[i][j].IMG = imgDict['OFF']

                        while initFlag:
                            for i in range(n):
                                for j in range(m):
                                    x = x + 1
                                    wordList[i][j].bomFlag = temp_list[x]
                            initFlag = False

                        bomNUM = temp_num

                        FastBomNum = bomNUM
                        Lost = False

                        for i in range(n):
                            for j in range(m):
                                print(wordList[i][j].bomFlag, end=' ')
                            print('')
                        win_flag = True
                elif event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出_name__ == '__main__':
                    exitFlag = 1
                    stop_thread(Timer)
                    Running = False

            elif Lost:
                if lost_flag:
                    lost_flag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 如果按下r

                        screen.fill((0, 0, 0))

                        Time = 0
                        temp_list = [0 for _ in range(390)]
                        initFlag = True
                        Running = True
                        First = True

                        x = -1

                        for i in range(temp_num):
                            temp_list[i] = 1

                        random.shuffle(temp_list)

                        for i in range(n):
                            for j in range(m):
                                wordList[i][j] = Block()
                                wordList[i][j].IMG = imgDict['OFF']

                        while initFlag:
                            for i in range(n):
                                for j in range(m):
                                    x = x + 1
                                    wordList[i][j].bomFlag = temp_list[x]
                            initFlag = False

                        bomNUM = temp_num

                        FastBomNum = bomNUM
                        Lost = False

                        for i in range(n):
                            for j in range(m):
                                print(wordList[i][j].bomFlag, end=' ')
                            print('')
                        lost_flag = True
                elif event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出_name__ == '__main__':
                    exitFlag = 1
                    stop_thread(Timer)
                    Running = False

            elif event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出_name__ == '__main__':
                exitFlag = 1
                stop_thread(Timer)
                Running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 50 < y < 700:
                    if event.button == 1 and wordList[get_i(y)][get_j(x)].flagNum == 0:  # 左击
                        if First:
                            if wordList[get_i(y)][get_j(x)].bomFlag == 1:

                                for i in range(n):
                                    for j in range(m):
                                        if wordList[i][j].bomFlag == 0:
                                            wordList[get_i(y)][get_j(x)], wordList[i][j] = wordList[i][j], \
                                                                                           wordList[get_i(y)][get_j(x)]

                                print('踩雷但转移')
                                rec(get_i(y), get_j(x))

                            else:
                                rec(get_i(y), get_j(x))

                            First = False

                        else:
                            if wordList[get_i(y)][get_j(x)].bomFlag == 1:

                                print('踩雷')
                                wordList[get_i(y)][get_j(x)].IMG = imgDict['Lei']
                                wordList[get_i(y)][get_j(x)].open = True
                                wordList[get_i(y)][get_j(x)].BomBom = True
                                screen.blit(wordList[get_i(y)][get_j(x)].IMG, get_xy(get_i(y), get_j(x)))

                            elif wordList[get_i(y)][get_j(x)].bomFlag == 0:
                                rec(get_i(y), get_j(x))

                    elif event.button == 3 and wordList[get_i(y)][get_j(x)].open == False:  # 右击
                        if wordList[get_i(y)][get_j(x)].flagNum == 0:
                            wordList[get_i(y)][get_j(x)].IMG = imgDict['Flag']
                            wordList[get_i(y)][get_j(x)].flagNum = wordList[get_i(y)][get_j(x)].flagNum + 1
                            bomNUM = bomNUM - 1
                            if wordList[get_i(y)][get_j(x)].Num == 99:
                                wordList[get_i(y)][get_j(x)].Num = -99

                        elif wordList[get_i(y)][get_j(x)].flagNum == 1:
                            wordList[get_i(y)][get_j(x)].IMG = imgDict['Wen']
                            wordList[get_i(y)][get_j(x)].flagNum = wordList[get_i(y)][get_j(x)].flagNum + 1
                            bomNUM = bomNUM + 1
                            if wordList[get_i(y)][get_j(x)].Num == -99:
                                wordList[get_i(y)][get_j(x)].Num = 99

                        elif wordList[get_i(y)][get_j(x)].flagNum == 2:
                            wordList[get_i(y)][get_j(x)].IMG = imgDict['OFF']
                            wordList[get_i(y)][get_j(x)].flagNum = wordList[get_i(y)][get_j(x)].flagNum + 1
                            wordList[get_i(y)][get_j(x)].flagNum = 0

                    elif event.button == 2:
                        go_bom(get_i(y), get_j(x))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 如果按下r

                    screen.fill((0, 0, 0))

                    Time = 0
                    temp_list = [0 for _ in range(390)]
                    initFlag = True
                    Running = True
                    First = True

                    x = -1

                    for i in range(temp_num):
                        temp_list[i] = 1

                    random.shuffle(temp_list)

                    for i in range(n):
                        for j in range(m):
                            wordList[i][j] = Block()
                            wordList[i][j].IMG = imgDict['OFF']

                    while initFlag:
                        for i in range(n):
                            for j in range(m):
                                x = x + 1
                                wordList[i][j].bomFlag = temp_list[x]
                        initFlag = False

                    bomNUM = temp_num

                    FastBomNum = bomNUM
                    Lost = False

                    for i in range(n):
                        for j in range(m):
                            print(wordList[i][j].bomFlag, end=' ')
                        print('')

        show_win_lost(lost_flag, win_flag)
        pygame.display.flip()



if __name__ == '__main__':
    main()
