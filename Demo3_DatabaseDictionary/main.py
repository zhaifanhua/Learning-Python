import mysql.connector
import importlib
import json
import sys
import time
from distlib.compat import raw_input


def generate(host: str, port: int, user: str, password: str, use_pure: bool, database_name: str):
    importlib.reload(sys)
    # 使用前修改配置
    conn = mysql.connector.connect(host=host, port=port, user=user, password=password, use_pure=use_pure)
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME, TABLE_COMMENT "
                   "FROM information_schema.TABLES "
                   "WHERE table_type='BASE TABLE' AND TABLE_SCHEMA='%s'" % database_name)
    tables = cursor.fetchall()
    markdown_table_header = """\n\n\n### %s (%s) \n| 序号 | 字段名称 | 数据类型 | 是否为空 | 字段说明 |\n| :--: |----| ---- | ---- | ---- |\n """
    markdown_table_row = """| %s | %s | %s | %s | %s |"""
    with open(database_name + ".md", "a", encoding="utf8") as md_file:
        for table in tables:
            cursor.execute(
                "SELECT ORDINAL_POSITION, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_COMMENT "
                "FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s'" % (
                    database_name, table[0])
            )
            tmp_table = cursor.fetchall()
            p = markdown_table_header % (table[0], remove_newline(table[1]))
            for col in tmp_table:
                p += (remove_newline(markdown_table_row % col) + "\n")
            md_file.writelines(p)
        md_file.close()
    raw_input("查询完毕！请在" + database_name + ".md中查看结果，感谢您的使用，请按任意键退出此窗口！")


def remove_newline(text):
    """
    去除文本中的换行符号
    """
    return text.replace("\r", "").replace("\n", "")


def read_json():
    try:
        with open('config.json', 'r', encoding="utf8") as c:
            config_json = json.load(c)
    except:
        print("配置文件出错，请检查config.json文件，按任意键退出此窗口")
        time.sleep(8)
        sys.exit(1)
    return config_json


if __name__ == '__main__':
    config = read_json()
    generate(config["host"], config["port"], config["user"], config["password"], config["use_pure"], config["database_name"])
