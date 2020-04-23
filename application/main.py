import threading

from server import FSLServer, DEFAULT_SETTINGS
from server.settings import Settings
from gui import GUI


class FSLApp:
    def __init__(self):
        self.settings = Settings('.\\settings.json', DEFAULT_SETTINGS)
        self.server = FSLServer(self.settings)
        self.gui = GUI(self)
        self.prepare_threads()
        self.prepare_events()

    def prepare_threads(self):
        self.server_thread = threading.Thread(target=self.server.server_thread_runner, daemon=True)

    def prepare_events(self):
        self.server.events.on('post_plan', self.gui.main_window.pack_and_emit, self.gui.main_window.populate_plan)
        self.server.events.on('exporters_loaded', self.gui.main_window.pack_and_emit, self.gui.main_window.print_exporters)

    def start(self):
        self.server_thread.start()
        self.gui.start()


if __name__ == '__main__':
    FSL_APP = FSLApp()
    FSL_APP.start()
