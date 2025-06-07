import flet as ft
import os
from src.utils.file_handler import FileHandler

# Màu sắc dịu, hiện đại
BG_COLOR = "#F6F7FB"  # Nền tổng thể
SIDEBAR_COLOR = "#F2F3F7"  # Sidebar
CARD_GRADIENTS = [
    ["#E53935", "#B71C1C"],  # Đỏ
    ["#FB8C00", "#E65100"],  # Cam
    ["#43A047", "#558B2F"],  # Xanh lá
    ["#1E88E5", "#1565C0"],  # Xanh dương
    ["#8E24AA", "#4A148C"],  # Tím
]
PROGRESS_COLOR = "#7C4DFF"  # Tím nhạt
PROGRESS_BG = "#E0E0E0"
CARD_TEXT_COLOR = "#fff"
CARD_SHADOW = "#D1C4E9"
CARD_BORDER_RADIUS = 18


class MainContent:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.selected_ebook = None
        self.content = ft.Text("Chọn một truyện để đọc", selectable=True, color="#333")
        self.grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=320,
            child_aspect_ratio=0.7,
            spacing=32,
            run_spacing=32,
        )
        self.widget = ft.Container(
            content=self.grid,
            bgcolor=BG_COLOR,
            expand=True,
            padding=40,
        )
        self.update_grid()

    def get_widget(self):
        return self.widget

    def update_grid(self):
        self.grid.controls.clear()
        ebooks = [e for e in self.data_manager.load_ebooks() if not e.get("is_deleted")]
        for idx, ebook in enumerate(ebooks):
            gradient = CARD_GRADIENTS[idx % len(CARD_GRADIENTS)]
            is_read = ebook.get("is_read")
            progress_value = 1.0 if is_read else 0.0
            progress_color = PROGRESS_COLOR if is_read else "#BDBDBD"
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        ebook.get("title", ebook.get("filename")),
                                        weight=ft.FontWeight.BOLD,
                                        size=20,
                                        max_lines=3,
                                        overflow="ellipsis",
                                        text_align="center",
                                        color=CARD_TEXT_COLOR,
                                    ),
                                    ft.Text(
                                        ebook.get("author", "Unknown"),
                                        italic=True,
                                        size=14,
                                        color=CARD_TEXT_COLOR,
                                        text_align="center",
                                    ),
                                    ft.Container(
                                        content=ft.ProgressBar(
                                            value=progress_value,
                                            width=200,
                                            color=progress_color,
                                            bgcolor=PROGRESS_BG,
                                            bar_height=8,
                                        ),
                                        margin=ft.margin.only(top=16),
                                    ),
                                    ft.Text(
                                        f"{'Đã đọc' if is_read else 'Chưa đọc'}",
                                        size=12,
                                        color=CARD_TEXT_COLOR,
                                        text_align="center",
                                    ),
                                ],
                                alignment="center",
                                horizontal_alignment="center",
                            ),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_center,
                                end=ft.alignment.bottom_center,
                                colors=gradient,
                            ),
                            border_radius=CARD_BORDER_RADIUS,
                            padding=20,
                            width=260,
                            height=200,
                            shadow=ft.BoxShadow(
                                blur_radius=12,
                                color=CARD_SHADOW,
                                offset=ft.Offset(2, 4),
                            ),
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        ebook.get("title", ebook.get("filename")),
                                        size=14,
                                        max_lines=1,
                                        overflow="ellipsis",
                                        color="#333",
                                        text_align="center",
                                    ),
                                    ft.Text(
                                        ebook.get("author", "Unknown"),
                                        size=12,
                                        color="#888",
                                        text_align="center",
                                    ),
                                ],
                                alignment="center",
                                horizontal_alignment="center",
                            ),
                            margin=ft.margin.only(top=8),
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                ),
                border_radius=CARD_BORDER_RADIUS,
                ink=True,
                on_click=(lambda filename: lambda e: self.display_content(filename))(
                    ebook.get("filename")
                ),
                animate=ft.Animation(200, "easeInOut"),
                on_hover=lambda e: self._on_card_hover(e),
            )
            self.grid.controls.append(card)
        self.widget.content = self.grid

    def _on_card_hover(self, e):
        if e.data == "true":
            e.control.opacity = 0.92
        else:
            e.control.opacity = 1
        e.control.update()

    def display_content(self, file_name):
        content = FileHandler.read_file(os.path.join("ebooks", file_name))
        self.content.value = content
        self.widget.content = ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(
                        "Quay lại thư viện",
                        on_click=lambda e: self.show_grid(),
                        bgcolor="#7C4DFF",
                        color="#fff",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                    ft.Text(
                        file_name, weight=ft.FontWeight.BOLD, size=18, color="#7C4DFF"
                    ),
                    ft.Divider(),
                    ft.Text(
                        self.content.value,
                        selectable=True,
                        expand=True,
                        size=16,
                        color="#222",
                    ),
                ],
                expand=True,
            ),
            bgcolor="#fff",
            expand=True,
            padding=30,
            border_radius=16,
        )
        self.widget.update()

    def show_grid(self):
        self.widget.content = self.grid
        self.widget.update()
