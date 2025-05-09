<div align="center">

![Alt](https://repobeats.axiom.co/api/embed/cafc5ba9edb06cacde43b1b2cb329a7c5cb2bab7.svg "Repobeats analytics image")

# SL Manager

SL Manager is a simple tool designed to help SCP: Secret Laboratory players easily manage custom translations, music, and keybindings.

</div>

## Features

- **Custom Translations**: Easily add and manage your own translation files.
- **Custom Music**: Import `.mp3` files into the game’s music folder.
- **CmdBind Creator**: Add or remove custom command keybinds for custom commands.

## Installation

1. Download the latest release from the [GitHub repository](https://github.com/RLLanonymous/SLManager).
2. Extract the files to a location of your choice.
3. Run `SLManager.exe`.

## Requirements (Source Installation)

- **Python 3.9+**
- **Dependencies:**
  - altgraph                  0.17.4
  - Jinja2                    3.1.6
  - MarkupSafe                3.0.2
  - packaging                 24.2
  - pefile                    2023.2.7
  - pip                       25.0.1
  - pyinstaller               6.12.0
  - pyinstaller-hooks-contrib 2025.2
  - PyQt6                     6.8.1
  - PyQt6-Qt6                 6.8.2
  - PyQt6_sip                 13.10.0
  - pywin32-ctypes            0.2.3
  - qt-material               2.14
  - setuptools                78.0.2

- **Run the `python main.py` to test the app or `pyinstaller --onefile --windowed main.py` to build the app**

## Usage

1. **Custom Translations**:
   - Click the "Custom Translations" button.
   - Select the folder containing your translations.
   - The folder will be copied to the game’s `Translations` directory.

2. **Custom Music**:
   - Click the "Custom Music (.mp3 only)" button.
   - Select an `.mp3` file.
   - The file will be added to the game’s `music` folder.

3. **Keybinds**:
   - Enter the keybind code (e.g., `102`).
   - Enter the command (e.g., `.help`).
   - Click "Add Bind" to save it.

## Troubleshooting

### "Windows protected your PC Warning
If Windows SmartScreen blocks the app:
- Click **More info**.
- Click **Run anyway**.

## License

This project is licensed under the **AGPL License**. However, it uses Qt libraries which are licensed under the **LGPL v3**. 

### Qt LGPL v3 Obligations:
- This application links dynamically to the Qt libraries, and users can relink the application to their own version of Qt if desired.
- A copy of the Qt source code is available at [Qt's official repository](https://code.qt.io) if you wish to modify or view it.
- If you distribute the software, you must make the source code of Qt and any modifications available to the users.
- The application must also provide a mechanism for users to replace the Qt libraries (dynamic linking).

For more details about the LGPL v3 license, please consult the official documentation from [GNU](https://www.gnu.org/licenses/lgpl-3.0.html).

---

### 🔗 Links
- **GitHub Repository**: [SL Manager](https://github.com/RLLanonymous/SLManager)
- **Discord Server**: [Join Us](https://discord.gg/fqvMufQkmk)
