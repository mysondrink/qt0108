"""
@Description：注册界面控制类
@Author：mysondrink@163.com
@Time：2024/1/11 17:17
"""
from controller.AbstractController import AbstractController
import pymysql

FAILED_CODE = 404
SUCCEED_CODE = 202


class RegisterController(AbstractController):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()


    """
    @detail 注册用户写入数据库
    """
    def insertUser(self, username, usercode):
        user_name = username
        user_code = usercode
        host = "127.0.0.1"
        user = "root"
        password = "password"
        port = 3306
        database = "test"
        charset = "utf8"
        connection = pymysql.connect(host=host, user=user, password=password, port=port, database=database,
                                     charset=charset)
        # MySQL语句
        sql = 'INSERT INTO user_table(user_name, user_code) VALUES (%s,%s)'

        # 获取标记
        cursor = connection.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, [user_name, user_code])
            # 提交事务
            connection.commit()
        except Exception as e:
            # print(str(e))
            # 有异常，回滚事务
            connection.rollback()
        # 释放内存
        cursor.close()
        connection.close()

        self.update_json.emit(dict(code=SUCCEED_CODE))
