import flet as ft
import os
from src.utils.file_handler import FileHandler

# Modern color palette
COLORS = {
    "primary": "#6366F1",
    "primary_light": "#A5B4FC",
    "secondary": "#8B5CF6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",
    "white": "#FFFFFF",
}

GRADIENTS = [
    [COLORS["primary"], COLORS["secondary"]],
    ["#F59E0B", "#EF4444"],
    [COLORS["success"], "#059669"],
    ["#3B82F6", COLORS["primary"]],
    ["#8B5CF6", "#EC4899"],
    ["#06B6D4", COLORS["success"]],
]


class MainContent:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.selected_ebook = None
        self.content = ft.Text("Select a book to start reading", selectable=True, color=COLORS["gray_600"])
        self.grid = ft.GridView(
            expand=True,
            runs_count=4,
            max_extent=280,
            child_aspect_ratio=0.75,
            spacing=24,
            run_spacing=24,
        )
        self.widget = ft.Container(
            content=self._build_empty_state(),
            bgcolor=COLORS["gray_50"],
            expand=True,
            padding=ft.padding.all(32),
        )
        self.update_grid()

    def _build_empty_state(self):
        return ft.Column(
            controls=[
                ft.Icon(
                    name=ft.icons.MENU_BOOK_OUTLINED,
                    size=80,
                    color=COLORS["gray_300"]
                ),
                ft.Text(
                    "Your Library is Empty",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["gray_700"],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Add your first book to get started with reading",
                    size=16,
                    color=COLORS["gray_500"],
                    text_align=ft.TextAlign.CENTER
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            spacing=16
        )

    def get_widget(self):
        return self.widget

    def update_grid(self):
        self.grid.controls.clear()
        ebooks = [e for e in self.data_manager.load_ebooks() if not e.get("is_deleted")]
        
        if not ebooks:
            self.widget.content = self._build_empty_state()
            self.widget.update()
            return

        for idx, ebook in enumerate(ebooks):
            gradient = GRADIENTS[idx % len(GRADIENTS)]
            is_read = ebook.get("is_read", False)
            is_favorite = ebook.get("is_favorite", False)
            
            # Book cover with gradient
            book_cover = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                name=ft.icons.MENU_BOOK_ROUNDED,
                                size=48,
                                color=COLORS["white"]
                            ),
                            alignment=ft.alignment.center,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        name=ft.icons.FAVORITE if is_favorite else ft.icons.FAVORITE_BORDER,
                                        size=16,
                                        color=COLORS["white"]
                                    ),
                                    ft.Container(expand=True),
                                    ft.Icon(
                                        name=ft.icons.CHECK_CIRCLE if is_read else ft.icons.RADIO_BUTTON_UNCHECKED,
                                        size=16,
                                        color=COLORS["white"]
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=ft.padding.all(12)
                        )
                    ],
                    spacing=0
                ),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=gradient,
                ),
                border_radius=16,
                width=200,
                height=280,
                shadow=ft.BoxShadow(
                    blur_radius=20,
                    color=gradient[0] + "40",
                    offset=ft.Offset(0, 8),
                    blur_style=ft.ShadowBlurStyle.OUTER
                ),
            )

            # Book info
            book_info = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            ebook.get("title", ebook.get("filename", "").replace('.txt', '').replace('.epub', '')),
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=COLORS["gray_800"],
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            ebook.get("author", "Unknown Author"),
                            size=14,
                            color=COLORS["gray_500"],
                            text_align=ft.TextAlign.CENTER,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            "Completed" if is_read else "Reading",
                                            size=12,
                                            weight=ft.FontWeight.W_500,
                                            color=COLORS["success"] if is_read else COLORS["primary"]
                                        ),
                                        bgcolor=COLORS["success"] + "20" if is_read else COLORS["primary"] + "20",
                                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        border_radius=8,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            margin=ft.margin.only(top=8)
                        )
                    ],
                    spacing=6,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True
                ),
                padding=ft.padding.only(top=16)
            )

            # Complete card
            card = ft.Container(
                content=ft.Column(
                    controls=[book_cover, book_info],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    tight=True
                ),
                bgcolor=COLORS["white"],
                border_radius=20,
                padding=ft.padding.all(16),
                ink=True,
                on_click=(lambda filename: lambda e: self.display_content(filename))(
                    ebook.get("filename")
                ),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                on_hover=self._on_card_hover,
                shadow=ft.BoxShadow(
                    blur_radius=12,
                    color=COLORS["gray_200"],
                    offset=ft.Offset(0, 4),
                    blur_style=ft.ShadowBlurStyle.OUTER
                )
            )
            self.grid.controls.append(card)

        self.widget.content = self.grid
        self.widget.update()

    def _on_card_hover(self, e):
        if e.data == "true":
            e.control.scale = 1.02
            e.control.shadow = ft.BoxShadow(
                blur_radius=20,
                color=COLORS["primary"] + "30",
                offset=ft.Offset(0, 8),
                blur_style=ft.ShadowBlurStyle.OUTER
            )
        else:
            e.control.scale = 1.0
            e.control.shadow = ft.BoxShadow(
                blur_radius=12,
                color=COLORS["gray_200"],
                offset=ft.Offset(0, 4),
                blur_style=ft.ShadowBlurStyle.OUTER
            )
        e.control.update()

    def display_content(self, file_name):
        content = FileHandler.read_file(os.path.join("ebooks", file_name))
        
        # Update last_read timestamp
        ebooks = self.data_manager.load_ebooks()
        for ebook in ebooks:
            if ebook.get("filename") == file_name:
                import datetime
                ebook["last_read"] = datetime.datetime.now().isoformat()
                break
        self.data_manager.save_ebooks(ebooks)
        
        # Reader header
        reader_header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK_ROUNDED,
                        icon_color=COLORS["primary"],
                        icon_size=24,
                        on_click=lambda e: self.show_grid(),
                        tooltip="Back to Library"
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                file_name.replace('.txt', '').replace('.epub', ''),
                                size=20,
                                weight=ft.FontWeight.W_600,
                                color=COLORS["gray_800"],
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),
                            ft.Text(
                                "Reading Mode",
                                size=14,
                                color=COLORS["gray_500"]
                            )
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.BOOKMARK_BORDER_ROUNDED,
                                icon_color=COLORS["gray_500"],
                                tooltip="Bookmark"
                            ),
                            ft.IconButton(
                                icon=ft.icons.SETTINGS_ROUNDED,
                                icon_color=COLORS["gray_500"],
                                tooltip="Reading Settings"
                            ),
                        ],
                        spacing=4
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=COLORS["white"],
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            border=ft.border.only(bottom=ft.BorderSide(1, COLORS["gray_200"]))
        )

        # Reader content
        reader_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            content,
                            selectable=True,
                            size=16,
                            color=COLORS["gray_700"],
                            text_align=ft.TextAlign.JUSTIFY,
                        ),
                        padding=ft.padding.all(32),
                        bgcolor=COLORS["white"],
                        border_radius=16,
                        margin=ft.margin.all(24),
                        shadow=ft.BoxShadow(
                            blur_radius=8,
                            color=COLORS["gray_200"],
                            offset=ft.Offset(0, 2),
                            blur_style=ft.ShadowBlurStyle.OUTER
                        )
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            expand=True,
            bgcolor=COLORS["gray_50"]
        )

        self.widget.content = ft.Column(
            controls=[reader_header, reader_content],
            spacing=0,
            expand=True
        )
        self.widget.update()

    def show_grid(self):
        self.update_grid()