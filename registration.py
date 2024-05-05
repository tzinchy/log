from log import Db_func
print(Db_func.balance(1))
data  = Db_func.list_of_expenses(1)
for i in data:
    print(i)