import pyautogui
import json
import GetLocation
import time
import aircv
import cv2
import numpy

def click(location=(1,1)):
    print(f'点击的坐标是:{location}')
    pyautogui.moveTo(location[0], location[1])
    pyautogui.click()

def logging(location):
        # 获取时间戳
        now_time = time.localtime()
        file_name = f'Spoils_{now_time[0]}_{now_time[1]}_{now_time[2]}_{now_time[3]}_{str(now_time[4]).zfill(2)}_{now_time[5]}.jpg'
        print(file_name)
        # 截图
        width = location[2]-location[0]
        high = location[3]-location[1]
        region = (location[0], location[1], width, high)
        image = pyautogui.screenshot(region=region)
        image.save(f'Log/{file_name}')

class AutoFight:
    def __init__(self, times=1):
        self.GetAgainButtonLocation()
        self.ReadButtonSource()
        time.sleep(1)
        self.times = times
        self.Run()

    def GetAgainButtonLocation(self):
        # 获取窗口位置
        self.window_location = GetLocation.GetWindowLocation()
        # 获取位置
        with open('static/locations.json', 'r') as data:
            locations = json.load(data)
        self.again_location = (self.window_location[0]+locations['again'][0], self.window_location[1]+locations['again'][1])
        self.zhengli_location = (self.window_location[0]+locations['overflowzhengli'][0], self.window_location[1]+locations['overflowzhengli'][1])
        self.tuiyi_location = (self.window_location[0]+locations['overflowtuiyi'][0], self.window_location[1]+locations['overflowtuiyi'][1])
        self.queding1_location = (self.window_location[0]+locations['overflowtuiyiqueding1'][0], self.window_location[1]+locations['overflowtuiyiqueding1'][1])
        self.queding2_location = (self.window_location[0]+locations['overflowtuiyiqueding2'][0], self.window_location[1]+locations['overflowtuiyiqueding2'][1])
        self.queding3_location = (self.window_location[0]+locations['overflowtuiyiqueding3'][0], self.window_location[1]+locations['overflowtuiyiqueding3'][1])
        self.zilvxundi_location = (self.window_location[0]+locations['zilvxundi'][0], self.window_location[1]+locations['zilvxundi'][1])
        self.start_location = (self.window_location[0]+locations['start'][0], self.window_location[1]+locations['start'][1])
        self.go_location = (self.window_location[0]+locations['go'][0], self.window_location[1]+locations['go'][1])
        self.exd3_location = (self.window_location[0]+locations['exd3'][0], self.window_location[1]+locations['exd3'][1])

    def ReadButtonSource(self):
        self.AgainButtonSource = aircv.imread('static/get_location_again.png')
        self.ZhenliButtonSource = aircv.imread('static/boat_overflow_zhengli.png')
        self.StartButtonSource = aircv.imread('static/get_location_start.png')
        self.EXD3ButtonSource = aircv.imread('static/get_location_d3.png')
        # 显示是否是否正确读取
        # cv2.imshow('Source', self.StartButtonSource)
        # cv2.waitKey()
    
    def WindowShot(self):
        # 获取待检测地区的长宽
        width = self.window_location[2]-self.window_location[0]
        high = self.window_location[3]-self.window_location[1]
        # 生成截屏数据
        region = (self.window_location[0], self.window_location[1], width, high)
        # 截图
        # time.sleep(1)
        self.window = pyautogui.screenshot(region=region)
        # numpy.array化
        self.window = numpy.array(self.window)
        # 转化为opencv图
        self.window = cv2.cvtColor(self.window, cv2.COLOR_BGR2RGB)
        # 显示图片
        # cv2.imshow('Window', self.window)
        # cv2.waitKey()
    
    def CheckStart(self):
        self.WindowShot()
        result = aircv.find_template(self.window, self.StartButtonSource)
        if not result == None:
            if result['confidence'] >= 0.9:
                click(self.start_location)
                time.sleep(0.5)
                if self.CheckOverflow():
                    click(self.exd3_location)
                    time.sleep(0.5)
                    click(self.start_location)
                click(self.go_location)
        
    def CheckAgain(self):
        self.WindowShot()
        result = aircv.find_template(self.window, self.AgainButtonSource)
        # print(result)
        if not result == None:
            if result['confidence'] >= 0.9:
                return True
    
    def CheckOverflow(self):
        self.WindowShot()
        # 顺序:整理>一键退役>确定1>点击屏幕>确定2>确定3>点击屏幕>返回上一级
        result = aircv.find_template(self.window, self.ZhenliButtonSource)
        if not result == None:
            if result['confidence'] >= 0.9:
                # print(result)
                click(self.zhengli_location)
                time.sleep(1)
                click(self.tuiyi_location)
                time.sleep(1)
                click(self.queding1_location)
                time.sleep(0.5)
                click(self.queding1_location)
                time.sleep(0.5)
                click(self.queding2_location)
                time.sleep(1)
                click(self.queding3_location)
                time.sleep(0.5)
                click(self.queding3_location)
                time.sleep(0.5)
                pyautogui.press('esc')
                time.sleep(2)
                click(self.zilvxundi_location)
                time.sleep(1)
                return True
            else:
                return False
        else:
            return False
            
    def CheckMainOverflow(self):
        self.WindowShot()
        result = aircv.find_template(self.window, self.EXD3ButtonSource)
        if not result == None:
            if result['confidence'] >= 0.9:
                pass
    
    def Run(self):
        # 开启副本
        self.CheckStart()
        # 设定初始次数
        count = 0
        while True:
            # 开始停顿一秒
            time.sleep(1)
            # 检测船上限(<整理>按钮),超出就退役
            self.CheckOverflow()
            # 检测是否有<再次挑战>按钮
            if self.CheckAgain():
                # 有,就次数加一
                count += 1
                print(f'第{count}次运行成功')
                # 检测是否超出次数
                if count >= self.times:
                    print('已经达到次数,准备结束.')
                    break
                time.sleep(10)
                logging(self.window_location)
                click(self.again_location)
                time.sleep(1)
                # 检测船上上限(再次挑战页面)
                if self.CheckOverflow():
                    click(self.exd3_location)
                    time.sleep(1)
                    click(self.start_location)
                    time.sleep(1)
                    click(self.go_location)
            else:
                # 没有就重新循环
                continue


if __name__ == '__main__':
    while True:
        times = int(input('>>请输入自动次数:'))
        program = AutoFight(times)
    # logging([100,200,300,400])
