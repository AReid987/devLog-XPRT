
from PIL import Image as PILImage
from pocketbase import PocketBase
from pocketbase.models.record import Record
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Image, RichLog


class LogScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]
    def __init__(self, pb: PocketBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb = pb
        self.logs: list[Record] = []
        self.log_widget = RichLog()

    async def on_mount(self) -> None:
        await self.load_logs()

    async def load_logs(self):
        try:
            collection = await self.pb.collection("logs").get_full_list(sort="-created")
            self.logs = collection
            for log in self.logs:
                self.log_widget.write(f"[{log.get('level')}] {log.get('message')}")
        except Exception as e:
            self.log_widget.write(f"Error loading logs: {e}")

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.log_widget
        yield Footer()

class GifScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]
    def __init__(self, gif_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gif_path = gif_path
        self.gif_widget = Image.from_file(gif_path)

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.gif_widget
        yield Footer()

class TrajectoryScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]
    def __init__(self, pb: PocketBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb = pb
        self.trajectories: list[Record] = []
        self.log_widget = RichLog()

    async def on_mount(self) -> None:
        await self.load_trajectories()

    async def load_trajectories(self):
        try:
            collection = await self.pb.collection("trajectories").get_full_list(sort="-created")
            self.trajectories = collection
            for trajectory in self.trajectories:
                self.log_widget.write(f"{trajectory.get('data')}")
        except Exception as e:
            self.log_widget.write(f"Error loading trajectories: {e}")

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.log_widget
        yield Footer()

class ScreenshotScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back")
    ]

    def __init__(self, image_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_path = image_path
        self.image_widget = PILImage.from_file(image_path)

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.image_widget
        yield Footer()

class ProxyLiteApp(App):
    CSS_PATH = "tui.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("l", "view_logs", "View Logs"),
        Binding("g", "view_gifs", "View Gifs"),
        Binding("t", "view_trajectories", "View Trajectories"),
        Binding("s", "view_screenshots", "View Screenshots"),
    ]

    def __init__(self, pb: PocketBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb = pb

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_view_logs(self) -> None:
        self.push_screen(LogScreen(self.pb))

    def action_view_gifs(self) -> None:
        self.push_screen(GifScreen("/packages/proxy-lite/gifs/demo.gif"))

    def action_view_trajectories(self) -> None:
        self.push_screen(TrajectoryScreen(self.pb))

    def action_view_screenshots(self) -> None:
        self.push_screen(ScreenshotScreen("/packages/proxy-lite/screenshots/screenshot.png"))

async def run_tui(pb: PocketBase):
    app = ProxyLiteApp(pb)
    await app.run()