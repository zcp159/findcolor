from ctypes import *
import pyautogui
import time


def get_color(x, y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)  # 获取颜色值
    pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    return [r, g, b]


# finda,findb：表示需要找色的坐标
# findcolorr,findcolorg,findcolorb：表示需要找的颜色RGB
# movexy：最后移动的坐标, 格式["±x","±y"], 默认为找到的坐标，例如["100","100"]表示固定点击坐标100,100，而"+10,-10"表示偏移点击找到的finda+10,findb-10位置
# dianji表示找到颜色后是否点击，默认不点击
# dengxiaoshi表示是否等finda,findb点的颜色改变才进行下去,启用后返回值将有miss键名, 值为true时表示成功消失, 值为false表示未消失
# xiaoshichaoshi表示等待消失的超时时间, 单位毫秒, 注意必须填写负数
def colorcaozuo(finda, findb, findcolorr, findcolorg, findcolorb, movexy=[], dianji="zuo1",
                dengxiaoshi=False, xiaoshichaoshi=2):
    movea = -753159852
    moveb = 945685632
    # 如果为空，则按默认值，找哪移动到哪
    if len(movexy) == 0:
        movea = finda
        moveb = findb
    # 如果为偏移移动，则以finda,findb为原点movea,moveb为相对距离进行偏移移动
    elif len(movexy) == 2:
        if "-" in movexy[0] + movexy[1] or "+" in movexy[0] + movexy[1]:
            movea = finda + int(movexy[0])
            moveb = findb + int(movexy[1])
        # 如果为固定移动，则传来什么坐标就移动到哪
        elif isinstance(int(movexy[0]), int) and isinstance(int(movexy[1]), int):
            movea = int(movexy[0])
            moveb = int(movexy[1])

    # 查看对应点颜色
    return_color = get_color(finda, findb)
    # 判断对应点颜色RBG是否符合传过来的RGB
    if return_color[0] == findcolorr and return_color[1] == findcolorg and return_color[2] == findcolorb:
        print("颜色符合")
        # 如果movea,和moveb设置过移动位置，则移动，否则不动
        if movea != -753159852 and moveb != 945685632:
            # 移动鼠标到位置
            pyautogui.moveTo(movea, moveb, duration=0.1)
            print("鼠标移动到{},{}".format(movea, moveb))

        # 判断是否需要点击
        if dianji == "zuo1":
            print("左击")
            pyautogui.click()
            time.sleep(0.1)
        elif dianji == "zuo2":
            print("双击")
            pyautogui.doubleClick()
            time.sleep(0.1)
        elif dianji == "you1":
            print("右击")
            pyautogui.click(button='right')
            time.sleep(0.1)
        else:
            print("无需点击")

    # 记录现在时间
    timegap = time.perf_counter()
    # 如果需要等待颜色消失
    if dengxiaoshi:
        # 重新找色
        return_color = get_color(finda, findb)
        # 当颜色跟以前的一样且未超时，则无限循环
        while return_color[0] == findcolorr and return_color[1] == findcolorg and return_color[
            2] == findcolorb and time.perf_counter() - timegap < xiaoshichaoshi:
            print("等待中")
            time.sleep(0.1)
            return_color = get_color(finda, findb)
    else:
        print("颜色不符")


if __name__ == '__main__':
    colorcaozuo(2387, 86, 76, 127, 178, movexy=[], dianji="zuo2", dengxiaoshi=True, xiaoshichaoshi=5)
    print("完成")
