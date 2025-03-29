import sys
import shutil
import os
import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QFormLayout, QLineEdit, QHBoxLayout, QSystemTrayIcon, QMenu, QComboBox, QLabel
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import Qt, QTranslator, QCoreApplication, QLocale, QSize
from qt_material import apply_stylesheet

# Info: Here should be placed every path to the files/folders you want to manage
TRANSLATION_DESTINATION_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\SCP Secret Laboratory\Translations"
MUSIC_DESTINATION_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\SCP Secret Laboratory\music"
CMDBINDING_PATH = r"C:\Users\Utilisateur\AppData\Roaming\SCP Secret Laboratory\cmdbinding.txt"

class SlManager(QWidget):
    def __init__(self):
        super().__init__()

        # Info: Here should be placed the settings of the app
        self.setWindowTitle(self.tr("SLManager"))
        self.setFixedSize(800, 300)
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('icon.ico'))
        apply_stylesheet(app, theme='dark_blue.xml')
        self.set_language()

        layout = QVBoxLayout()

        # Language selection combo box
        self.language_selector = QComboBox(self)
        self.language_selector.addItem(self.tr("Select Language"))
        self.language_selector.addItem("English")
        self.language_selector.addItem("Français")
        self.language_selector.addItem("Deutsch")
        self.language_selector.currentTextChanged.connect(self.change_language)
        layout.addWidget(self.language_selector)

        # Custom translation button
        self.btn_select_folder = QPushButton(self.tr("Custom Translations 📝"), self)
        self.btn_select_folder.clicked.connect(self.select_translation_file)
        layout.addWidget(self.btn_select_folder)

        # Custom music button
        self.btn_select_mp3 = QPushButton(self.tr("Custom Music (.mp3 only) 🎵"), self)
        self.btn_select_mp3.clicked.connect(self.select_mp3)
        layout.addWidget(self.btn_select_mp3)

        # New bind text input
        self.form_layout = QFormLayout()
        self.keybind_input = QLineEdit(self)
        self.command_input = QLineEdit(self)

        # Applying translation to labels, not QLineEdit
        label_keybind = QLabel(self.tr("Keybind (e.g., 102):"))
        label_command = QLabel(self.tr("Command (e.g., .help):"))

        self.form_layout.addRow(label_keybind, self.keybind_input)
        self.form_layout.addRow(label_command, self.command_input)

        layout.addLayout(self.form_layout)

        # Keybind buttons
        keybind_layout = QHBoxLayout()

        # Bind Add button
        self.btn_add_keybind = QPushButton(self.tr("Add Bind ✅"), self)
        self.btn_add_keybind.clicked.connect(self.add_keybind)
        keybind_layout.addWidget(self.btn_add_keybind)

        # Bind Help button
        self.btn_info = QPushButton(self.tr("Check Keybind Codes ℹ️"), self)
        self.btn_info.clicked.connect(self.open_link)
        keybind_layout.addWidget(self.btn_info)

        # Bind Clear button
        self.btn_clear_cmdbind = QPushButton(self.tr("Clear Binds ❌"), self)
        self.btn_clear_cmdbind.clicked.connect(self.clear_cmdbind)
        keybind_layout.addWidget(self.btn_clear_cmdbind)

        layout.addLayout(keybind_layout)

        self.setLayout(layout)

        # Tray icon
        self.tray_icon = QSystemTrayIcon(QIcon('icon.ico'), parent=self)
        self.tray_icon.setToolTip(self.tr("SLManager - Right click for options"))

        tray_menu = QMenu(self)
        quit_action = QAction(self.tr("Quit"), self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Add the top-right GitHub icon button
        top_layout = QHBoxLayout() 
        self.github_button = QPushButton(self)
        self.github_button.setIcon(QIcon("icon.ico")) 
        self.github_button.setIconSize(QSize(32, 32))  
        self.github_button.clicked.connect(self.open_github)

        top_layout.addStretch()
        top_layout.addWidget(self.github_button)

        layout.addLayout(top_layout)

    def set_language(self):
        # Load translation file based on system language
        translator = QTranslator()
        locale = QLocale.system().name()  # Auto-detect system language (fr_FR, en_US, etc.)
        
        if translator.load(f"{locale}.qm"):
            QCoreApplication.installTranslator(translator)
        else:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Failed to load the translation file for locale {locale}"))

    def change_language(self, language):
        if language == "English":
            self.load_translation("en_US.qm")
        elif language == "Français":
            self.load_translation("fr_FR.qm")
        elif language == "Deutsch":
            self.load_translation("de_DE.qm")
        else:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Language not supported."))

    def load_translation(self, lang_file):
        translator = QTranslator()  # Create the translator instance

        # Load the translation file
        if translator.load(lang_file):
            # Install the translator
            QApplication.instance().installTranslator(translator)

            # Mettre à jour tous les éléments de l'interface
            self.setWindowTitle(self.tr("SLManager"))
            self.language_selector.setItemText(0, self.tr("Select Language"))
            self.language_selector.setItemText(1, self.tr("English"))
            self.language_selector.setItemText(2, self.tr("Français"))
            self.language_selector.setItemText(3, self.tr("Deutsch"))
            self.btn_select_folder.setText(self.tr("Custom Translations 📝"))
            self.btn_select_mp3.setText(self.tr("Custom Music (.mp3 only) 🎵"))
            self.form_layout.itemAt(0).widget().setText(self.tr("Keybind (e.g., 102):"))
            self.form_layout.itemAt(1).widget().setText(self.tr("Command (e.g., .help):"))
            self.btn_add_keybind.setText(self.tr("Add Bind ✅"))
            self.btn_info.setText(self.tr("Check Keybind Codes ℹ️"))
            self.btn_clear_cmdbind.setText(self.tr("Clear Binds ❌"))

            QMessageBox.information(self, self.tr("Success"), self.tr(f"Language changed to {lang_file.split('.')[0]}"))

        else:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"Failed to load the translation file {lang_file}"))

    def select_translation_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("Select a Translation File"), "", "Translation Files (*.ts)")
        if file_path:
            file_name = os.path.basename(file_path)
            destination = os.path.join(TRANSLATION_DESTINATION_PATH, file_name)

            try:
                if os.path.exists(destination):
                    QMessageBox.warning(self, self.tr("Error"), self.tr(f"The file '{file_name}' already exists in Translations!"))
                    return

                shutil.copy2(file_path, destination)
                QMessageBox.information(self, self.tr("Success"), self.tr(f"The file '{file_name}' has been successfully moved!"))

            except Exception as ex:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"An error occurred: {str(ex)}"))

    def select_mp3(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("Select an .mp3 file"), "", "MP3 Files (*.mp3)")
        if file_path:
            file_name = os.path.basename(file_path)
            destination = os.path.join(MUSIC_DESTINATION_PATH, file_name)

            try:
                if os.path.exists(destination):
                    QMessageBox.warning(self, self.tr("Error"), self.tr(f"The file '{file_name}' already exists in music!"))
                    return

                shutil.copy2(file_path, destination)
                QMessageBox.information(self, self.tr("Success"), self.tr(f"The file '{file_name}' has been successfully moved!"))

            except Exception as ex:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"An error occurred: {str(ex)}"))

    def add_keybind(self):
        keybind = self.keybind_input.text().strip()
        command = self.command_input.text().strip()

        if not os.path.exists(CMDBINDING_PATH):
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"The file '{CMDBINDING_PATH}' does not exist!"))
            return

        if not keybind.isdigit() or not command:
            QMessageBox.warning(self, self.tr("Invalid Input"), self.tr("Please enter a valid keybind and command!"))
            return

        keybind_line = f"{keybind}:{command}"

        try:
            # Check if the keybind already exists
            with open(CMDBINDING_PATH, 'r') as file:
                content = file.read()

            with open(CMDBINDING_PATH, 'a') as file:
                if content and not content.endswith("\n"):
                    file.write("\n")  # Jump a line before writing
                file.write(keybind_line + '\n')

            QMessageBox.information(self, self.tr("Success"), self.tr(f"Keybind {keybind_line} has been added successfully!"))
            self.keybind_input.clear()
            self.command_input.clear()

        except Exception as ex:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"An error occurred: {str(ex)}"))

    def clear_cmdbind(self):
        if not os.path.exists(CMDBINDING_PATH):
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"The file '{CMDBINDING_PATH}' does not exist!"))
            return
        
        reply = QMessageBox.question(self, self.tr('Warning'), self.tr('Are you sure you want to clear all keybinds? This action cannot be undone.'),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                open(CMDBINDING_PATH, 'w').close()
                QMessageBox.information(self, self.tr("Success"), self.tr("All keybinds have been cleared successfully!"))
            except Exception as ex:
                QMessageBox.critical(self, self.tr("Error"), self.tr(f"An error occurred: {str(ex)}"))

    def open_link(self):
        url = "https://github.com/RLLanonymous/SLManager/blob/main/docs/Keybinds.md"
        webbrowser.open(url)

    def open_github(self):
        url = "https://github.com/RLLanonymous/SLManager"
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlManager()
    window.show()
    sys.exit(app.exec())
