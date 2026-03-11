import flet as ft
def main(page: ft.Page):
    print("Has open?", hasattr(page, 'open'))
    print("Has show_dialog?", hasattr(page, 'show_dialog'))
    print("Has dialog property?", hasattr(page, 'dialog'))
    try:
        page.dialog = ft.AlertDialog(title=ft.Text("Hi"))
        print("Set page.dialog!")
    except Exception as e:
        print("Cannot set page.dialog:", e)
    page.window.destroy()

ft.run(main)
