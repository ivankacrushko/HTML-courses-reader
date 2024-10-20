import http.server
import socketserver
import webbrowser
import os
import threading

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def list_folders(path):
    try:
        with os.scandir(path) as entries:
            folders = [entry.name for entry in entries if entry.is_dir()]
            return folders
    except FileNotFoundError:
        print(f"Ścieżka {path} nie istnieje.")
        return []

def choose_folder(folders):
    if not folders:
        print("Nie znaleziono żadnych folderów.")
        return None

    print("Dostępne foldery:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")

    while True:
        try:
            choice = int(input("Wybierz numer folderu: "))
            if 1 <= choice <= len(folders):
                return folders[choice - 1]
            else:
                print("Niepoprawny numer, spróbuj ponownie.")
        except ValueError:
            print("Proszę podać numer folderu.")

def start_server(site_path):
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        webbrowser.open(f"http://localhost:{PORT}/{site_path}")
        httpd.serve_forever()

def main():
    global PORT
    PORT = 8000
    directory_path = "./Wyklady/"

    while True:
        folders = list_folders(directory_path)
        selected_folder = choose_folder(folders)
        file_path = os.path.join(directory_path, selected_folder, 'html')
        os.system('cls')
        server_thread = threading.Thread(target=start_server, args=(file_path,), daemon=True)
        server_thread.start()

        while True:
            a = input("Aby uruchomic inna prezentacje wylacz, a nastepnie uruchom aplikacje ponownie")

if __name__ == "__main__":
    main()
