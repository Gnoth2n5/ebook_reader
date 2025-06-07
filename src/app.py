import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import flet as ft
from src.components.sidebar import Sidebar
from src.components.main_content import MainContent
from src.utils.data_manager import DataManager

EBOOK_DIR = "ebooks"
DATA_DIR = "data"


def main(page: ft.Page):
    page.title = "Modern Ebook Reader"
    page.bgcolor = "#FAFAFA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    }
    page.theme = ft.Theme(
        font_family="Inter",
        color_scheme_seed="#6366F1",
        use_material3=True
    )

    os.makedirs(EBOOK_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    data_manager = DataManager(os.path.join(DATA_DIR, "ebooks.json"))
    main_content = MainContent(data_manager)
    sidebar = Sidebar(data_manager, main_content)

    # Tạo FilePicker
    file_picker = ft.FilePicker(on_result=lambda e: sidebar.handle_file_picked(e))
    page.overlay.append(file_picker)

    # Header với gradient và shadow
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    name=ft.icons.MENU_BOOK_ROUNDED,
                    color="#FFFFFF",
                    size=28
                ),
                ft.Text(
                    "Modern Ebook Reader",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color="#FFFFFF"
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.ADD_ROUNDED, size=20),
                            ft.Text("Add Book", size=14, weight=ft.FontWeight.W_500)
                        ],
                        spacing=8,
                        tight=True
                    ),
                    on_click=lambda e: file_picker.pick_files(
                        allow_multiple=False, 
                        allowed_extensions=["txt", "epub"]
                    ),
                    bgcolor="#FFFFFF",
                    color="#6366F1",
                    elevation=0,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=20, vertical=12)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#6366F1", "#8B5CF6"]
        ),
        padding=ft.padding.symmetric(horizontal=32, vertical=20),
        shadow=ft.BoxShadow(
            blur_radius=8,
            color="#6366F1",
            offset=ft.Offset(0, 2),
            blur_style=ft.ShadowBlurStyle.OUTER
        )
    )

    # Main layout
    main_layout = ft.Container(
        content=ft.Row(
            controls=[
                sidebar.get_widget(),
                ft.VerticalDivider(width=1, color="#E5E7EB"),
                main_content.get_widget(),
            ],
            expand=True,
            spacing=0,
        ),
        expand=True,
        bgcolor="#FAFAFA"
    )

    page.add(
        ft.Column(
            controls=[
                header,
                main_layout,
            ],
            expand=True,
            spacing=0,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)