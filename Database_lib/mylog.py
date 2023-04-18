"""实现log处理的封装"""
import os,datetime
import shutil


import logging, sys, traceback

righnote ='''
Copyright [2022] by [Michael]
1999-2025 All rights reserved.
'''

"""测试log管理的类"""
class Mylog():

    def __init__(self):
        datetimeNow = datetime.datetime.now()
        self.datatimeStr = datetimeNow.strftime("%y-%m-%d-%H-%M-%S")

    def logPath(self):
        logPath = r'./log'  # 定义一个变量储存要指定的文件夹目录
        if not os.path.exists(logPath):  # 没有这个文件目录则新建一个
            os.mkdir(logPath)
            print('创建目录{}成功'.format(logPath))
            return True
    def configLog(self):
        # *****************************************
        # 增加调试日志模块
        # logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s\
        # - %(message)s')
        self.logPath()  # 创建目录
        # 将日志写入文本
        logging.basicConfig(filename='./log/{}.txt'.format(self.datatimeStr), filemode='w', level=logging.INFO, format='\
                %(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

        # 禁用日志，禁用优先级低于CRITICAL的日志
        '''日志有五种优先级，优先级从低到高依次为：
        DEBUG
        INFO
        WARNING
        ERROR
        CRITICAL
        警用日志会警用低于指定优先级的日志，如下使用logging.CRITICAL，因所有优先级都低于
        CRITICAL，因此logging.disable(logging.WARNING)会禁用全部日志

        不禁用时只需注释掉如下这行即可
        '''
        # logging.disable(logging.DEBUG)
        logging.info("log 配置ok")
"""
使用方式：
from mylog import Mylog,logging
log = Mylog()
log.configLog()


logging.info("开始主程序")

"""
# # 单模块测试
# log = Mylog()
# log.configLog()
# logging.info("测试log，ok")

