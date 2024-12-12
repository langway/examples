import flet as ft

from components.properties_table import PropertiesList, PropertiesTable, SourceCode

name = "Text with variable properties"


def example():

    t = ft.Text(
        value="This is a sample text",
        italic=True,
        selectable=True,
        size=20,
        # color=ft.Colors.GREEN_800,
        bgcolor=ft.Colors.GREEN_100,
        max_lines=2,
        style=ft.TextStyle(
            size=30,
            shadow=ft.BoxShadow(
                spread_radius=5, blur_radius=10, color=ft.Colors.ORANGE
            ),
            foreground=ft.Paint(
                color=ft.Colors.BLUE_400, blend_mode=ft.BlendMode.COLOR_BURN
            ),
        ),
    )

    paint_properties_list = [
        {"name": "color", "value_type": "enum", "values": ft.Colors},
    ]

    shadow_properties_list = [
        {
            "name": "spread_radius",
            "value_type": "number",
        },
        {
            "name": "blur_radius",
            "value_type": "number",
        },
        {"name": "color", "value_type": "enum", "values": ft.Colors},
    ]

    style_properties_list = [
        {"name": "size", "value_type": "number"},
        {"name": "letter_spacing", "value_type": "number"},
        {
            "name": "foreground",
            "value_type": "dataclass",
            "properties": paint_properties_list,
        },
        {
            "name": "shadow",
            "value_type": "dataclass",
            "properties": shadow_properties_list,
        },
    ]

    properties_list = [
        {
            "name": "value",
            "value_type": "str",
        },
        {"name": "italic", "value_type": "bool"},
        {"name": "selectable", "value_type": "bool"},
        {"name": "size", "value_type": "number"},
        {"name": "color", "value_type": "enum", "values": ft.Colors},
        {"name": "bgcolor", "value_type": "enum", "values": ft.Colors},
        {"name": "max_lines", "value_type": "number"},
        {
            "name": "style",
            "value_type": "dataclass",
            # "dataclass": ft.TextStyle,
            "properties": style_properties_list,
        },
    ]

    # properties = PropertiesTable(properties_list, t)

    properties = PropertiesList(properties=properties_list, control=t)

    # source_code = ft.Text(value=get_source_code(), selectable=True)
    # source_code = properties.source_code

    # source_code = SourceCode(t)

    example_control = ft.Column(
        controls=[
            t,
            properties,
            ft.Text("Source code:", weight=ft.FontWeight.BOLD),
            # source_code,
        ]
    )

    return example_control