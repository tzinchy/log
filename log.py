import mysql.connector
class Db_func:
    @classmethod
    def create_user(self, login, password):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.callproc('create_new_user', [login, password])
            stored_result = curr.stored_results()
            reply = next(stored_result)
            data = reply.fetchall()[0][0]
            user.commit()
            user.close()
            return data
        except:
            print('lose')

    @classmethod
    def try_to_find_user(self, login, password):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.callproc('try_to_find_user', [login, password])
            stored_result = curr.stored_results()
            reply = next(stored_result)
            data = reply.fetchall()[0][0]
            user.commit()
            user.close()
            return data
        except:
            print('lose')
