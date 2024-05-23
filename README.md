# Py_Late
#### Video Demo:  https://youtu.be/sGCaOhh5Jw8

#### Description:
Py_Late is a simple Python GUI translation application utilizing the Argostranslate backend library. The purpose of this application is to provide a user-friendly interface for translating text between different languages. It's important to note that this project is developed solely for academic purposes and is not intended for production use or long-term maintenance.


#### Concept:
The 'Py_Late' Translator GUI Application allows users to input text in one language and translate it into another language of their choice. The application supports multiple languages and provides a straightforward interface for users to select the input and output languages. It leverages the Argostranslate backend library, which offers translation capabilities and language detection.


#### Files and Functionality:

    project.py: This file contains the main functionality of the GUI application. It utilizes the Tkinter library for creating the graphical user interface. The Window class initializes the application window and sets up various widgets such as textboxes, comboboxes, and buttons for user interaction.

    translator.py: This file encapsulates the functionalities related to translation using the Argostranslate backend library. It includes the Translator class, which provides methods for installing language packages, translating text, checking available languages, and uninstalling packages. The class interacts with the Argostranslate library to perform translation tasks.


#### Design Choices:
The design of the 'Py_Late' Translator GUI Application prioritizes simplicity and ease of use. The decision to use Tkinter for the graphical interface was made due to its beginner friendly documentation and availability in the Python standard library. Tkinter provides a platform-independent solution for creating GUI applications without requiring additional dependencies.

The usage of the Argostranslate library for translation tasks was chosen for its open-source nature and effectiveness. While it's documentation is not very verbose, Argostranslate offers a locally installed API for translating text between languages, making it suitable for integration into the GUI application without having to trust external cloud providers.


#### Conclusion:
In summary, the 'Py_Late' Translator GUI Application serves as a basic tool for translating text between languages using the Argostranslate backend library. While it may lack advanced features found in commercial translation software, it provides a simple and effective solution for a personal usecase.

This project is provided under the MIT License. You are free to use, modify, and distribute the code for academic and non-commercial purposes. However, please note that this project is provided "AS IS," and no maintenance or support is guaranteed.
