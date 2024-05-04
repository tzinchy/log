import flet as ft
import mysql.connector

user = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='log'
)

def registration_user(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    #функция для перехода в окно логина
    def to_log_window(e):
        loging_user(page)
    #добавляем все необходимые объекты для регистрации пользователя
    page.add(ft.SafeArea(ft.Row([ft.Text("СТРАНИЦА С ВХОДОМ")], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([ft.TextButton('Для прехода на логирование', on_click=to_log_window)], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()

def loging_user(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    #функция для перехода в окно регистрации
    def to_registration_window(e):
        registration_user(page)
    #добавляем все необходимые объекты на страницу с входом в аккаунт
    login = ft.TextField(label='Login')
    password = ft.TextField(label='Password')
    page.add(ft.SafeArea(ft.Row([ft.Text("РЕГИСТРАЦИЯ")], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([login, password], alignment=ft.MainAxisAlignment.CENTER)))
    page.add(ft.SafeArea(ft.Row([ft.TextButton('Для прехода на логирование', on_click=to_registration_window)], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()


def chooser(page: ft.Page):
    page.clean()
    page.theme_mode = 'dark'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    def to_loging_user(e):
        loging_user(page)
    def to_registrate_user(e):
        registration_user(page)
    #переменные для действитя пользователя
    to_reg = ft.TextButton('Зарегестрироваться', on_click=to_loging_user)
    to_log = ft.TextButton('Войти',on_click=to_registrate_user)
    page.add(ft.SafeArea(ft.Row([to_reg, to_log], alignment=ft.MainAxisAlignment.CENTER)))
    page.update()

if __name__ == '__main__':
    ft.app(chooser, view = ft.WEB_BROWSER)
