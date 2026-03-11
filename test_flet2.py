import flet as ft, asyncio
class Test(ft.Container):
    def did_mount(self): asyncio.create_task(self.run())
    async def run(self): pass
def main(page): page.add(Test())
ft.run(main)
