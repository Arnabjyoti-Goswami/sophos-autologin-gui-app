# source ./venv/Scripts/activate
import tkinter as tk
from tkinter import simpledialog

from customtkinter import CTk as ctk
from customtkinter import CTkButton as ctk_button
from customtkinter import CTkCheckBox as ctk_checkbox
from customtkinter import CTkEntry as ctk_entry
from customtkinter import CTkFont as ctk_font
from customtkinter import CTkFrame as ctk_frame
from customtkinter import CTkLabel as ctk_label
from customtkinter import CTkOptionMenu as ctk_optionmenu
from customtkinter import set_appearance_mode as ctk_set_theme
from customtkinter import set_default_color_theme as ctk_set_color_theme
from customtkinter import set_widget_scaling as ctk_set_widget_scale

from utils import load_credentials, save_credentials_file

# Themes: "System" (standard), "Dark", "Light"
ctk_set_theme("System")
# Color themes: "blue" (standard), "green", "dark-blue"
ctk_set_color_theme("blue")
from customtkinter import ThemeManager


class CustomDialog(simpledialog.Dialog):
    def body(self, master):
        self.label = ctk_label(
            master,
            text="This is a custom dialog box",
            foreground="#ffffff",  # Use 'foreground' instead of 'fg'
            background="#2b2b2b",  # Use 'background' instead of 'bg'
            font=("Arial", 12),
        )

    def apply(self):
        print("You clicked OK")


class Frame(ctk_frame):
    def __init__(
        self,
        master: any,
        grid: tuple[int, int],
        span: tuple[int, int],
        width: int = 200,
        bg_color: tuple[str, str] | str = "transparent",
        fg_color: tuple[str, str] | None = None,
        border_width: int | None = None,
        corner_radius: int = 0,
    ) -> None:
        super().__init__(
            master=master,
            border_width=border_width,
            bg_color=bg_color,
            fg_color=fg_color,
            width=width,
            corner_radius=corner_radius,
        )
        self.grid(
            row=grid[0],
            column=grid[1],
            columnspan=span[1],
            rowspan=span[0],
            sticky="nsew",
        )


