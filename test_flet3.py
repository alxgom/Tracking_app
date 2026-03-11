import flet as ft
def main(p: ft.Page):
    dlg = ft.AlertDialog(title=ft.Text('hi'));
    try: p.open(dlg); print('success open')\n    except Exception as e: print('fail open:', e)
    try: p.close(dlg); print('success close')\n    except Exception as e: print('fail close:', e)
    p.window.destroy()
ft.run(main)
