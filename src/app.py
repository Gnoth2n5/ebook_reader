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
    page.title = "Ebook Reader"
    page.bgcolor = "#2650D7"

    os.makedirs(EBOOK_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    data_manager = DataManager(os.path.join(DATA_DIR, "ebooks.json"))
    main_content = MainContent(data_manager)
    sidebar = Sidebar(data_manager, main_content)

    # Tạo FilePicker
    file_picker = ft.FilePicker(on_result=lambda e: sidebar.handle_file_picked(e))
    page.overlay.append(file_picker)

    page.add(
        ft.Row(
            controls=[
                sidebar.get_widget(),
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            "Chọn file",
                            on_click=lambda e: file_picker.pick_files(
                                allow_multiple=False, allowed_extensions=["txt", "epub"]
                            ),
                        ),
                        main_content.get_widget(),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