class App(ctk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Impartus Downloader")
        self.geometry("1100x580")

        # give a tuple of row/column indices that will have the same weight
        # or give just a single index and specify its weight
        # weight: how much space will be allocated to the row or column when the window is resized
        # configure the grid for the main parent window frame
        self.grid_columnconfigure(1, weight=3, uniform="main_col_group")
        self.grid_rowconfigure((0, 1, 2, 3), weight=1, uniform="main_row_group")

        # sticky: "nsew" (north, south, east, west), if cell is larger, then on which sides will this widget stick to the cell boundary?

        # padx, pady: padding on x and y axis of the widget/element from the boundary of the cell, cell being its position in the grid
        # ipadx, ipady: internal padding on x and y axis of the widget from its own boundary
        # if you provide padding as a single number it will be applied to both sides, so better to provide as a tuple always
        # padx=(20, 0) means 20 padding on left and 0 padding on right, pady=(20, 0) means 20 padding on top and 0 padding on bottom

        # columnspan: how many columns will this widget span
        # rowspan: how many rows will this widget span
        # by default columnspan and rowspan are 1

        # LEFT SIDEBAR FRAME
        self.sidebar_frame = Frame(
            master=self,
            grid=(0, 0),
            span=(4, 1),
            width=140,
            fg_color=("#f0f0f0", "#3b3b42"),
            bg_color=("#dadae8", "#89898f"),
        )
        # configure the left sidebar frame's grid
        self.sidebar_frame.grid_rowconfigure(
            0, weight=8, uniform="sidebar_row_group", pad=0
        )

        # logo label on top left
        self.logo_label = ctk_label(
            master=self.sidebar_frame,
            text="Impartus Downloader",
            font=ctk_font(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=(30, 10), pady=(25, 10), sticky="n")

        # set theme on bottom left
        self.appearance_mode_label = ctk_label(
            master=self.sidebar_frame,
            text="Appearance Mode",
            anchor="w",
            font=ctk_font(size=14),
        )
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(0, 5))

        # initial state shown in the optionmenu for appearance mode
        initial_state = tk.StringVar(self)
        initial_state.set("System")

        self.appearance_mode_optionemenu = ctk_optionmenu(
            master=self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            variable=initial_state,
        )
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(0, 10))

        # set scaling of UI on bottom left
        self.scaling_label = ctk_label(
            master=self.sidebar_frame,
            text="Zoom Level",
            anchor="w",
            font=ctk_font(size=14),
        )
        self.scaling_label.grid(row=3, column=0, padx=20, pady=(0, 5))

        # initial state shown in the optionmenu for scaling of UI
        initial_state = tk.StringVar(self)
        initial_state.set("100%")

        self.scaling_optionemenu = ctk_optionmenu(
            master=self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
            variable=initial_state,
        )
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(0, 20))

        # MAIN FRAME
        self.main_frame = Frame(master=self, grid=(0, 1), span=(4, 3))
        # configure the main frame's grid
        self.main_frame.grid_columnconfigure(
            (0, 1, 2), weight=1, uniform="main_frame_col_group"
        )

        self.login_form()

    def login_form(self) -> None:
        username: str = ""
        password: str = ""
        initial_credentials = load_credentials()
        if type(initial_credentials) == str:
            pass
        elif type(initial_credentials) == dict:
            username = initial_credentials["username"]
            password = initial_credentials["password"]

        initial_username_state = tk.StringVar(self)
        initial_username_state.set(username)
        initial_password_state = tk.StringVar(self)
        initial_password_state.set(password)

        self.username_label = ctk_label(
            master=self.main_frame,
            text="Username",
            font=ctk_font(size=14),
        )
        self.username_label.grid(
            row=0, column=0, padx=(40, 20), pady=(20, 20), sticky="w"
        )

        self.username_input = ctk_entry(
            width=250,
            master=self.main_frame,
            placeholder_text="Username",
            font=ctk_font(size=14),
            textvariable=initial_username_state,
        )
        self.username_input.grid(
            row=1, column=0, padx=(20, 20), pady=(0, 20), sticky="w"
        )

        self.password_label = ctk_label(
            master=self.main_frame,
            text="Password",
            font=ctk_font(size=14),
        )
        self.password_label.grid(row=0, column=2, padx=(20, 20), pady=(20, 20))

        self.password_input_frame = Frame(
            master=self.main_frame,
            grid=(1, 2),
            span=(1, 1),
            fg_color=self.main_frame.cget("fg_color"),
        )
        self.password_input_frame.grid_columnconfigure(
            0, weight=3, uniform="password_input"
        )
        self.password_input_frame.grid_columnconfigure(
            1, weight=1, uniform="password_input"
        )
        self.password_input_frame.grid_rowconfigure(
            0, weight=1, uniform="password_input"
        )
        self.password_input = ctk_entry(
            width=250,
            master=self.password_input_frame,
            placeholder_text="Password",
            font=ctk_font(size=14),
            show="*",
            textvariable=initial_password_state,
        )
        self.password_input.grid(row=0, column=0, padx=(0, 1), pady=(0, 20), sticky="e")

        self.show_password_button = ctk_button(
            master=self.password_input_frame,
            text="Show",
            command=self.toggle_password,
        )
        self.show_password_button.grid(
            row=0, column=1, padx=(0, 0), pady=(0, 20), sticky="e"
        )

        self.submit_credentials_button = ctk_button(
            master=self.main_frame,
            text="Submit",
            command=self.submit_credentials,
            font=ctk_font(size=14, family="Roboto", weight="bold"),
            border_width=2,
            corner_radius=20,
        )
        self.submit_credentials_button.grid(
            row=2, column=1, padx=(20, 20), pady=(0, 20), ipadx=20, ipady=10
        )

    def toggle_password(self):
        if self.password_input.cget("show") == "":
            self.password_input.configure(show="*")
            self.show_password_button.configure(text="Show")
        else:
            self.password_input.configure(show="")
            self.show_password_button.configure(text="Hide")

    def submit_credentials(self):
        username = self.username_input.get()
        password = self.password_input.get()
        if not (username and password):
            return
        save_credentials_file({"username": username, "password": password})

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk_set_theme(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk_set_widget_scale(new_scaling_float)

    def button_callback(self) -> None:
        # dialog = CustomDialog(self)
        print("Button clicked")
        # tkinter.messagebox.showinfo(
        #     title="Button",
        #     message="You clicked the button!",
        #     parent=self,
        #     icon="info",
        #     type="ok",
        #     detail="This is a detailed message",
        #     default="ok",
        # )


if __name__ == "__main__":
    app = App()
    app.mainloop()
