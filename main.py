import sys
from PyQt6.QtWidgets import QApplication
from app.worker import StatsWorker
from app.widget import DashboardWidget
from app.tray import SystemTrayApp

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    dashboard = DashboardWidget()
    tray = SystemTrayApp(widget=dashboard, parent=app)
    tray.show()

    # Worker Thread
    worker = StatsWorker(interval=1)
    
    # Sinyalleri bağla (Hem dashboard hem tray güncellenir)
    worker.stats_updated.connect(dashboard.update_stats)
    worker.stats_updated.connect(tray.update_tray)
    
    worker.start()

    def cleanup():
        worker.stop()

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()