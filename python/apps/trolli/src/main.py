from board import Board
import os
import flet
from flet.buttons import RoundedRectangleBorder
from flet.auth.providers.auth0_oauth_provider import Auth0OAuthProvider
from flet.security import decrypt, encrypt
from flet import (
    UserControl,
    View,
    AlertDialog,
    Column,
    Row,
    Container,
    Icon,
    Page,
    Text,
    ElevatedButton,
    AppBar,
    PopupMenuButton,
    PopupMenuItem,
    TextField,
    colors,
    icons,
    padding,
    theme,
    margin,
    TemplateRoute,
)
from user import User
from data_store import DataStore
from memory_store import InMemoryStore
from app_layout import AppLayout
from landing_page import LandingPage


class TrelloApp(UserControl):
    def __init__(self, page: Page, store: DataStore):
        super().__init__()
        self.page = page
        self.store: DataStore = store
        self.page.on_route_change = self.route_change
        self.boards = self.store.get_boards()
        self.logged_in_user = ""
        self.login_profile_button = PopupMenuItem(
            text="Log in", on_click=self.login)
        self.logout_button = PopupMenuItem(
            text="Log out", on_click=self.logout)
        self.appbar_items = [
            self.login_profile_button,
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Settings")
        ]
        self.appbar = AppBar(
            leading=Icon(icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=Text(f"Trolli", font_family="Pacifico",
                       size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                Container(
                    content=PopupMenuButton(
                        items=self.appbar_items
                    ),
                    margin=margin.only(left=50, right=25)
                )
            ],
        )
        self.page.appbar = self.appbar
        self.encryption_key = os.getenv("TROLLI_ENCRYPTION_KEY")
        self.provider = Auth0OAuthProvider(
            domain="dev-j3wnirdjarxj51uz.us.auth0.com",
            client_id=os.getenv("AUTH0_CLIENT_ID"),
            client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
            redirect_url="http://localhost:8088/api/oauth/redirect",

        )

        page.on_login = self.on_login
        page.on_logout = self.on_logout
        self.app_layout = AppLayout(self, self.page, self.store,
                                    tight=True, expand=True, vertical_alignment="start")
        self.landing_page = LandingPage(self, self.page, alignment=flet.MainAxisAlignment.CENTER,
                                        vertical_alignment=flet.CrossAxisAlignment.CENTER, height=(self.page.height-75))

        self.page.update()

    def build(self):
        self.layout = self.app_layout if self.page.auth is not None else self.landing_page
        return self.layout

    def set_authorized(self):
        self.layout = self.app_layout
        self.update()

    def on_login(self, e):

        def close_dlg(e):
            dialog.open = False
            self.page.update()
            self.page.login(self.provider)

        dialog = AlertDialog(
            title=Text("Please verify your email to continue"),
            content=Column([
                Row([
                    ElevatedButton(
                        text="Email verified", on_click=close_dlg)
                ], alignment="center")
            ], tight=True),
            modal=True
        )

        if e.error:
            raise Exception(e.error)

        if self.page.auth.user['email_verified'] is False:

            print("not verified")
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
        else:
            self.layout = self.app_layout
            self.update()

            self.initialize()
            #jt = self.page.auth.token.to_json()
            #ejt = encrypt(jt, self.encryption_key)
            #self.page.client_storage.set("trolli_token", ejt)
            self.layout.sidebar.set_workspace_user(
                self.page.auth.user["nickname"])
            self.layout.update()
            self.logged_in_user = self.page.auth.user["nickname"]
            self.set_login_button()
            print("self.page.auth.user: ", self.page.auth.user)
            self.page.update()

    def on_logout(self, e):
        self.provider.query_params = "?prompt=login"
        self.layout.sidebar.set_workspace_user()
        self.set_login_button()
        self.page.update()

    def set_login_button(self):
        if self.page.auth is None:
            self.appbar_items[0] = self.login_profile_button
        else:
            self.logout_button.text = f"Log out {self.logged_in_user}"
            self.appbar_items[0] = self.logout_button
            self.appbar.update()

    def initialize(self):
        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                [
                    self.appbar,
                    self.layout
                ],
                padding=padding.all(0),
                bgcolor=colors.BLUE_GREY_200
            )
        )
        self.page.update()
        # create an initial board for demonstration if no boards
        if len(self.boards) == 0:
            self.create_new_board("My First Board")
        self.page.go("/")

    def login(self, e):
        self.page.client_storage.clear()
        saved_token = None
        ejt = self.page.client_storage.get("trolli_token")
        if ejt:
            saved_token = decrypt(ejt, self.encryption_key)
        if e is not None or saved_token is not None:
            self.page.login(self.provider)

    def logout(self, e):
        self.page.client_storage.remove("trolli_token")
        self.page.logout()

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/boards")
        elif troute.match("/board/:id"):
            if int(troute.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.layout.set_board_view(int(troute.id))
        elif troute.match("/boards"):
            self.layout.set_all_boards_view()
        elif troute.match("/members"):
            self.layout.set_members_view()
        self.page.update()

    def add_board(self, e):

        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (type(e.control) is TextField and e.control.value != ""):
                self.create_new_board(dialog_text.value)
            dialog.open = False
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = TextField(label="New Board Name",
                                on_submit=close_dlg, on_change=textfield_change)
        create_button = ElevatedButton(
            text="Create", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True)
        dialog = AlertDialog(
            title=Text("Name your new board"),
            content=Column([
                dialog_text,
                Row([
                    ElevatedButton(
                        text="Cancel", on_click=close_dlg),
                    create_button
                ], alignment="spaceBetween")
            ], tight=True),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def create_new_board(self, board_name):
        new_board = Board(self, self.store, board_name)
        self.store.add_board(new_board)
        self.layout.hydrate_all_boards_view()

    def delete_board(self, e):
        self.store.remove_board(e.control.data)
        self.layout.set_all_boards_view()


if __name__ == "__main__":

    def main(page: Page):

        page.title = "Flet Trello clone"
        page.padding = 0
        page.theme = theme.Theme(
            font_family="Verdana")
        page.theme.page_transitions.windows = "cupertino"
        page.fonts = {
            "Pacifico": "/Pacifico-Regular.ttf"
        }
        page.bgcolor = colors.BLUE_GREY_200
        app = TrelloApp(page, InMemoryStore())
        page.add(app)
        page.update()

    flet.app(target=main, port=8088,
             assets_dir="../assets", view=flet.WEB_BROWSER)
