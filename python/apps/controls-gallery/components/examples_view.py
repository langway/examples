import flet as ft


class ExamplesView(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery
        self.visible = False
        self.expand = True
        self.control_name_text = ft.Text(theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
        self.control_description = ft.Text(theme_style=ft.TextThemeStyle.BODY_MEDIUM)
        self.examples = ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)
        self.controls = [
            self.control_name_text,
            self.control_description,
            self.examples,
        ]

    def display(self, grid_item):
        self.visible = True
        self.examples.controls = []
        self.control_name_text.value = grid_item.name
        self.control_description.value = grid_item.description

        # for example in grid_item.examples:
        #     self.examples.controls.append(
        #         ft.Column(
        #             controls=[
        #                 ft.Container(
        #                     content=ft.Row(
        #                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        #                         controls=[
        #                             ft.Text(
        #                                 example.name,
        #                                 theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
        #                                 weight=ft.FontWeight.W_500,
        #                             ),
        #                             ft.IconButton(
        #                                 content=ft.Image(
        #                                     src="github-mark.svg",
        #                                     width=24,
        #                                     height=24,
        #                                     color=ft.Colors.ON_SURFACE,
        #                                 ),
        #                                 url=f"https://github.com/flet-dev/examples/blob/main/python/apps/controls-gallery/examples/{example.file_name}",
        #                                 url_target=ft.UrlTarget.BLANK,
        #                             ),
        #                         ],
        #                     ),
        #                     bgcolor=ft.Colors.SECONDARY_CONTAINER,
        #                     padding=5,
        #                     border_radius=5,
        #                 ),
        #                 ft.Container(
        #                     content=example.example(),
        #                     clip_behavior=ft.ClipBehavior.NONE,
        #                 ),
        #             ],
        #         )
        #     )

        for example in grid_item.examples:
            self.examples.controls.append(
                ft.Tabs(
                    selected_index=0,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="视图",
                            tab_content=ft.Icon(ft.Icons.VIEW_DAY),
                            content=self.get_controls_view(example),
                        ),
                        ft.Tab(
                            text="代码",
                            tab_content=ft.Icon(ft.Icons.CODE),
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Markdown(
                                            f"```python\r\n{example.source_code}\r\n```",
                                            # example.source_code,
                                            selectable=True,
                                            code_theme=ft.MarkdownCodeTheme.GITHUB,
                                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                            # on_tap_link=lambda e: page.launch_url(e.data),
                                        ),
                                        # clip_behavior=ft.ClipBehavior.NONE,
                                    ),
                                ],
                            ),
                            # content=ft.Markdown(example.source_code),
                        ),
                    ],
                    expand=1,
                ),

            )

    def get_controls_view(self, example):
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                example.name,
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.IconButton(
                                content=ft.Image(
                                    src="github-mark.svg",
                                    width=24,
                                    height=24,
                                    color=ft.Colors.ON_SURFACE,
                                ),
                                url=f"https://github.com/flet-dev/examples/blob/main/python/apps/controls-gallery/examples/{example.file_name}",
                                url_target=ft.UrlTarget.BLANK,
                            ),
                        ],
                    ),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    padding=5,
                    border_radius=5,
                ),
                ft.Container(
                    content=example.example(),
                    clip_behavior=ft.ClipBehavior.NONE,
                ),
            ],
        )
