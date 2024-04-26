import flet as ft
import mysql.connector
import db_quer
from user_class import *
loggs= {'sasha':'pull'}
user = None
password = None
def main(page: ft.Page):

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def to_account(e):
        global user
        user = username_or_email.value
        if user in loggs:
            return True
        else:
            print('not correct')
            return False

    def check_password(e):
        global password
        password = cpassword.value
        if loggs.get(user, None) == password:
            return True
        else:
            print('not correct')
            return False

    page.title = 'to-do-list'
    username_or_email = ft.TextField(label='Login or Email', width=150, on_submit=to_account)
    cpassword = ft.TextField(label='password', width=150, on_submit=check_password)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(ft.Row([username_or_email, cpassword], alignment=ft.MainAxisAlignment.CENTER))


if __name__ == "__main__":
    ft.app(main)
