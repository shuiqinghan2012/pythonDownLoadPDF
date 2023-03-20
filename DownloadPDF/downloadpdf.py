#downloadpdf.py 为主调用函数
from mylog import Mylog,logging
from FileExcel import FileExcel
from webRequest import WebRequest
import os
from pythFile import readFileName,file_name
righnote ='''
Copyright [2022] by [Michael]
1999-2025 All rights reserved.
'''




def runMain(excelPath):
    PN = readFileName('PN', 'excelname.txt')


    BomExcelObj = FileExcel(excelPath)
    listT = BomExcelObj.readExcelToList()
    for i in listT:
        print(i)
    print(listT[0])
    partList = BomExcelObj.getColWord(PN)
    print(partList)
    pdfObj = WebRequest()
    # for part in partList:
    for rowNum in range(len(partList)):
        part = partList[rowNum]
        # print(part,rowNum)
        pdfUrlRow = 1+1+ rowNum  # i为partList的位置,list从0开始计数，Excel从1开始，且第一行为标题，所以Excel和list差2行
        # print(pdfUrlRow)
        pdfUrlCol = BomExcelObj.maxCol + 1
        # print(pdfUrlRow, pdfUrlCol)
        try:
            logging.info("下载{}，所在位置为{}，总数为{}".format(part,rowNum,len(partList)))
            print("下载{}，所在位置为{}，总数为{}".format(part,rowNum,len(partList)))
            pdfUrl,state = pdfObj.runDownLoadPDF(str(part))
        except Exception as err:
            logging.debug(err)

        else:#将PDF url和下载ok/NG标准加入到Excel表中
            if state:
                BomExcelObj.writeExcelCell(pdfUrl,pdfUrlRow,pdfUrlCol)
                BomExcelObj.writeExcelCell("OK", pdfUrlRow, pdfUrlCol+1)
            else:
                BomExcelObj.writeExcelCell(pdfUrl, pdfUrlRow, pdfUrlCol)
                BomExcelObj.writeExcelCell("NG", pdfUrlRow, pdfUrlCol+1)
            # print("pdfUrl执行写入Excel")
    #保存Excel
    BomExcelObj.saveResult(bomFile)




#*********************************路径处理************************************
print(righnote)
# print(os.getcwd())
path = os.getcwd()
# path = input("请输入BOM所在路径:")
# if path =="":
#     path = os.getcwd()
#
# #test空路径ok
# # path = r'D:\adb'
# print(path)


#改变目录
os.chdir(path)
print(os.getcwd())
logging.info('BOM Excel所在路径是:{}'.format(path))

#print('从excelname.txt文件中读取BOM名称')
bomFile = readFileName('BOM','excelname.txt')
print(bomFile)
excelPathList = file_name(path)
for excelPath in excelPathList:
    if(bomFile in excelPath):
        print(excelPath)
        excelpath = excelPath#查找BOM的路径处理

log = Mylog()
log.configLog()

logging.info("开始主程序")
# excelPath = 'd:\Work\Study\Python\DownloadPDF\Test_BOM.xlsx'


runMain(excelPath)