import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    DIRECTORY_TO_WATCH = "."
    
    def __init__(self):
        self.observer = Observer()
        self.flask_process = None

    def run(self):
        event_handler = Handler(self)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        self.start_flask_app()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            self.stop_flask_app()
        self.observer.join()

    def start_flask_app(self):
        if self.flask_process:
            self.flask_process.kill()
        self.flask_process = subprocess.Popen([sys.executable, 'app.py'])

    def stop_flask_app(self):
        if self.flask_process:
            self.flask_process.kill()
            self.flask_process = None

class Handler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            # Restart the Flask app
            print(f"Detected changes in {event.src_path}. Restarting the server...")
            self.watcher.start_flask_app()

if __name__ == '__main__':
    watcher = Watcher()
    watcher.run()
