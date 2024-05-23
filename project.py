from tkinter import Tk, Button, Label, Text, ttk, StringVar, IntVar, Checkbutton, Frame, Toplevel, Canvas, Scrollbar, END
from translator import Translator

class Window:
    def __init__(self):
        self.window_title = "Py_Late"
        self.window_width = 300
        self.window_height = 300
        self.window_padx = 10
        self.window_pady = 10

        self.window = Tk()
        self.window.title(self.window_title)
        self.window.minsize(width=self.window_width, height=self.window_height)
        self.window.config(padx=self.window_padx, pady=self.window_pady)
        self.window.grid()

        self.translator = Translator("en", "es")
        self.translator.quick_download()

        self.language_map = {"en": "English", "es": "Spanish"}
        self.language_names = list(self.language_map.values())

        self.from_textbox = Text(height=(self.window_height // 20), width=(self.window_width // 10))
        self.from_textbox.focus()
        self.from_textbox.grid(column=0, row=1, columnspan=2)

        self.to_textbox = Text(height=(self.window_height // 20), width=(self.window_width // 10))
        self.to_textbox.grid(column=3, row=1, columnspan=2)

        Label(text="Translating from:").grid(column=0, row=0)
        Label(text="Translating to:").grid(column=3, row=0)

        self.from_lang = StringVar()
        self.from_lang.set("English")
        self.from_combobox = ttk.Combobox(
            self.window, values=self.language_names, textvariable=self.from_lang, state="readonly"
        )
        self.from_combobox.bind("<<ComboboxSelected>>", self.update_from_code)
        self.from_combobox.grid(column=1, row=0)

        self.to_lang = StringVar()
        self.to_lang.set("Spanish")
        self.to_combobox = ttk.Combobox(
            self.window, values=self.language_names, textvariable=self.to_lang, state="readonly"
        )
        self.to_combobox.bind("<<ComboboxSelected>>", self.update_to_code)
        self.to_combobox.grid(column=4, row=0)

        self.translate_button = Button(text="Translate", command=self.translate_text)
        self.translate_button.grid(column=2, row=2)

        self.switch_text_button = Button(text="<-->", command=self.switch_text)
        self.switch_text_button.grid(column=2, row=1)

        self.download_button = Button(text="Download Packages", command=self.show_download_popup)
        self.download_button.grid(column=0, row=2)

        self.uninstall_button = Button(text="Uninstall all packages", command=self.uninstall_packages)
        self.uninstall_button.grid(column=4, row=2)

        self.languages_button = Button(text="Check available languages", command=self.check_languages)
        self.languages_button.grid(column=2, row=0)

    # prints available language packages
    def check_languages(self):
        langs = self.translator.check_languages()
        if len(langs) < 1:
            print("No languages downloaded!")
        else:
            print("Available languages:")
            for lang in langs:
                print(lang)

    # uninstalls all packages
    def uninstall_packages(self):
        self.translator.uninstall()
        self.refresh_comboboxes()

    # takes left box text -> translates and places to right text box
    def translate_text(self):
        self.to_textbox.delete("1.0", END)
        translation = self.translator.translate(self.from_textbox.get("1.0", END))
        self.to_textbox.insert("1.0", translation)

    # update the translator's current from lang code
    def update_from_code(self, event=None):
        code = next(code for code, name in self.translator._language_map.items() if name == self.from_lang.get())
        self.translator.from_code = code

    # update the current to lang code
    def update_to_code(self, event=None):
        code = next(code for code, name in self.translator._language_map.items() if name == self.to_lang.get())
        self.translator.to_code = code

    # swap the text box content and selected from / to lang codes
    def switch_text(self):
        from_text = self.from_textbox.get("1.0", "end-1c")
        to_text = self.to_textbox.get("1.0", "end-1c")

        self.from_textbox.delete("1.0", END)
        self.from_textbox.insert("1.0", to_text)

        self.to_textbox.delete("1.0", END)
        self.to_textbox.insert("1.0", from_text)

        tmp = self.from_lang.get()
        self.from_lang.set(self.to_lang.get())
        self.to_lang.set(tmp)

        self.update_from_code()
        self.update_to_code()

    # updates combobox values on user changes
    def update_comboboxes(self):
        self.language_map = self.translator.get_language_names()
        self.language_names = list(self.language_map.values())
        self.from_combobox['values'] = self.language_names
        self.to_combobox['values'] = self.language_names

    # refreshes combobox values when called
    def refresh_comboboxes(self):
        self.translator.update_language_map()
        self.update_comboboxes()

    # seperate window pop up for package downloads
    def show_download_popup(self):
        popup = Toplevel(self.window)
        popup.title("Select Packages to Download")

        canvas = Canvas(popup)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        available_packages = self.translator.get_packages()
        unique_packages = []
        seen_packages = set()

        for package in available_packages:
            package_str = str(package)
            languages = package_str.split(" → ")
            if len(languages) == 2:
                translation_direction = f"{languages[0]} → {languages[1]}"
                if translation_direction not in seen_packages:
                    unique_packages.append((translation_direction, package))
                    seen_packages.add(translation_direction)

        package_vars = [IntVar() for _ in unique_packages]

        # Create the checkboxes in a grid layout
        columns = 2  # Number of columns for checkboxes
        for i, (translation_direction, _) in enumerate(unique_packages):
            row = i // columns
            col = i % columns
            Checkbutton(frame, text=translation_direction, variable=package_vars[i]).grid(row=row, column=col, sticky="w")

        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        download_button = Button(
            popup,
            text="Download Selected Packages",
            command=lambda: self.download_packages(unique_packages, package_vars)
        )

        download_button.pack()

    
    def download_packages(self, unique_packages, package_vars):
        selected_packages = [package for (translation_direction, package), var in zip(unique_packages, package_vars) if var.get()]
        print("Installing selected packages:")
        [print(p) for p in selected_packages]
        self.translator.selected_download(selected_packages)
        print("Packages installed!")
        self.refresh_comboboxes()

    # call the window mainloop
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    Window().run()