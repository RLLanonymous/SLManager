import sys
import shutil
import os
import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QFormLayout, QLineEdit, QHBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer
from qt_material import apply_stylesheet


# Destination paths
TRANSLATION_DESTINATION_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\SCP Secret Laboratory\Translations"
MUSIC_DESTINATION_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\SCP Secret Laboratory\music"
CMDBINDING_PATH = r"C:\Users\Utilisateur\AppData\Roaming\SCP Secret Laboratory\cmdbinding.txt"

class SlManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SLManager")
        self.setFixedSize(500, 300)
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('icon.ico'))  # Ensure you have an 'icon.png' file in the same directory as your script
        
        apply_stylesheet(app, theme='dark_blue.xml')


        layout = QVBoxLayout()

        # Button to drop a folder into Translations
        self.btn_select_folder = QPushButton("Custom Translations 📝", self)
        self.btn_select_folder.clicked.connect(self.select_folder)
        layout.addWidget(self.btn_select_folder)

        # Button to drop an .mp3 file into music
        self.btn_select_mp3 = QPushButton("Custom Music (.mp3 only) 🎵", self)
        self.btn_select_mp3.clicked.connect(self.select_mp3)
        layout.addWidget(self.btn_select_mp3)

        # Form to input keybinds
        self.form_layout = QFormLayout()
        self.keybind_input = QLineEdit(self)
        self.command_input = QLineEdit(self)

        self.form_layout.addRow("Keybind (e.g., 102):", self.keybind_input)
        self.form_layout.addRow("Command (e.g., .help):", self.command_input)

        # Reduce spacing in the form layout
        self.form_layout.setVerticalSpacing(5)  # Reduced vertical spacing between rows
        self.form_layout.setContentsMargins(0, 0, 0, 0)  # No margins for the form

        layout.addLayout(self.form_layout)

        # Create a horizontal layout for the keybind and info button
        keybind_layout = QHBoxLayout()
        
        # Button to add a keybind
        self.btn_add_keybind = QPushButton("Add Bind ✅", self)
        self.btn_add_keybind.clicked.connect(self.add_keybind)
        keybind_layout.addWidget(self.btn_add_keybind)

        # Info button (I) to redirect to a link
        self.btn_info = QPushButton("Check Keybind Codes ℹ️", self)
        self.btn_info.clicked.connect(self.open_link)
        keybind_layout.addWidget(self.btn_info)

        # Clear cmdbinding button
        self.btn_clear_cmdbind = QPushButton("Clear Binds ❌", self)
        self.btn_clear_cmdbind.clicked.connect(self.clear_cmdbind)
        keybind_layout.addWidget(self.btn_clear_cmdbind)

        # Reduce horizontal spacing between buttons
        keybind_layout.setSpacing(10)  # Reduced spacing between buttons

        layout.addLayout(keybind_layout)

        self.setLayout(layout)

        # Set up the system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon('icon.ico'), parent=self)  # Use your icon file here
        self.tray_icon.setToolTip("SLManager - Right click for options")
        
        # Create a context menu for the tray icon
        tray_menu = QMenu(self)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        # Set the tray icon's menu
        self.tray_icon.setContextMenu(tray_menu)

        # Show the tray icon
        self.tray_icon.show()

    def select_folder(self):
        # Selects a folder and copies it to Translations
        folder_path = QFileDialog.getExistingDirectory(self, "Choose the folder to move")

        if folder_path:
            folder_name = os.path.basename(folder_path)
            destination = os.path.join(TRANSLATION_DESTINATION_PATH, folder_name)

            try:
                if os.path.exists(destination):
                    QMessageBox.warning(self, "Error", f"The folder '{folder_name}' already exists in Translations!")
                    return

                shutil.copytree(folder_path, destination)
                QMessageBox.information(self, "Success", f"The folder '{folder_name}' has been successfully moved!")

            except Exception as ex:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")

    def select_mp3(self):
        # Selects an .mp3 file and copies it to the music folder
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an .mp3 file", "", "MP3 Files (*.mp3)")

        if file_path:
            file_name = os.path.basename(file_path)
            destination = os.path.join(MUSIC_DESTINATION_PATH, file_name)

            try:
                if os.path.exists(destination):
                    QMessageBox.warning(self, "Error", f"The file '{file_name}' already exists in music!")
                    return

                shutil.copy2(file_path, destination)
                QMessageBox.information(self, "Success", f"The file '{file_name}' has been successfully moved!")

            except Exception as ex:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")

    def add_keybind(self):
        # Add a keybind to cmdbinding.txt
        keybind = self.keybind_input.text().strip()
        command = self.command_input.text().strip()

        # Validation of inputs
        if not keybind.isdigit() or not command:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid keybind and command!")
            return

        # Format the line to add to the file
        keybind_line = f"{keybind}:{command}"

        # Add the keybind to cmdbinding.txt
        try:
            with open(CMDBINDING_PATH, 'a') as file:
                file.write(keybind_line + '\n')

            QMessageBox.information(self, "Success", f"Keybind {keybind_line} has been added successfully!")
            self.keybind_input.clear()
            self.command_input.clear()

        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")

    def clear_cmdbind(self):
        # Clear the cmdbinding.txt file with a warning
        reply = QMessageBox.question(self, 'Warning', 'Are you sure you want to clear all keybinds? This action cannot be undone.',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Clear the cmdbinding.txt file
                open(CMDBINDING_PATH, 'w').close()
                QMessageBox.information(self, "Success", "All keybinds have been cleared successfully!")
            except Exception as ex:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")

    def open_link(self):
        # Opens the URL when the info button is clicked
        url = "https://github.com/RLLanonymous/SLManager/blob/dev/docs/Keybinds.md"
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlManager()
    window.show()
    sys.exit(app.exec())
