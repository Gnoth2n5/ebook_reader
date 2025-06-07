import os

import flet as ft

from src.utils.file_handler import FileHandler


class Sidebar:
    def __init__(self, data_manager, main_content):
        self.data_manager = data_manager
        self.main_content = main_content
        self.ebook_list = ft.ListView(expand=True)
        self.selected_menu = "all"
        self.widget = ft.Container(
            content=ft.Column(
                controls=self._build_menu(),
                expand=True,
            ),
            width=220,
            bgcolor="#1CDC11",
            padding=10,
        )
        self.update_ebook_list()

    def _build_menu(self):
        return [
            ft.Text("Thư viện", weight=ft.FontWeight.BOLD, size=18),
            ft.ListTile(
                leading=ft.Icon(name="book"),
                title=ft.Text(f"All ({self.data_manager.count_all()})"),
                selected=self.selected_menu == "all",
                on_click=lambda e: self._on_menu_select("all"),
            ),
            ft.ListTile(
                leading=ft.Icon(name="history"),
                title=ft.Text(
                    f"Recently Read ({self.data_manager.count_recently_read()})"
                ),
                selected=self.selected_menu == "recent",
                on_click=lambda e: self._on_menu_select("recent"),
            ),
        ]

    def _on_menu_select(self, menu):
        self.selected_menu = menu
        self.widget.content.controls = self._build_menu()
        self.update_ebook_list()
        self.widget.update()

    def get_widget(self):
        return self.widget

    def update_ebook_list(self):
        self.ebook_list.controls.clear()
        ebooks = self.data_manager.load_ebooks()
        if self.selected_menu == "all":
            filtered = [e for e in ebooks if not e.get("is_deleted")]
        elif self.selected_menu == "recent":
            import datetime

            now = datetime.datetime.now()
            filtered = []
            for e in ebooks:
                last_read = e.get("last_read")
                if last_read and not e.get("is_deleted"):
                    try:
                        dt = datetime.datetime.fromisoformat(last_read)
                        if (now - dt).days <= 7:
                            filtered.append(e)
                    except Exception:
                        pass
        elif self.selected_menu == "favorite":
            filtered = [
                e for e in ebooks if e.get("is_favorite") and not e.get("is_deleted")
            ]
        elif self.selected_menu == "read":
            filtered = [
                e for e in ebooks if e.get("is_read") and not e.get("is_deleted")
            ]
        elif self.selected_menu == "deleted":
            filtered = [e for e in ebooks if e.get("is_deleted")]
        else:
            filtered = [e for e in ebooks if not e.get("is_deleted")]
        for ebook in filtered:
            self.ebook_list.controls.append(
                ft.ListTile(
                    title=ft.Text(ebook.get("title", ebook.get("filename"))),
                    on_click=(
                        lambda name: lambda e: self.main_content.display_content(name)
                    )(ebook.get("filename")),
                )
            )

    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            file_name = os.path.basename(file_path)
            dest_path = os.path.join("ebooks", file_name)

            # Sao chép file
            FileHandler.copy_file(file_path, dest_path)

            # Cập nhật danh sách
            ebooks = self.data_manager.load_ebooks()
            if not any(e.get("filename") == file_name for e in ebooks):
                ebooks.append(
                    {
                        "filename": file_name,
                        "title": file_name,
                        "author": "Unknown",
                        "is_read": False,
                        "is_favorite": False,
                        "is_deleted": False,
                        "last_read": None,
                    }
                )
                self.data_manager.save_ebooks(ebooks)
                self.update_ebook_list()

            # Hiển thị nội dung
            self.main_content.display_content(file_name)
