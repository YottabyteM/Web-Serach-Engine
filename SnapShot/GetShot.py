from selenium import webdriver
import time
import os.path

input_file = "./Info.json"


def webshot(url, saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    pic_name = saveImgName
    link = url
    try:
        driver.get(link)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(pic_name + ".png")

        print("Process {} get one pic !!!".format(os.getpid()))
        time.sleep(0.1)
    except Exception as e:
        print(pic_name, e)


if __name__ == '__main__':
    t = time.time()
    # 两个参数，前面url，后面保存地址
    f = open(input_file, 'r', encoding='UTF-8')
    URLS = []
    NAME = []
    for line in f.readlines():
        line = eval(line.strip().strip(','))
        URLS.append(line["PostURL"])
        NAME.append(line["RecruitPostName"])
    for i in range(0, len(URLS)):
        webshot(URLS[i], './data/'+str(NAME[i]))
