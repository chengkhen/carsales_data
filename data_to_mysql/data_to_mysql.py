import pandas as pd
import mysql.connector

# 读取 Excel 文件
file_path = 'C:/Users/86152/Desktop/生产实习/爬取数据/cpi.xlsx'
df = pd.read_excel(file_path)
# 去除所有列名的前后空格
df.columns = df.columns.str.strip()
# 连接到 MySQL 数据库
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='carsale'
    )
    cursor = conn.cursor()

    # 获取 DataFrame 的列名
    columns = df.columns.tolist()
    # 检查列是否与数据库表的列完全一致
    # expected_columns = ['品牌', '201501', '201502', '201503', '201504', '201505', '201506', '201507', '201508', '201509', '201510', '201511', '201512', '201601', '201602','201603', '201604', '201605', '201606', '201607',
    #                            '201608', '201609', '201610', '201611', '201612', '201701', '201702', '201703', '201704', '201705',
    #                            '201706', '201707', '201708', '201709', '201710', '201711', '201712', '201801', '201802', '201803',
    #                            '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812', '201901',
    #                            '201902', '201903', '201904', '201905', '201906', '201907', '201908', '201909', '201910', '201911',
    #                            '201912', '202001', '202002', '202003', '202004', '202005', '202006', '202007', '202008', '202009',
    #                            '202010', '202011', '202012', '202101', '202102', '202103', '202104', '202105', '202106', '202107',
    #                            '202108', '202109', '202110', '202111', '202112', '202201', '202202', '202203', '202204', '202205',
    #                            '202206', '202207', '202208', '202209', '202210', '202211', '202212', '202301', '202302', '202303',
    #                            '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311', '202312', '202401',
    #                            '202402', '202403', '202404', '202405', '202406', '202407', '202408', '202409', '202410', '202411']
    # # 打印 DataFrame 列名和预期列名
    # print("DataFrame columns:", df.columns.tolist())
    # print("Expected columns:", expected_columns)
    # # 检查列数是否匹配
    # if len(df.columns) != len(expected_columns):
    #     raise ValueError(
    #         "The number of columns in DataFrame does not match the expected number of columns in the database table.")
    #
    # if columns != expected_columns:
    #     raise ValueError("DataFrame columns do not match the database table structure.")


    # 动态生成 SQL 插入语句
    placeholders = ', '.join(['%s'] * len(columns))  # 每一列的占位符
    column_names = ', '.join([f"`{col}`" for col in columns])  # 列名用反引号括起来

    insert_query = f"""
    INSERT IGNORE INTO cpi ({column_names})
    VALUES ({placeholders})
    """

    # 将每一行数据转换为元组，准备批量插入
    values = []
    for index, row in df.iterrows():
        # 替换缺失值 (NaN 或 None) 为 NULL
        row_values = [None if pd.isna(value) else value for value in row]
        values.append(tuple(row_values))

    # 执行批量插入
    cursor.executemany(insert_query, values)

    # 提交事务
    conn.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
    conn.rollback()

finally:
    # 关闭连接
    cursor.close()
    conn.close()
