import flet as ft
import mysql.connector
from log import Db_func
import datetime

def admin_page(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'
    page.add(ft.SafeArea(ft.Row([ft.Text('admin cabinet')], alignment=ft.MainAxisAlignment.CENTER)))

def user_page(page: ft.Page, user_id):
    print(user_id)
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.title = 'bunk.app'
    page.add(ft.Row([ft.Text("Personal cabinet")], alignment=ft.MainAxisAlignment.CENTER))
    def printer(e):
        print(data.value)
        print(f"{str(date_picker.value).split()[0]} {time_picker.value}")
        print(price.value)

    btn = ft.ElevatedButton(text="SUBMIT", on_click=printer, width=400)
    price = ft.TextField(label='Сумма', width=400)
    first, second, third = Db_func.categor()
    data = ft.Dropdown(width=100, options=[ft.dropdown.Option(key=first[0], text=f"{first[1]}"),
                                           ft.dropdown.Option(key=second[0], text=f"{second[1]}"),
                                           ft.dropdown.Option(key=second[0], text=f"{third[1]}")])

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

    date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date(),
    )

    page.add(ft.SafeArea(ft.Row([price], alignment=ft.MainAxisAlignment.END)))
    page.add(ft.SafeArea(ft.Row([data, time_button, date_button], alignment=ft.MainAxisAlignment.END)))
    page.add(ft.SafeArea(ft.Row([btn], alignment=ft.MainAxisAlignment.END)))

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
    page.add(ft.SafeArea(ft.Row([ft.IconButton(icon=ft.icons.DONE, icon_color="blue400", icon_size=20, tooltip="Done", on_click=finder, width=600)], alignment=ft.MainAxisAlignment.CENTER)))
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
            res = ft.AlertDialog(title=ft.Text(f"ERROR YOUR ACCOUNT DOESNT CREATED\n{reply}"), on_dismiss=lambda e: print("error"))
            page.dialog = res
            res.open = True
            page.update()

    def to_log_window(e):
        to_loging_user(page)

    # добавляем все необходимые объекты на страницу с входом в аккаунт
    login_to_registration = ft.TextField(label='Login')
    password_to_registration = ft.TextField(label='Password', password=True, can_reveal_password=True)
    page.add(ft.SafeArea(ft.Row([ft.Text("Registration")], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([login_to_registration, password_to_registration], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([ft.TextButton('Registration', on_click=regist)], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([ft.TextButton('Have a account? - login', on_click=to_log_window)], alignment=ft.MainAxisAlignment.CENTER)))
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
    to_reg = ft.TextButton('Registration', on_click=to_registrate_user, width= 175)
    to_log = ft.TextButton('Login', on_click=to_logging_user, width= 175)
    page.add(ft.SafeArea(ft.Row([to_reg, to_log], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()


if __name__ == '__main__':
    ft.app(chooser)
