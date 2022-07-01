import json
import time
import numpy
from win32gui import *
import pyautogui
import cv2
import aircv

def GetAllLocation():
    titles = set()
    def foo(hwnd, nouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            titles.add(GetWindowText(hwnd))
    EnumWindows(foo,0)
    lt = [t for t in titles if t]
    lt.sort()
    for t in lt :
        print(t)

def GetWindowLocation():
    name = '雷电模拟器(64)'
    handle = FindWindow(0, name)
    if handle == 0:
        print('没有这个窗口')
        exit(10010)
    else:
        WindowLocation = GetWindowRect(handle)
        print(f'窗口范围:{WindowLocation}')
        return WindowLocation     

def CheckWindowLocation():
    # 屏幕截图
    time.sleep(2)
    screen = pyautogui.screenshot()
    cv_screen = numpy.array(screen)
    cv_screen = cv2.cvtColor(cv_screen, cv2.COLOR_RGB2BGR)
    cv2.imshow('Screen', cv_screen)
    cv2.waitKey()

def WindowShot(name):
    location = GetWindowLocation()
    width = location[2]-location[0]
    high = location[3]-location[1]
    region = (location[0], location[1], width, high)
    time.sleep(2)
    image = pyautogui.screenshot(region=region)
    image.save(f'static/{name}.png')

def GetButtonLocation(name, search_file_path, isFirst = False):
    # 仅第一次使用(如果没有get_location_window.png)
    if isFirst:
        WindowShot('get_location_window')
    # 读取源文件和待搜索的图片
    img_source = aircv.imread('static/get_location_window.png')
    img_search = aircv.imread(search_file_path)
    # 搜索
    result = aircv.find_template(img_source, img_search)
    # 获取左上角、右下角坐标,可信度
    left_top_location = result['rectangle'][0]
    right_down_location = result['rectangle'][3]
    confidence = f'''{result['confidence']*100}%'''
    print(f'<整理>在窗口里面的坐标\n左上角:{left_top_location}\n右下角:{right_down_location}\n可信度:{confidence}')
    # 写入JSON文件
    writed = result['result']
    with open('static/locations.json', 'r') as temp:
        locations = json.load(temp)
    if name in locations.keys():
        locations[name] = writed
    else:
        locations.update({name:writed})
    data = json.dumps(locations)
    with open('static/locations.json', 'w') as temp:
        temp.write(data)
    # 通过opencv显示出来
    image = cv2.imread('static/get_location_window.png')
    cv2.rectangle(image, left_top_location, right_down_location, (0, 255, 255), 3)
    cv2.imshow(name, image)
    cv2.waitKey()

if __name__ == '__main__':
    paths = {
        'zilvxundi':'static/zilvxundi.png',
        'again':'static/get_location_again.png',
        'overflowzhengli':'static/boat_overflow_zhengli.png',
        'overflowtuiyi':'static/boat_overflow_tuiyi.png',
        'overflowtuiyiqueding1':'static/boat_overflow_queding.png',
        'overflowtuiyiqueding2':'static/boat_overflow_queding.png',
        'overflowtuiyiqueding3':'static/boat_overflow_queding.png',
        'start':'static/get_location_start.png',
        'go':'static/get_location_go.png',
        'exd3':'static/get_location_d3.png'
    }
    name = 'exd3'
    GetButtonLocation(name=name, search_file_path=paths[name], isFirst=True)
