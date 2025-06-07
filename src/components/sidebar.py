import os
import flet as ft
from src.utils.file_handler import FileHandler


class Sidebar:
    def __init__(self, data_manager, main_content):
        self.data_manager = data_manager
        self.main_content = main_content
        self.ebook_list = ft.ListView(expand=True, spacing=4)
        self.selected_menu = "all"
        self.widget = ft.Container(
            content=ft.Column(
                controls=self._build_menu(),
                expand=True,
                spacing=8,
            ),
            width=280,
            bgcolor="#FFFFFF",
            padding=ft.padding.all(20),
        )
        self.update_ebook_list()

    def _build_menu(self):
        menu_items = [
            {
                "key": "all",
                "icon": ft.icons.LIBRARY_BOOKS_ROUNDED,
                "title": "All Books",
                "count": self.data_manager.count_all()
            },
            {
                "key": "recent",
                "icon": ft.icons.HISTORY_ROUNDED,
                "title": "Recently Read",
                "count": self.data_manager.count_recently_read()
            },
            {
                "key": "read",
                "icon": ft.icons.CHECK_CIRCLE_ROUNDED,
                "title": "Completed",
                "count": self.data_manager.count_read()
            },
            {
                "key": "favorite",
                "icon": ft.icons.FAVORITE_ROUNDED,
                "title": "Favorites",
                "count": self.data_manager.count_favorite()
            }
        ]

        controls = [
            ft.Container(
                content=ft.Text(
                    "Library",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#1F2937"
                ),
                margin=ft.margin.only(bottom=16)
            )
        ]

        for item in menu_items:
            is_selected = self.selected_menu == item["key"]
            
            menu_tile = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            name=item["icon"],
                            color="#6366F1" if is_selected else "#6B7280",
                            size=20
                        ),
                        ft.Text(
                            item["title"],
                            size=14,
                            weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.W_400,
                            color="#1F2937" if is_selected else "#6B7280",
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Text(
                                str(item["count"]),
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color="#FFFFFF" if is_selected else "#6B7280"
                            ),
                            bgcolor="#6366F1" if is_selected else "#F3F4F6",
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                        )
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#F0F4FF" if is_selected else "transparent",
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                ink=True,
                on_click=lambda e, key=item["key"]: self._on_menu_select(key),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )
            controls.append(menu_tile)

        controls.extend([
            ft.Divider(height=1, color="#E5E7EB", thickness=1),
            ft.Container(
                content=ft.Text(
                    "Books",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color="#1F2937"
                ),
                margin=ft.margin.only(top=16, bottom=8)
            ),
            ft.Container(
                content=self.ebook_list,
                expand=True
            )
        ])

        return controls

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
        else:
            filtered = [e for e in ebooks if not e.get("is_deleted")]

        for ebook in filtered:
            book_tile = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            ebook.get("title", ebook.get("filename")),
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color="#1F2937",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Text(
                            ebook.get("author", "Unknown Author"),
                            size=12,
                            color="#6B7280",
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name=ft.icons.CHECK_CIRCLE if ebook.get("is_read") else ft.icons.RADIO_BUTTON_UNCHECKED,
                                    color="#10B981" if ebook.get("is_read") else "#D1D5DB",
                                    size=16
                                ),
                                ft.Text(
                                    "Completed" if ebook.get("is_read") else "In Progress",
                                    size=11,
                                    color="#10B981" if ebook.get("is_read") else "#6B7280"
                                )
                            ],
                            spacing=4,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    spacing=4,
                    tight=True
                ),
                bgcolor="transparent",
                border_radius=8,
                padding=ft.padding.all(12),
                ink=True,
                on_click=(lambda name: lambda e: self.main_content.display_content(name))(
                    ebook.get("filename")
                ),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                on_hover=self._on_book_hover,
                border=ft.border.all(1, "#E5E7EB")
            )
            self.ebook_list.controls.append(book_tile)

    def _on_book_hover(self, e):
        if e.data == "true":
            e.control.bgcolor = "#F9FAFB"
            e.control.border = ft.border.all(1, "#6366F1")
        else:
            e.control.bgcolor = "transparent"
            e.control.border = ft.border.all(1, "#E5E7EB")
        e.control.update()

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
                        "title": file_name.replace('.txt', '').replace('.epub', ''),
                        "author": "Unknown Author",
                        "is_read": False,
                        "is_favorite": False,
                        "is_deleted": False,
                        "last_read": None,
                    }
                )
                self.data_manager.save_ebooks(ebooks)
                self.update_ebook_list()
                self.main_content.update_grid()

            # Hiển thị nội dung
            self.main_content.display_content(file_name)