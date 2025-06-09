import pickle
from prettytable import *
nm = ['ФИО', 'Возраст', 'Должность', 'Зарплата', 'Стаж']
dt = ['Соловьев Н.С.', '65', 'Директор', '150000', '12', 'Брежнев Л.И.', '45', 'Зам. директора', '120000', '10', 'Коробова С.И.', '34', 'Главный бухгалтер', '100000', '7', 'Старков Н.В.', '35', 'Завхоз', '70000', '10', 'Баранова С.А.', '33', 'Зав. складом', '90000', '6']
all = [nm, dt]

def inp(nm, dt):
    f = open('all.bin', 'wb')
    pickle.dump(all, f)
    f.close()

def out():
    tab = PrettyTable()
    f = open('all.bin', 'rb')
    all = pickle.load(f)
    tab.field_names = all[0]
    rows1 = all[1]
    row = []
    rows = []
    for i in range(len(rows1)):
        if i % 5 == 0 and i > 0:
            rows.append(row)
            row = []
        row.append(rows1[i])
    tab.add_rows(rows)
    print(tab)
inp(nm, dt)
out()