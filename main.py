import flet as ft
import matplotlib

matplotlib.use('Agg')  # Устанавливаем бэкенд, который не требует оконного сервера
import mysql.connector
from log import Db_func
import datetime
from decimal import Decimal
import plotly.graph_objs as go
import plotly.io as pio
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt


def admin_page(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'
    page.add(ft.SafeArea(ft.Row([ft.Text('admin cabinet')], alignment=ft.MainAxisAlignment.CENTER)))
    data_about_cat = Db_func.admin_data_by_categorys()
    data_about_months = Db_func.admin_data_months()

    def visualize_expenses_by_category(e):
        nonlocal data_about_cat  # Используем nonlocal, чтобы ссылаться на внешнюю переменную

        # Извлечение данных
        categories = [item[0] for item in data_about_cat]
        amounts = [float(item[1]) for item in data_about_cat]

        # Создание круговой диаграммы
        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title('Распределение трат по категориям')

        # Сохранение диаграммы в файл
        plt.savefig('pie_chart_admin.png')
        plt.close()  # Закрыть фигуру после сохранения

        # Отображение диалогового окна с помощью вашего фреймворка
        res = ft.AlertDialog(title=ft.Text(f"График успешно сохранен"),
                             on_dismiss=lambda e: print("error"))
        page.dialog = res  # Замените 'page' на ваш контекст страницы
        res.open = True
        page.update()  # Обновите страницу или контекст, чтобы обновления отобразились

    def for_visualisation_cat(e):
        nonlocal data_about_cat
        # Извлечение данных
        categories = [item[0] for item in data_about_cat]
        amounts = [float(item[1]) for item in data_about_cat]

        # Создание круговой диаграммы
        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title('Распределение трат по категориям')

        # Сохранение диаграммы в файл
        plt.savefig('pie_chart_admin.png')
        plt.close()  # Закрыть фигуру после сохранения
        res = ft.AlertDialog(title=ft.Text(f"График успешно сохранен"),
                             on_dismiss=lambda e: print("error"))
        page.dialog = res
        res.open = True
        page.update()


    page.add(ft.SafeArea(ft.TextButton('Для построения графкиа по категориям', on_click=for_visualisation_cat)))
    page.add(ft.SafeArea(ft.TextButton('Для построения графкиа по месяцам', on_click=visualize_expenses_by_category)))


def user_page(page: ft.Page, user_id):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'
    page.add(ft.Row([ft.Text("Personal cabinet", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)],
                    alignment=ft.MainAxisAlignment.CENTER))
    balance = Db_func.balance(user_id)
    balance_text = ft.TextField(value=balance, read_only=True, label='balance')
    page.update()
    diagrams = Db_func.list_of_expenses(user_id)
    list_expenses = [str(i) for i in Db_func.list_of_expenses(user_id)]

    def save_pie_chart(diagrams, filename="pie_chart.png"):
        category_sums = defaultdict(Decimal)
        for category, amount, _ in diagrams:
            category_sums[category] += amount
        categories = list(category_sums.keys())
        sums = list(category_sums.values())

        plt.figure(figsize=(10, 6))
        plt.pie(sums, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Распределение трат по категориям')
        plt.savefig(filename)
        plt.close()

    def save_bar_chart(diagrams, filename="bar_chart.png"):
        category_sums = defaultdict(Decimal)
        for category, amount, _ in diagrams:
            category_sums[category] += amount
        categories = list(category_sums.keys())
        sums = list(category_sums.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categories, sums, color='skyblue')
        plt.title('Распределение трат по категориям')
        plt.xlabel('Категории')
        plt.ylabel('Суммы')
        plt.savefig(filename)
        plt.close()

    def close_anchor(e):
        text = f"Трата выбрана"
        print(f"closing view from {text}")
        anchor.close_view(text)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    anchor_controls = [
        ft.ListTile(title=ft.Text(str(i)), on_click=close_anchor, data=i[0])
        for i in list_expenses
    ]

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Find your expenses",
        view_hint_text="Choose expenses",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=anchor_controls,
        width=200
    )

    # Создаем кнопку
    open_list_button = ft.OutlinedButton("Open list expenses", on_click=lambda _: anchor.open_view())

    # Создаем Row и добавляем в него кнопку и SearchBar (anchor)
    controls_row = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            open_list_button,
            anchor,  # Добавляем SearchBar справа от кнопки
        ],
    )

    def printer(e):
        nonlocal balance, balance_text
        if (int(price.value) <= int(balance)):
            date_of_expenses = f"{str(date_picker.value).split()[0]} {time_picker.value}"
            Db_func.new_expenses(user_id, category.value, price.value, date_of_expenses)
            balance = Db_func.balance(user_id)
            balance_text.value = balance

            res = ft.AlertDialog(title=ft.Text(f"ТРАНЗАКЦИЯ ПРОШЛА УСПЕШНО"),
                                 on_dismiss=lambda e: print("error"))
            page.dialog = res
            res.open = True
            page.update()

        else:
            page.update()
            res = ft.AlertDialog(title=ft.Text(f"ТРАНЗАКЦИЯ ОТКЛОНЕНА"),
                                 on_dismiss=lambda e: print("error"))
            page.dialog = res
            res.open = True
            page.update()

    btn = ft.ElevatedButton(text="SUBMIT", on_click=printer, width=400)
    price = ft.TextField(label='Сумма', width=400)
    first, second, third = Db_func.categor()
    category = ft.Dropdown(width=100, options=[ft.dropdown.Option(key=first[0], text=f"{first[1]}"),
                                               ft.dropdown.Option(key=second[0], text=f"{second[1]}"),
                                               ft.dropdown.Option(key=third[0], text=f"{third[1]}")])

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
    )

    page.overlay.append(time_picker)

    time_button = ft.ElevatedButton(
        "Pick time",
        icon=ft.icons.TIMELAPSE,
        on_click=lambda _: time_picker.pick_time(),
    )
    date_picker = ft.DatePicker(
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )

    page.overlay.append(date_picker)
    graphics = ft.Dropdown(width=100, options=[ft.dropdown.Option(key='bar', text=f"round diagram"),
                                               ft.dropdown.Option(key='plot', text=f"plot diagram")])
    date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date(),
    )
    img1 = ft.Image(
        src=f"bar_chart.png",
        width=300,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    img2 = ft.Image(
        src=f"pie_chart.png",
        width=300,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    def create_graph(e):
        res = ft.AlertDialog(title=ft.Text(f"РЕЗУЛЬТАТ СОХРАНЕН"),
                             on_dismiss=lambda e: print("error"))
        page.dialog = res
        res.open = True
        page.update()
        if 'bar' in str(graphics.value):
            save_bar_chart(diagrams)
        elif 'plot' in str(graphics.value):
            save_pie_chart(diagrams)

    page.add(ft.SafeArea(
        ft.Row([controls_row, img1, img2, ft.Text("Example of diagrams")], alignment=ft.MainAxisAlignment.START)))
    page.add(ft.SafeArea(ft.Row([graphics, ft.TextButton("Для построения графика", on_click=create_graph)],
                                alignment=ft.MainAxisAlignment.START)))
    page.add(ft.SafeArea(ft.Row([balance_text], alignment=ft.MainAxisAlignment.END)))
    page.add(ft.SafeArea(ft.Row([price], alignment=ft.MainAxisAlignment.END)))
    page.add(ft.SafeArea(ft.Row([category, time_button, date_button], alignment=ft.MainAxisAlignment.END)))
    page.add(ft.SafeArea(ft.Row([btn], alignment=ft.MainAxisAlignment.END)))

    page.update()


def to_loging_user(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'

    def finder(e):
        reply = Db_func.try_to_find_user(login.value, password.value)
        if (login.value == 'admin' and password.value == 'admin'):
            admin_page(page)
        else:
            if reply == 'user exist':
                id = Db_func.user_id(login.value, password.value)
                user_page(page, id)
            else:
                def close_banner(e):
                    page.banner.open = False
                    page.update()

                page.banner = ft.Banner(
                    bgcolor=ft.colors.AMBER_700,
                    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER_300, size=40),
                    content=ft.Text(
                        "Something wrong!?"
                    ),
                    actions=[
                        ft.TextButton("Retry", on_click=close_banner),

                    ],
                )
                page.banner.open = True
                page.update()

    # функция для перехода в окно логина
    def to_reg_window(e):
        registration_user(page)

    # добавляем все необходимые объекты для регистрации пользователя
    login = ft.TextField(label='Login')
    password = ft.TextField(label='Password', password=True, can_reveal_password=True)
    page.add(ft.SafeArea(ft.Row([ft.Text("Login to app")], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([login, password], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([ft.IconButton(icon=ft.icons.DONE, icon_color="blue400", icon_size=20, tooltip="Done",
                                               on_click=finder, width=600)], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(
        ft.Row([ft.TextButton('Registration', on_click=to_reg_window)], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()


def registration_user(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'

    # функция для перехода в окно регистрации
    def regist(e):
        reply = Db_func.create_user(login_to_registration.value, password_to_registration.value)
        if reply == 'USER CREATED':
            res = ft.AlertDialog(title=ft.Text(f"{reply}"), on_dismiss=lambda e: print("error"))
            page.dialog = res
            res.open = True
            page.update()
        else:
            res = ft.AlertDialog(title=ft.Text(f"ERROR YOUR ACCOUNT DOESNT CREATED\n{reply}"),
                                 on_dismiss=lambda e: print("error"))
            page.dialog = res
            res.open = True
            page.update()

    def to_log_window(e):
        to_loging_user(page)

    # добавляем все необходимые объекты на страницу с входом в аккаунт
    login_to_registration = ft.TextField(label='Login')
    password_to_registration = ft.TextField(label='Password', password=True, can_reveal_password=True)
    page.add(ft.SafeArea(ft.Row([ft.Text("Registration")], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(
        ft.SafeArea(ft.Row([login_to_registration, password_to_registration], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(
        ft.SafeArea(ft.Row([ft.TextButton('Registration', on_click=regist)], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([ft.TextButton('Have a account? - login', on_click=to_log_window)],
                                alignment=ft.MainAxisAlignment.CENTER)))
    page.update()


def chooser(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'
    img = ft.Image(
        src=f"topburch3.png",
        width=500,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    def to_logging_user(e):
        to_loging_user(page)

    def to_registrate_user(e):
        registration_user(page)

    page.add(img)
    # переменные для действитя пользователя
    to_reg = ft.TextButton('Registration', on_click=to_registrate_user, width=175)
    to_log = ft.TextButton('Login', on_click=to_logging_user, width=175)
    page.add(ft.SafeArea(ft.Row([to_reg, to_log], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()


if __name__ == '__main__':
    ft.app(chooser)
