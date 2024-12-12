import flet as ft


class SourceCode(ft.Text):
    def __init__(self, control):
        super().__init__()
        self.control = control
        # self.update_source_code(control)

    def did_mount(self):
        self.update_source_code(self.control)

    def update_source_code(self, control):
        text = ""
        # for property in self.properties:
        #     if type(getattr(self.control, property["name"])).__name__ == "str":
        #         property_value = f"""'{getattr(self.control, property["name"])}'"""
        #     else:
        #         property_value = getattr(self.control, property["name"])
        #     text = text + f"{property["name"]}={property_value}, "
        # control_name = type(self.control).__name__
        print(control)

        # code = f"""ft.{control_name}({text})"""
        # self.value = code
        self.update()


class PropertiesTable(ft.DataTable):
    def __init__(self, properties, control, parent=None):
        super().__init__(
            columns=[
                ft.DataColumn(ft.Text("Property name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(
                    ft.Text("Property value", weight=ft.FontWeight.BOLD, width=200)
                ),
            ]
        )
        if parent == None:
            self.parent = control
        else:
            self.parent = parent
        self.properties = properties
        self.control = control
        self.rows = self.get_rows()

        # self.source_code = ft.Text()

    # def did_mount(self):
    #     self.update_source_code()

    def update_source_code(self):
        text = ""
        for property in self.properties:
            if type(getattr(self.control, property["name"])).__name__ == "str":
                property_value = f"""'{getattr(self.control, property["name"])}'"""
            else:
                property_value = getattr(self.control, property["name"])
            text = text + f"{property["name"]}={property_value}, "
        control_name = type(self.control).__name__

        # code = f"""ft.{control_name}({text})"""
        # self.source_code.value = code
        # self.source_code.update()

    def get_rows(self):
        data_rows = []

        for property in self.properties:

            # print(
            #     f"Property type: {type(getattr(self.control, property["name"])).__name__}"
            # )
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(property["name"])),
                        ft.DataCell(
                            # self.get_value_control(
                            #     value_type=property["value_type"],
                            #     value=getattr(self.control, property["name"]),
                            #     data=property["name"],
                            # )
                            self.get_value_control(property)
                        ),
                    ],
                ),
            )
        return data_rows

    def value_changed(self, e):
        print("Value changed!")
        setattr(self.control, e.control.data, e.control.value)
        # self.update_source_code()
        self.parent.update()

    # def get_value_control(self, value_type, value, data):
    def get_value_control(self, property):
        value = getattr(self.control, property["name"])
        match property["value_type"]:
            case "str":
                return ft.TextField(
                    content_padding=3,
                    value=value,
                    data=property["name"],
                    # on_change=self.value_changed,
                )
            case "number":
                return ft.TextField(
                    content_padding=3,
                    value=value,
                    data=property["name"],
                    # on_change=self.value_changed,
                )
            case "bool":
                return ft.Checkbox(
                    value=value,
                    data=property["name"],
                    # on_change=self.value_changed,
                )
            case "enum":

                options = []

                options_list = property["values"]
                for item in options_list:
                    options.append(ft.dropdown.Option(item.value))

                return ft.Dropdown(
                    options=options,
                    value=value,
                    data=property["name"],
                    # on_change=self.value_changed,
                )

            case "dataclass":
                properties_dialog = ft.AlertDialog(
                    title=ft.Text(f"{property["name"].capitalize()} properties"),
                    content=PropertiesTable(
                        properties=property["properties"],
                        control=value,
                    ),
                )

                def open_dlg(e):
                    e.control.page.open(properties_dialog)

                return ft.Button(text="...", on_click=open_dlg)

            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                return ft.Text("Something's wrong with the type")


class PropertiesList(ft.ListView):
    def __init__(self, properties, control, top_control=None):
        super().__init__()
        self.properties = properties
        self.control = control
        self.divider_thickness = 3
        self.width = 500
        if top_control == None:
            self.top_control = control
        else:
            self.top_control = top_control
        # self.expanded_icon_color = ft.Colors.AMBER
        # self.elevation = 8
        # self.divider_color = ft.colors.PRIMARY
        self.controls = self.get_properties_controls()

    def get_properties_controls(self):
        controls = []

        for property in self.properties:
            value = getattr(self.control, property["name"])
            if property["value_type"] == "dataclass":
                property_value = ""
                controls.append(
                    ft.ExpansionTile(
                        bgcolor=ft.Colors.OUTLINE_VARIANT,
                        title=ft.Text(property["name"]),
                        controls=[
                            PropertiesList(
                                properties=property["properties"],
                                control=value,
                                top_control=self.top_control,
                            )
                        ],
                    )
                )
            else:
                controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                        margin=5,
                        padding=5,
                        border_radius=3,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(property["name"]),
                                self.get_value_control(property),
                            ],
                        ),
                    )
                )

        return controls

    def value_changed(self, e):
        print(f"Control: {self.control}!")
        print(f"Top Control: {self.top_control}!")
        print(f"Property: {e.control.data}!")

        print(f"Value: {e.control.value}!")
        setattr(self.control, e.control.data, e.control.value)
        # update
        # if self.control != self.top_control:
        #     setattr(self.top_control, e.control.data, self.control)
        # self.update_source_code()
        # self.control.update()
        self.top_control.update()

    def get_value_control(self, property):

        value = getattr(self.control, property["name"])
        match property["value_type"]:
            case "str":
                return ft.TextField(
                    border_color=ft.Colors.SECONDARY,
                    content_padding=3,
                    value=value,
                    data=property["name"],
                    on_change=self.value_changed,
                )
            case "number":
                return ft.TextField(
                    border_color=ft.Colors.SECONDARY,
                    content_padding=3,
                    value=value,
                    data=property["name"],
                    on_change=self.value_changed,
                )
            case "bool":
                return ft.Checkbox(
                    value=value,
                    data=property["name"],
                    on_change=self.value_changed,
                )
            case "enum":

                options = []

                options_list = property["values"]
                for item in options_list:
                    options.append(ft.dropdown.Option(item.value))

                return ft.Dropdown(
                    options=options,
                    value=value,
                    data=property["name"],
                    on_change=self.value_changed,
                )

            case "dataclass":

                properties_list = PropertiesList(
                    properties=property["properties"], control=value
                )

                return properties_list

            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                return ft.Text("Something's wrong with the type")