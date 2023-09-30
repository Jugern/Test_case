import tkinter as tk
import csv
from datetime import datetime
from request_test import WorkRequest
from create_csv import Create_CSV_File
from selenium_test import SeleniumStart
from tkinter import filedialog


class TkinterParser():

    def __init__(self):
        self.root = tk.Tk()
        self.method_var = tk.StringVar()
        self.method_var.set("requests")  # Устанавливаем метод "requests" по умолчанию
        self.create_widgets()
        self.file_path = ''
        self.save_path = ''

    # Создание виджетов
    def create_widgets(self):
        file_button = tk.Button(self.root, text="Выбрать файл", command=self.open_file)
        file_button.pack(pady=10)
        save_button = tk.Button(self.root, text="Выбрать путь сохранения", command=self.save_file)
        save_button.pack(pady=10)
        method_label = tk.Label(self.root, text="Выберите метод преобразования:")
        method_label.pack()
        requests_radio = tk.Radiobutton(self.root, text="requests", variable=self.method_var, value="requests")
        requests_radio.pack()
        bb4_radio = tk.Radiobutton(self.root, text="bb4", variable=self.method_var, value="bb4")
        bb4_radio.pack()
        bb4_radio.config(state="disabled")
        selenium_radio = tk.Radiobutton(self.root, text="selenium", variable=self.method_var, value="selenium")
        selenium_radio.pack()
        self.convert_button = tk.Button(self.root, text="Преобразовать", command=self.convert_file)
        self.convert_button.pack(pady=10)
        self.convert_button.config(state="disabled")
        self.status_label = tk.Label(self.root, text="Начало работы скрипта:")
        self.status_label.pack(pady=10)
        self.status_label2 = tk.Label(self.root, text="Конец работы скрипта:")
        self.status_label2.pack(pady=10)
        self.status_label3 = tk.Label(self.root, text="Разница:")
        self.status_label3.pack(pady=10)

    # Нажатие кнопки "Выбрать файл"
    def open_file(self):
        """
        Получаем адрес файла - абсолютный путь,
        производим проверку на расширение файла - .CSV,
        при прохождение всех проверок кнопка 'Преобразовать' становиться активной.
        """
        self.file_path = filedialog.askopenfilename()
        # print(filedialog.askopenfilename())
        try:
            if self.file_path[-4:] == '.csv':
                self.convert_button.config(state="normal")
            else:
                raise FileExistsError
        except FileExistsError:
            self.file_path = ""
            self.status_label3.config(text="Выбранный файл не соответствует расширению .CSV")
            print("Выбранный файл не соответствует расширению .CSV")

    # Нажатие кнопки "Выбрать путь сохранения"
    def save_file(self):
        """
        Если кнопка не будет нажата, то сохранение произойдет в папку скрипта,
        в случае выбора папки сохранение произойдет в данную папку.
        :return:
        """
        self.save_path = filedialog.askdirectory()

    # Нажатие кнопки "Преобразовать"
    def convert_file(self):
        """
        Это основной метод, который произедет все действия для сбора информации и записи файла.

        start_time, end_time начало работы скрипта и конец работы,
        в status_label3 будет выведена время работы скрипта

        convert произведет преобразования .csv в список

        в зависимости от выбора метода преобразования, будет выбран способ запуска скрипта
        через библиотеку Requests или через библиотеку Selenium.

        :return:
        """
        # Очистить значения
        self.status_label.config(text="Начало работы скрипта:")
        self.status_label2.config(text="Конец работы скрипта:")
        self.status_label3.config(text="Разница:")


        start_time = datetime.now()
        self.status_label.config(text=self.status_label.cget("text") + str('\n') + \
                                      str(start_time.strftime('%H:%M:%S')))
        selected_method = self.method_var.get()

        convert = self.convert_csv()

        if selected_method == 'requests':
            otvet = self.request_test(convert)
        elif selected_method == 'bb4':
            otvet = self.request_test(convert)
        elif selected_method == 'selenium':
            otvet = self.selenium_test(convert)
        else:
            otvet = self.status_label3.config(text="Ошибка")

        file = Create_CSV_File(otvet)
        file.create_csv()

        end_time = datetime.now()
        self.status_label2.config(text=self.status_label2.cget("text") + str('\n') + \
                                       str(end_time.strftime('%H:%M:%S')))
        self.status_label3.config(text=self.status_label3.cget("text") + str('\n') + \
                                       str(end_time - start_time))

    # Открытие csv файла и преобразование в список
    def convert_csv(self):
        with open(self.file_path, newline='\n', encoding='UTF8') as f:
            spisok = []
            for x in csv.reader(f, delimiter=' ', quotechar='|'):
                spisok.append(x)
            return spisok

    # Запуск через библиотеку Requests
    def request_test(self, file, *args, **kwargs):
        if file:
            kol = WorkRequest(file)
            return kol.start_requests()
        else:
            self.status_label3.config(text="Пустой файл")


    # Запуск через библиотеку Selenium
    def selenium_test(self, file, *args, **kwargs):
        if file:
            kol = SeleniumStart(file)
            # print(kol.start_selenium())
            return kol.start_selenium()
        else:
            self.status_label3.config(text="Пустой файл")


    # Запуск Ткинтер
    def run(self):
        self.root.mainloop()


# import bs, selen
# selen.test_eight_components()
if __name__ == '__main__':
    app = TkinterParser()
    app.run()
