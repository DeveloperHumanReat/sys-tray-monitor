from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt
from app.autostart import is_autostart_enabled, set_autostart

class SystemTrayApp(QSystemTrayIcon):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.widget = widget

        self.setIcon(self.create_dynamic_icon(0))
        self.setToolTip("Windows Sistem Monitörü")

        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item:selected {
                background-color: #45475a;
                border-radius: 4px;
            }
            QMenu::item:checked {
                color: #a6e3a1;
            }
        """)

        # Dashboard Göster
        show_action = self.menu.addAction("Dashboard Göster")
        show_action.triggered.connect(self.toggle_widget)

        self.menu.addSeparator()

        # Windows Başlangıcında Çalıştır (Checkable Option)
        self.autostart_action = self.menu.addAction("Windows ile Başlat")
        self.autostart_action.setCheckable(True)
        self.autostart_action.setChecked(is_autostart_enabled())
        self.autostart_action.triggered.connect(self.toggle_autostart)

        self.menu.addSeparator()

        # Çıkış
        quit_action = self.menu.addAction("Çıkış")
        quit_action.triggered.connect(self.parent().quit)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_tray_click)

    def toggle_autostart(self, checked):
        success = set_autostart(checked)
        if not success:
            # İşlem başarısız olduysa kutucuğu eski durumuna çek
            self.autostart_action.setChecked(not checked)

    def create_dynamic_icon(self, cpu_percent):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if cpu_percent < 50:
            bg_color = QColor("#89b4fa")
        elif cpu_percent < 80:
            bg_color = QColor("#f9e2af")
        else:
            bg_color = QColor("#f38ba8")

        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 28, 28)

        painter.setPen(QColor("#11111b"))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(11)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "S")
        painter.end()

        return QIcon(pixmap)

    def update_tray(self, data):
        cpu = data["cpu"]
        ram = data["ram"]
        self.setIcon(self.create_dynamic_icon(cpu))
        self.setToolTip(f"Sistem Monitörü\nCPU: %{cpu:.1f} | RAM: %{ram:.1f}")

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_widget()

    def toggle_widget(self):
        if self.widget.isVisible():
            self.widget.hide()
        else:
            geometry = self.geometry()
            x = geometry.x() - self.widget.width() // 2
            y = geometry.y() - self.widget.height() - 10
            
            if x < 0: x = 10
            if y < 0: y = 10

            self.widget.move(x, y)
            self.widget.show()
            self.widget.activateWindow()