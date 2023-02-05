import os
import time


def run():
    os.system('start D:\\matlab\\elasticsearch\\elasticsearch\\bin\\elasticsearch.bat')
    time.sleep(20)
    os.system('start D:\\matlab\\kibana\\kibana\\bin\\kibana.bat')


if __name__ == '__main__':
    run()
