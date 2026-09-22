⚡ Windows System Tray Performance Monitor

A lightweight, modern, and feature-rich desktop performance monitor for Windows. Built with Python 3 and PyQt6, it runs silently in the system tray and provides real-time hardware telemetry.

🚀 Key Features

System Tray Integration: Runs seamlessly in the background with a dynamic tray icon. The icon color updates automatically based on CPU usage (Blue = Normal, Yellow = Medium, Red = High CPU load).

Dark Mode Dashboard: Minimalist dark UI with real-time progress indicators for hardware resources.

Live CPU Sparkline Chart: Custom hardware-accelerated 30-second rolling CPU utilization graph built with QPainter.

Top Resource Consumers: Displays the top 3 CPU-intensive processes in real time using psutil.

Network & Storage Monitoring: Live tracking for Download/Upload speeds (KB/s), RAM, and Disk usage.

Windows Registry Autostart: Built-in option to automatically run on Windows boot (HKCU\Software\Microsoft\Windows\CurrentVersion\Run).

Standalone Binary Support: Can be compiled into a single background --noconsole .exe using PyInstaller.

🛠️ Tech Stack

Language: Python 3.x

GUI Framework: PyQt6

System Metrics: psutil

Build System: PyInstaller

📂 Project Structure

sys-tray-monitor/
│── .gitignore
│── requirements.txt
│── main.py
│── README.md
└── app/
    ├── __init__.py
    ├── autostart.py   # Windows Registry auto-start manager
    ├── worker.py      # Background telemetry thread
    ├── widget.py      # Dark Mode Dashboard & Live Sparkline Chart
    └── tray.py        # Dynamic system tray icon & context menu


📦 Installation & Setup

Clone the repository:

git clone https://github.com/DeveloperHumanReat/sys-tray-monitor.git
cd sys-tray-monitor


Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run the application:

python main.py


🔨 Building Standalone Executable (.exe)

To build a background executable that runs without opening a black command line window:

pip install pyinstaller
pyinstaller --noconsole --onefile --name "SysTrayMonitor" main.py


The generated SysTrayMonitor.exe file will be saved in the dist/ directory.

📬 Author & Contact

Developer: DeveloperHumanReat

GitHub: @DeveloperHumanReat

Email: developerhumanreat@gmail.com