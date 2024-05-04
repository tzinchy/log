import flet as ft
import mysql.connector
from log import Db_func

def admin_page(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.add(ft.SafeArea(ft.Row([ft.Text('admin cabinet')], alignment=ft.MainAxisAlignment.CENTER)))


def user_page(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.add(ft.Row([ft.Text("Personal cabinet")], alignment=ft.MainAxisAlignment.CENTER))


def to_loging_user(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'

    def finder(e):
        reply = Db_func.try_to_find_user(login.value, password.value)
        if (login.value == 'admin' and password.value == 'admin'):
            admin_page(page)
        else:
            if reply == 'user exist':
                user_page(page)

            else:
                res = ft.Banner(bgcolor=ft.colors.AMBER_100,
                                leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                                content=ft.Text(f"{reply}"), )
                page.dialog = res
                res.open = True
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

    def to_logging_user(e):
        to_loging_user(page)

    def to_registrate_user(e):
        registration_user(page)

    # переменные для действитя пользователя
    to_reg = ft.TextButton('Registration', on_click=to_registrate_user)
    to_log = ft.TextButton('Login', on_click=to_logging_user)
    page.add(ft.SafeArea(ft.Row([to_reg, to_log], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()


if __name__ == '__main__':
    ft.app(chooser)
