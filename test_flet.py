import flet as ft

def main(page: ft.Page):
    with open("page_attrs.txt", "w") as f:
        f.write("\n".join(dir(page)))
    page.window.destroy()

ft.app(target=main)
