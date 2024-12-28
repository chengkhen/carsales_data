import requests
from lxml import html
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

chrome_driver = 'E:/chromedriver/chromedriver-win64/chromedriver.exe'
# 设置Chrome的选项
options = Options()
options.add_argument("headless")  # 无头模式

# 使用Service指定驱动路径，并通过options来配置浏览器设置
service = Service(executable_path=chrome_driver)
# 初始化浏览器
browser = webdriver.Chrome(service=service, options=options)


def china_car_sales():

    # 创立中国汽车总体销量列表
    china_car_sales_list = []
    # 获取中国汽车每月销售量（2018.11-2024.11）
    for i in range(3):
        browser.get("https://xl.16888.com/month-201811-202411-{}.html".format(i + 1))

        wait = WebDriverWait(browser, 4)

        page = html.fromstring(browser.page_source)

        for each in page.xpath("//tr"):

            # 对于中国汽车每月销售量需要获取的信息为：时间time、销量sales、同比month_over_month
            # python 把list里的方括号去掉 http://t.csdn.cn/Du8nV
            # python去除list中的空 https://www.csdn.net/tags/NtjaUg3sOTIzNy1ibG9n.html
            # 详解 Python 中的 filter() 函数 http://t.csdn.cn/TzS28
            # python删除list中的空list https://www.shuzhiduo.com/topic/python-list-%E5%88%A0%E9%99%A4%E7%A9%BAlist/

            time = each.xpath(".//td[@class='xl-td-t4'][1]/text()")

            sales = each.xpath(".//td[@class='xl-td-t4'][2]/text()")

            year_on_year = each.xpath(".//td[@class='xl-td-t4'][3]/text()")

            china_car_sales_list.append(list((time, sales, year_on_year)))


    browser.close()
    to_save = pd.DataFrame(china_car_sales_list,
                           columns=["time", "Sales", "Year_on_year"])
    to_save.to_csv('E:/carsales/data/china_car_sales_list.csv')

def car_sale_per_factory():
    # 创立中国汽车分厂商每月销售表
    car_sale_per_factory_list = []
    # 获取中国汽车分厂商每月销售量（2018.11-2024.11）
    # 载入月份数据
    data = pd.read_csv('E:/carsales/data/month.csv')
    year_month_list = data["month"]

    for i in range(0, 93):
        year_month = year_month_list.loc[i]
        for i in range(3):

            str = 'https://xl.16888.com/factory-%d-%d-{}.html' % (year_month, year_month)
            browser.get(str.format(i + 1))

            page = html.fromstring(browser.page_source)
            for each in page.xpath("//tr"):
                rank = each.xpath(".//td[@class='xl-td-t1']/text()")
                brand = each.xpath(".//td[@class='xl-td-t2']/a/text()")
                sales = each.xpath(".//td[@class='xl-td-t3'][1]/text()")
                Share_in_sales = each.xpath(".//td[@class='xl-td-t3'][2]/text()")
                car_sale_per_factory_list.append(list((rank, brand, sales, Share_in_sales, year_month)))
    browser.close()
    to_save = pd.DataFrame(car_sale_per_factory_list,
                           columns=["Rank", "Brand", "Sales", "Share_in_sales", "Year_Month"])
    to_save.to_csv('E:/carsales/data/car_sale_per_factory_list.csv', index=False)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    china_car_sales()
    #car_sale_per_factory()

