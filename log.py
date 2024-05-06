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
    @classmethod
    def categor(self):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.execute('SELECT * FROM category')
            data = curr.fetchall()
            user.commit()
            user.close()
            return data
        except:
            print('lose')
    @classmethod
    def user_id(self, login, password):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            query = f'SELECT id FROM user WHERE login = %s AND password = %s'
            curr.execute(query, (login, password))
            data = curr.fetchall()[0][0]
            user.commit()
            user.close()
            return data
        except:
            print('lose')
    @classmethod
    def new_expenses(self, user_id, category_id, price, p_date):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.callproc('create_new_expenses', [user_id, category_id, price, p_date])
            user.commit()
            user.close()
        except:
            print('lose')
    @classmethod
    def balance(self, users_id):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            query = f'SELECT balance FROM total_result WHERE user_id = %s'
            curr.execute(query, [users_id])
            data = curr.fetchall()[0][0]
            print(data)
            user.commit()
            user.close()
            return data
        except:
            print('lose')
    @classmethod
    def list_of_expenses(self, userr_id):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.callproc('expenes_list', [userr_id])
            stored_result = curr.stored_results()
            reply = next(stored_result)
            data = reply.fetchall()
            user.commit()
            user.close()
            return data
        except:
            print('lose')
    @classmethod
    def admin_data_months(self):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.callproc('data_month')
            stored_result = curr.stored_results()
            reply = next(stored_result)
            data = reply.fetchall()
            user.commit()
            user.close()
            return data
        except:
            print('lose')
    @classmethod
    def admin_data_by_categorys(self):
        try:
            user = mysql.connector.connect(
                user='root',
                password='',
                host='localhost',
                database='bunk'
            )
            curr = user.cursor()
            curr.callproc('admin_data_categor')
            stored_result = curr.stored_results()
            reply = next(stored_result)
            data = reply.fetchall()
            user.commit()
            user.close()
            return data
        except:
            print('lose')