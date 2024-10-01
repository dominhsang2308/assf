import os
import shutil
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path
import datetime

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"Đã có thay đổi trong thư mục {event.src_path}")
            file_path = event.src_path
            if file_path.endswith('.crdownload') or file_path.endswith('.part'):
                print(f'tệp đang được tải xuống, :{file_path}')
                return
            if os.path.isfile(file_path):
                destination = get_location_folder(file_path)
                if destination:
                    move_file(file_path,destination)
                else:
                    print(f'Tệp không thuộc để phân loại:  {file_path}')


def get_current_date_folder():
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    return current_date

source_folder = str(Path.home()/ "Downloads")

def create_folders_by_date():
    current_date_folder = get_current_date_folder()
    folders = {
        'video': os.path.join(source_folder,'Video',current_date_folder),
        'pdf': os.path.join(source_folder,'PDF', current_date_folder),
        'image': os.path.join(source_folder,'Image',current_date_folder),
        'document': os.path.join(source_folder,'Document',current_date_folder ),
        'rar': os.path.join(source_folder,'Winrar',current_date_folder),
        'exe': os.path.join(source_folder, 'EXE',current_date_folder),
        'csv': os.path.join(source_folder,'CSV',current_date_folder)
    }
    return folders

def get_location_folder(filename):
    folders = create_folders_by_date()
    ext = filename.split('.')[-1].lower()
    if ext in ['mp4','mkv','mov']:
        return folders['video']
    elif ext in ['pdf']:
        return folders['pdf']
    elif ext in ['png','jpg','gif','jpeg']:
        return folders['image']
    elif ext in ['doc','docx','txt']:
        return folders['document']
    elif ext in ['rar']:
        return folders['rar']
    elif ext in ['exe']:
        return folders['exe']
    elif ext in ['csv']:
        return folders['csv']
    else:
        return source_folder
    
def move_file(file_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    filename = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, filename)

    if os.path.exists(destination_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = f"{base}_{counter}{ext}"
        new_destionation = os.path.join(destination_folder,new_filename)

        while os.path.exists(new_destionation):
            counter +=1
            new_filename = f"{base}_{counter}{ext}"
            new_destionation = os.path.join(destination_folder,new_filename)
        destination_path = new_destionation
    try:
        shutil.copy(file_path,destination_folder)
        print(f'Moved {file_path} -> {destination_path}')
    except Exception as e:
        print(f'Cannot move file {e}')

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_folder, recursive=False)
    
    observer.start()
    print(f"Đang theo dõi thư mục: {source_folder}") 

    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        observer.stop() 
        print("Đã dừng quan sát.")
    
    observer.join()

    
