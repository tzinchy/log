import flet as ft
import mysql.connector

class User:
    def __init__(self, use, passw):
        self.user = use
        self.password = passw

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, use):
        self.__user = use

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, passw):
        self.__password = passw

#connection from mysql to py
db_connection = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='log'
)
conn = db_connection.cursor()
def main_page(page):
    def quer(e):
        main(page)
        page.update()
    page.clean()
    page.update()
    page.add(ft.Text("РАБОТАЕТ"))
    page.add(ft.TextButton('Нажми и верни все', on_click=quer))
    page.update()
#created window
def main(page: ft.Page):
    def start():
        page.clean()
        page.title = "loggs app"
        page.theme_mode = 'dark'
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def close_banner(e):
            page.banner.open = False
            page.update()

        eror_login = ft.Banner(
            bgcolor=ft.colors.RED,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLUE_ACCENT, size=40),
            content=ft.Text(
                "Пользователь не найден"
            ),
            actions=[
                ft.TextButton("Попробуйте снова", on_click=close_banner),
            ],
        )
        eror_password = ft.Banner(
            bgcolor=ft.colors.RED,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLUE_ACCENT, size=40),
            content=ft.Text(
                "Ошибка в пароле"
            ),
            actions=[
                ft.TextButton("Попробуй снова", on_click=close_banner),
            ],
        )

        def show_error_login():
            page.dialog = eror_login
            eror_login.open = True
            page.update()

        def show_error_password():
            page.dialog = eror_password
            eror_password.open = True
            page.update()

        def show_welcome(user1):
            dlg = ft.AlertDialog(
                title=ft.Text(f'ДОБРО ПОЖАЛОВАТЬ\nLOGIN {user1.user}\nPASSWORD {user1.password}'),
                on_dismiss=lambda e: print("Dialog dismissed!")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            db_connection.commit()

        # Словарь соответствия сообщений и функций
        message_actions = {
            'Login not found.': show_error_login,
            'Incorrect password provided.': show_error_password
        }

        def done(e):
            main_page(page)
            page.update()

        def checker(e):
            user1 = User(log.value, password.value)
            try:
                conn.callproc('AuthenticateUser', [user1.user, user1.password])
                result = next(conn.stored_results())
                message = result.fetchall()[0][0]

                # Вызываем соответствующую функцию из словаря или показываем приветствие, если сообщение не найдено
                action = message_actions.get(message, lambda: show_welcome(user1))
                action()

            except Exception as ex:
                print('Error:', ex)

        log = ft.TextField(label="login", width=200)
        password = ft.TextField(label='password', width=200, can_reveal_password=True, password=True)
        enter = ft.TextButton("Go to", width=400, height=50, on_click=checker)
        page.add(ft.SafeArea(ft.Row(
            [ft.Text("Введите данные для входа в учетную запись", size=15, weight=ft.FontWeight.W_500, selectable=True)],
            alignment=ft.MainAxisAlignment.CENTER)))
        page.add(ft.SafeArea(ft.Row([log, password], alignment=ft.MainAxisAlignment.CENTER)))
        page.add(ft.SafeArea(ft.Row([enter], alignment=ft.MainAxisAlignment.CENTER)))
        page.add(ft.TextButton('НАЖМИНА НА МЕНЯ', on_click=done))
        page.update()
    start()
if __name__ == "__main__":
    ft.app(target=main_page, view=ft.WEB_BROWSER)
