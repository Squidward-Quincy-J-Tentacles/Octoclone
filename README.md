# OctoClone 🐙

**Version:** v2025.08.13.GK0827
**Author:** MrSquidward

OctoClone is a Python-based web cloning and reconnaissance tool. It allows users to:

* Clone websites (HTML, CSS, JS, images)
* Discover subdomains via `crt.sh`
* Scan hidden directories (wordlist-based)
* Download files by extension
* Save and load project configurations

> ⚠️ **For educational and authorized testing purposes only.** Do not use this tool on websites you do not own or have permission to test.

---

## Table of Contents

1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Windows Executable](#windows-executable)
5. [Available Commands](#available-commands)
6. [Example Workflow](#example-workflow)
7. [Configuration](#configuration)
8. [Wordlist](#wordlist)
9. [Screenshots](#screenshots)
10. [License](#license)
11. [Contributing](#contributing)
12. [Troubleshooting](#troubleshooting)
13. [Disclaimer](#disclaimer)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/OctoClone.git
cd OctoClone
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: Make the script executable on Linux/macOS:

```bash
chmod +x octoclone.py
./octoclone.py
```

---

## Dependencies

* Python 3.x
* `requests`
* `beautifulsoup4`
* `colorama`

Install dependencies manually if needed:

```bash
pip install requests beautifulsoup4 colorama
```

---

## Usage

Run the tool:

```bash
python3 octoclone.py
```

You will see a prompt:

```text
octoclone>
```

---

## Windows Executable

To run OctoClone on Windows, use the pre-built `.exe` file (included in releases).
To build your own executable:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build executable:

```bash
pyinstaller --onefile octoclone.py
```

3. The executable will appear in the `dist` folder.

---

## Available Commands

Inside the OctoClone shell:

| Command              | Description                              |
| -------------------- | ---------------------------------------- |
| `set url <target>`   | Set target URL                           |
| `set project <path>` | Set project folder path                  |
| `clone`              | Clone the full website                   |
| `verbose on/off`     | Enable or disable verbose mode           |
| `subdomains`         | Find subdomains via crt.sh               |
| `subdirs`            | Scan hidden directories using a wordlist |
| `download <.ext>`    | Download specific file types             |
| `show config`        | Show current settings                    |
| `save config`        | Save current configuration to file       |
| `load config`        | Load configuration from file             |
| `cd <folder>`        | Change working directory                 |
| `help`               | Show help                                |
| `exit`               | Exit the tool                            |

> Any other Linux shell command entered will run in the system shell.

---

## Example Workflow

```text
octoclone> set url https://example.com
octoclone> set project ~/Desktop/ExampleClone
octoclone> verbose on
octoclone> clone
octoclone> subdomains
octoclone> subdirs
octoclone> download .jpg
```

---

## Configuration

OctoClone supports saving/loading project configuration:

* Save configuration:

```text
octoclone> save config
```

* Load configuration:

```text
octoclone> load config
```

Configuration is stored in `octoclone_config.json`.

---

## Wordlist

A sample `common.txt` wordlist is included for hidden directory scanning:

```
admin/
login/
dashboard/
config/
uploads/
images/
css/
js/
backup/
test/
```

You can replace this with your own custom wordlist.

---

## Screenshots

> *(Optional: Add screenshots of OctoClone in action)*

1. Cloning a website
2. Subdomain enumeration
3. Directory scanning results

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -am "Add new feature"`)
4. Push to the branch (`git push origin feature/xyz`)
5. Create a Pull Request

---

## Troubleshooting

* **Python version error:** Ensure you are using Python 3.x
* **Module not found:** Run `pip install -r requirements.txt`
* **Timeout errors:** Check your internet connection or target website status
* **Permission errors:** Ensure you have write access to the project folder

---

## Disclaimer

This tool is for **educational purposes only**. Do not attempt to clone or access sites without explicit permission. The author is not responsible for misuse.
