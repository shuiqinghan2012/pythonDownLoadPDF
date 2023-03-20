import time
import random
import requests
from lxml import etree

from mylog import Mylog,logging
log = Mylog()
log.configLog()
logging.info("开始webRequest")


"""
一个描述web请求的类
输入为url
getHTMLText：返回url文本或者错误时返回false，如有错误，将错误写入到log
getHTMLText：返回url对应的内容或者错误时返回false，如有错误，将错误写入到log
getPDF(name):输入希望保存的pdf文件名，然后下载pdf
getDatasheet5PartUrl():解析得到part选择页面的url：
https://www.datasheet5.com/part/LTM4650IY%23PBF/Analog%20Devices%20Inc
getDatasheet5PDFUrl():解析得到PDF页面的url：
https://www.analog.com/LTM4650/datasheet?ADICID=SYND_WW_P682800_PF-spglobal?hkey=EF798316E3902B6ED9A73243A3159BB0
测试起始URL：
url = 'https://www.datasheet5.com/search/LTM4650IY%23PBF'

runDownloadPDF()：执行整个流程的调用函数
"""

class WebRequest():
    def __init__(self):
        self.url = ''
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]

        self.headers = {}
        self.headers['User-Agent'] = random.choice(user_agent_list)
        # self.headers ={
        #     'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        #     'Cookie':'locale = zh - cn;'
        # }

    def getHTMLContent(self):
        try:
            response = requests.get(self.url, headers= self.headers,timeout=5)
            response.raise_for_status()  # 如果状态不是200，引发HTTPError异常
            logging.info("访问getHTMLContent ok")
            time.sleep(random.randint(1, 5))
            response.close()
            return response.content

        except Exception as err:
            logging.info(err)
            logging.info("getHTMLContent 执行,return false")
            return False
        # else:#try内代码块没有异常则执行
        #     return response

    def getHTMLText(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=5)
            response.raise_for_status()  # 如果状态不是200，引发HTTPError异常
            time.sleep(random.randint(1, 5))
            # 设置编码
            response.encoding = "utf-8"
            logging.info("访问getHTMLText ok")
            response.close()
            return response.text   #or .text获取文本

        except Exception as err:
            logging.info(err)
            logging.info("getHTMLText 执行,return false")
            return False

    def getPDF(self,name):
        resp = self.getHTMLContent()
        # path = r'.\PdfFile'
        # name = path+ "\\"+ name
        if resp:
            with open(r"%s.pdf" % name, "wb") as code:
                code.write(resp)
                time.sleep(random.randint(1,5))  # 防止访问速度过快，可以灵活的调整时间 作者：silencedream https://www.bilibili.com/read/cv10914159/ 出处：bilibili
                logging.info("getPDF 执行ok")
            return True
        else:
            logging.info("getPDF 执行,resp is false")
            return False

    def getUrl(self):
        resp = self.getHTMLText()
        if resp:
            e = etree.HTML(resp)
            url_new = e.xpath('//a[@id="pdp-datasheet_0"]/@href')
            url_title = e.xpath('//*[@id="spnManufacturerPartNumber"]/text()')
            logging.info("getUrl 执行ok")
            return url_new,url_title

        else:
            logging.info("getUrl 执行,resp is false")
            return False,False

    def getDatasheet5PartUrl(self):
        resp = self.getHTMLText()
        if resp:
            e = etree.HTML(resp)
            url_new = e.xpath('//td[@class="td-part"]/a/@href')[0]
            url_new = f'https://www.datasheet5.com{url_new}'
            print(url_new)
            return url_new

        else:
            logging.info("getDatasheet5PartUrl 执行,resp is false")
            return False
    def getDatasheet5PDFUrl(self):
        resp = self.getHTMLText()
        if resp:
            e = etree.HTML(resp)
            url_new = e.xpath('//div[@class="name"]/a/@href')[0]
            # url_new = f'https://www.datasheet5.com{url_new}'
            print(url_new)
            part_name = e.xpath('//tr/td[@class ="plainText"]/text()')[0]
            return url_new,part_name

        else:
            logging.info("getDatasheet5PDFUrl 执行,resp is false")
            return False,False
    def datasheetSearch(self,partPN):
        home = 'https://www.datasheet5.com/'
        self.url = home + "search/"+partPN
        # url = 'https://www.datasheet5.com/search/LTM4650IY%23PBF'
        print(self.url)
        # return url
    def runDownLoadPDF(self,partPN):
        # partPN = 'LTM4650IY%23PBF'
        self.datasheetSearch(partPN)
        logging.info("runDownLoadPDF 开始执行")
        self.url = self.getDatasheet5PartUrl()
        pdfUrl,part = self.getDatasheet5PDFUrl()
        self.url = pdfUrl
        #将pdfurl写入到Excel表中固定位置，该函数最后将pdfUrl返回并从主函数写入
        #判断是否下载成功，并打印输出
        for i in range(2):
            if(self.getPDF(part.strip())):
                print("下载{}PDF成功".format(part))
                return pdfUrl,True
                break
            else:
                print("下载pdfUrl Fail! {}".format(pdfUrl))
                return pdfUrl,False






    # def getResponse(self):
    #     resp = self.requestHTML()
    #     if resp:
    #         if resp.status_code == 200:
    #             print(resp.content)
    #         else:
    #             print(resp)
    #     else:
    #         print('访问HTML不成功')


# url='https://4donline.ihs.com/images/VipMasterIC/IC/BELF/BELF-S-A0014526752/BELF-S-A0014526752-1.pdf?hkey=EF798316E3902B6ED9A73243A3159BB0'
# url = 'HTTPS://www.mouser.cn/datasheet/2/643/ds_bps_p_series-1314646.pdf'  #测试可以访问的pdf 页面
# url = 'HTTPS://www.mouser.cn/ProductDetail/Bel-Power-Solutions/DP1501-9RG?qs=DBKgNs46bfQx2Oy1uA5dyQ%3D%3D'  #PDF前一级页面
# url ='https://www.mouser.cn/ProductDetail/Texas-Instruments/TUSB1002RGER?qs=zEmsApcVOkXKUslZUCtTrg%3D%3D'
# url ="https://2.python-requests.org/en/master/_modules/requests/exceptions/#RequestException"

# url = 'https://www.datasheet5.com/search/TUSB1310ZAY'
# url = 'https://www.datasheet5.com/search/SN75DP130SSRGZR' #ok
# url = 'https://www.datasheet5.com/search/MYSGK4R030ERSR' #NG
url = 'https://www.datasheet5.com/search/LTM4650IY%23PBF'
# headers
# headers = {
#   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
# }


# //a[@id="pdp-datasheet_0"]/@href
#//*[@id="spnManufacturerPartNumber"]/text()



#测试模块
# htmlObj = WebRequest(url)
# resp = htmlObj.getHTMLText()
# print(resp)

# 初始url
# urlObj = WebRequest(url)
# downloadUrl = urlObj.getDatasheet5PartUrl()
# print(downloadUrl)
# # 获取到器件型号url
# downloadObj = WebRequest(downloadUrl)
# # downloadObj.getDatasheet5PDFUrl()
# pdfUrl,part = downloadObj.getDatasheet5PDFUrl()
# print(pdfUrl,part)
#
# pdfObj = WebRequest(pdfUrl)
# pdfObj.getPDF(part)

#测试ok
# pdfObj = WebRequest()
# pdfObj.runDownLoadPDF()


# print(title)

