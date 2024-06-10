import subprocess
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f'Arquivo criado: {event.src_path}')
        
        with open(event.src_path, 'r') as file:
            json_str = json.load(file)
            json_str = json.dumps(json_str)

        subprocess.run(["python", "src/main/initGen.py",json_str])

def monitor_folder(folder):
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_watch = r'src/JsonReciver'
    monitor_folder(folder_to_watch)


