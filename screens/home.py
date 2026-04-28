from app import BaseScreen


class HomeScreen(BaseScreen):
    def on_enter(self, *args):
        super().on_enter(*args)
        if self.manager and hasattr(self.manager, "set_selected_demo"):
            self.manager.set_selected_demo("Home")

    def open_demo(self, screen_name, label):
        self.record_event(f"Opening {label} sample.", selected_demo=label)
        self.go_to(screen_name)

    def clear_status(self):
        self.record_event("Dashboard reset. Pick another sample.", selected_demo="Home")
