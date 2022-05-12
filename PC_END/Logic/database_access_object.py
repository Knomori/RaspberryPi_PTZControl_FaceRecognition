import sqlite3

from Logic import client_parameter


# 读取数据库不加锁，写数据库加锁


class DAO():
    def get_all_data(self):
        try:
            conn = sqlite3.connect(client_parameter.face_sqlite_path)
            c = conn.cursor()
            all_data = c.execute("SELECT recongition_sequence,name,identity_codes,is_clocked,clock_time FROM user_data")

            all_rows = []
            for data in all_data:
                one_row = [str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4])]
                all_rows.append(one_row)

            conn.commit()
            c.close()
            conn.close()

            return all_rows  # 返回的是二维列表
        except:
            print("database_access_object.py线程数据库访问失败")  # 也有可能数据库正在生成

    def get_data_use_name(self, name_to_search):
        try:
            conn = sqlite3.connect(client_parameter.face_sqlite_path)
            c = conn.cursor()
            sql = "SELECT recongition_sequence,name,identity_codes,is_clocked,clock_time FROM user_data WHERE name LIKE '%" + name_to_search + "%'"
            all_data = c.execute(sql)

            all_rows = []
            for data in all_data:
                one_row = [str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4])]
                all_rows.append(one_row)

            conn.commit()
            c.close()
            conn.close()

            return all_rows  # 返回的是二维列表
        except:
            print("database_access_object.py 的 get_data_use_name 线程数据库访问失败")  # 也有可能数据库正在生成

    def modify_new_data(self, new_datas):
        print("准备写入新数据")
        client_parameter.mutex_modify_db.lock()

        try:
            conn = sqlite3.connect(client_parameter.face_sqlite_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_data")  # 先删除所有的

            # 然后插入新的
            for row_data in new_datas:
                if row_data[3] == "是":
                    row_data[3] = 1
                elif row_data[3] == "否":
                    row_data[3] = 0
                elif row_data[3] == "-":
                    row_data[3] = 0
                else:
                    row_data[3] = 500

                cursor.execute(
                    "INSERT INTO user_data (recongition_sequence, name,identity_codes,is_clocked,clock_time) VALUES ('{}','{}','{}','{}','{}')"
                        .format(row_data[0], row_data[1], row_data[2], int(row_data[3]), row_data[4]))

            conn.commit()
            cursor.close()
            conn.close()
        except:
            print("database_access_object.py 的 get_data_use_name 线程数据库访问失败")  # 也有可能数据库正在生成

        client_parameter.mutex_modify_db.unlock()
