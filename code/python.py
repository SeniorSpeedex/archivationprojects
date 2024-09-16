import os
import zipfile
try:
    import py7zr
except ImportError:
    py7zr = None
from tkinter import filedialog, Tk, StringVar, OptionMenu, Button, Label, Entry, Listbox, mainloop

def create_archive(file_paths, archive_path, archive_type):
    try:
        if archive_type == ".zip":
            with zipfile.ZipFile(archive_path, "w") as zip_archive:
                for file_path in file_paths:
                    zip_archive.write(file_path, os.path.basename(file_path))
        elif archive_type == ".7z":
            if py7zr:
                with py7zr.SevenZipFile(archive_path, "w") as sz_archive:
                    for file_path in file_paths:
                        sz_archive.write(file_path, os.path.basename(file_path))
            else:
                print("Для работы с 7z-архивами необходима библиотека 'py7zr'.")
                return
        else:
            print(f"Неподдерживаемый тип архива: {archive_type}")
            return
        print(f"Архив '{archive_path}' успешно создан.")
    except Exception as e:
        print(f"Ошибка при создании архива: {e}")

def main():
    root = Tk()
    root.title("Архиватор файлов")

    # Выбор файлов для архивирования
    def choose_files():
        file_paths = filedialog.askopenfilenames(title="Выберите файлы для архивирования")
        file_list.delete(0, "end")
        for file_path in file_paths:
            file_list.insert("end", os.path.basename(file_path))

    # Выбор директории для сохранения архива
    def choose_directory():
        archive_dir = filedialog.askdirectory(title="Выберите папку для сохранения архива")
        archive_path_entry.delete(0, "end")
        archive_path_entry.insert(0, archive_dir)

    # Создание архива
    def create_archive_wrapper():
        file_paths = [os.path.join(archive_path_entry.get(), f) for f in file_list.get(0, "end")]
        archive_type = archive_type_var.get()
        archive_name = archive_name_entry.get()
        if archive_name:
            archive_path = os.path.join(archive_path_entry.get(), f"{archive_name}{archive_type}")
            create_archive(file_paths, archive_path, archive_type)
        else:
            print("Пожалуйста, введите имя архива.")

    # Интерфейс
    file_list = Listbox(root, width=50)
    file_list.grid(row=0, column=0, padx=10, pady=10)

    archive_type_var = StringVar()
    archive_type_var.set(".zip")
    archive_type_dropdown = OptionMenu(root, archive_type_var, ".zip", ".7z")
    archive_type_dropdown.grid(row=1, column=0, padx=10, pady=10)

    archive_path_label = Label(root, text="Путь для сохранения:")
    archive_path_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    archive_path_entry = Entry(root, width=50)
    archive_path_entry.grid(row=3, column=0, padx=10, pady=5)

    archive_name_label = Label(root, text="Имя архива:")
    archive_name_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    archive_name_entry = Entry(root, width=50)
    archive_name_entry.grid(row=5, column=0, padx=10, pady=5)

    choose_files_button = Button(root, text="Выбрать файлы", command=choose_files)
    choose_files_button.grid(row=6, column=0, padx=10, pady=10)

    choose_directory_button = Button(root, text="Выбрать папку", command=choose_directory)
    choose_directory_button.grid(row=7, column=0, padx=10, pady=10)

    create_archive_button = Button(root, text="Создать архив", command=create_archive_wrapper)
    create_archive_button.grid(row=8, column=0, padx=10, pady=10)

    mainloop()

if __name__ == "__main__":
    main()
