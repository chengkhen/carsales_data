import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_driver = 'E:/chromedriver/chromedriver-win64/chromedriver.exe'
# 设置 Chrome 配置
options = Options()
options.headless = False  # 可设置为 True 以使浏览器在后台运行
# 使用Service指定驱动路径，并通过options来配置浏览器设置
service = Service(executable_path=chrome_driver)
# 启动浏览器
driver = browser = webdriver.Chrome(service=service, options=options)

# 打开汽车销量网站
driver.get("https://auto.16888.com/")  # 这里替换为实际的汽车销量网站 URL

# 假设 `txt` 文件的路径为 "cars.txt"
txt_file = "E:/carsales/data/car_model.txt"
output_csv = "E:/carsales/data/car_url.csv"

# 读取txt文件中的车型名
with open(txt_file, 'r', encoding='utf-8') as f:
    car_models = f.readlines()

# 打开 CSV 文件以保存结果
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['车型名', '网址']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历所有车型名并进行搜索
    for car_model in car_models:
        car_model = car_model.strip()  # 去除前后的空格和换行符

        # 找到搜索框并输入车型名
        search_box = driver.find_element(By.CLASS_NAME, "search_text")
        search_box.clear()  # 清除已有内容
        # 输入后等待一会儿再提交
        #search_box.send_keys(car_model)
        #time.sleep(3)  # 模拟延迟
        #search_box.send_keys(Keys.RETURN)  # 提交搜索

        for char in car_model:
            search_box.send_keys(char)  # 逐个字符输入
            time.sleep(0.1)  # 每个字符之间的延迟，可以调整此值来控制速度

        time.sleep(1)  # 可以在最后输入后再停顿一下，模拟按下回车的等待
        search_box.send_keys(Keys.RETURN)  # 提交搜索

        # 等待页面加载
        time.sleep(5)  # 你可以根据页面加载时间调整

        # 获取当前页面 URL
        current_url = driver.current_url

        # 将车型名和网址写入 CSV 文件
        writer.writerow({'车型名': car_model, '网址': current_url})

        print(f"已搜索车型: {car_model}，网址: {current_url}")

# 关闭浏览器
driver.quit()

print("所有车型搜索完成，结果已保存到 CSV 文件中。")
