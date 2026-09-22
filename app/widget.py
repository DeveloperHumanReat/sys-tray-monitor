from collections import deque
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QPen, QLinearGradient
from PyQt6.QtCore import Qt

class CPUChartWidget(QWidget):
    """Son 30 saniyelik CPU kullanımını çizen hafif Sparkline Grafik"""
    def __init__(self, max_points=30, parent=None):
        super().__init__(parent)
        self.max_points = max_points
        self.data = deque([0.0] * max_points, maxlen=max_points)
        self.setFixedHeight(70)

    def add_value(self, val):
        self.data.append(val)
        self.update()  # paintEvent çağrısını tetikler

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Grafik Arka Planı
        painter.fillRect(0, 0, w, h, QColor("#181825"))

        # Çerçeve Çizgisi
        painter.setPen(QPen(QColor("#313244"), 1))
        painter.drawRect(0, 0, w - 1, h - 1)

        if len(self.data) < 2:
            return

        # Noktaları Hesapla
        step = w / (self.max_points - 1)
        points = []
        for i, val in enumerate(self.data):
            x = i * step
            # 0..100 değerini grafik yüksekliğine göre oranla (Kenarlardan padding bırakarak)
            y = h - (val / 100.0 * (h - 10) + 5)
            points.append((x, y))

        # Çizgi Yolu (Path) Oluştur
        path = QPainterPath()
        path.moveTo(points[0][0], points[0][1])
        for x, y in points[1:]:
            path.lineTo(x, y)

        # Çizginin Altını Renkle Doldur (Gradient Fill)
        fill_path = QPainterPath(path)
        fill_path.lineTo(w, h)
        fill_path.lineTo(0, h)
        fill_path.closeSubpath()

        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0.0, QColor(137, 180, 250, 100))  # #89b4fa / %40 opaklık
        gradient.setColorAt(1.0, QColor(137, 180, 250, 0))    # Tam şeffaf

        painter.fillPath(fill_path, gradient)

        # Çizginin Kendisini Çiz
        pen = QPen(QColor("#89b4fa"), 2)
        painter.setPen(pen)
        painter.drawPath(path)


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Grafiğe yer açmak için yüksekliği 420px yaptık
        self.setFixedSize(310, 430)

        layout = QVBoxLayout()
        self.setLayout(layout)

        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 14px;
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 12px;
                font-weight: 600;
                border: none;
            }
            QProgressBar {
                border: none;
                background-color: #313244;
                border-radius: 4px;
                text-align: center;
                color: transparent;
                height: 7px;
            }
            QProgressBar::chunk {
                border-radius: 4px;
            }
        """)

        c_layout = QVBoxLayout(container)

        # Başlık
        title = QLabel("⚡ Sistem Performansı")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #89b4fa; padding-bottom: 2px;")
        c_layout.addWidget(title)

        # CPU & İlerleme Çubuğu
        self.cpu_label = QLabel("CPU: %0")
        self.cpu_bar = QProgressBar()
        c_layout.addWidget(self.cpu_label)
        c_layout.addWidget(self.cpu_bar)

        # Canlı CPU Grafiği
        self.chart = CPUChartWidget(max_points=30)
        c_layout.addWidget(self.chart)

        # RAM
        self.ram_label = QLabel("RAM: %0")
        self.ram_bar = QProgressBar()
        c_layout.addWidget(self.ram_label)
        c_layout.addWidget(self.ram_bar)

        # DISK
        self.disk_label = QLabel("Disk: %0")
        self.disk_bar = QProgressBar()
        c_layout.addWidget(self.disk_label)
        c_layout.addWidget(self.disk_bar)

        # Network
        self.net_label = QLabel("↓ 0.0 KB/s  |  ↑ 0.0 KB/s")
        self.net_label.setStyleSheet("color: #a6adc8; font-size: 11px; margin-top: 2px;")
        c_layout.addWidget(self.net_label)

        # Ayırıcı Çizgi
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #313244; max-height: 1px; margin: 4px 0px;")
        c_layout.addWidget(line)

        # En Çok Kaynak Tüketenler
        proc_title = QLabel("🔥 En Yüksek CPU Kullananlar")
        proc_title.setStyleSheet("color: #f9e2af; font-size: 11px; font-weight: bold;")
        c_layout.addWidget(proc_title)

        self.proc_labels = []
        for _ in range(3):
            lbl = QLabel("-")
            lbl.setStyleSheet("color: #bac2de; font-size: 11px; font-weight: normal;")
            c_layout.addWidget(lbl)
            self.proc_labels.append(lbl)

        layout.addWidget(container)

    def get_bar_color(self, val):
        if val < 60:
            return "#a6e3a1"
        elif val < 85:
            return "#f9e2af"
        return "#f38ba8"

    def update_stats(self, data):
        # CPU & Grafik
        cpu_val = data['cpu']
        self.cpu_label.setText(f"CPU: %{cpu_val:.1f}")
        self.cpu_bar.setValue(int(cpu_val))
        self.cpu_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.get_bar_color(cpu_val)}; }}")
        
        # Grafiğe yeni veriyi ekle
        self.chart.add_value(cpu_val)

        # RAM & Disk
        self.ram_label.setText(f"RAM: %{data['ram']:.1f}")
        self.ram_bar.setValue(int(data['ram']))
        self.ram_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.get_bar_color(data['ram'])}; }}")

        self.disk_label.setText(f"Disk: %{data['disk']:.1f}")
        self.disk_bar.setValue(int(data['disk']))
        self.disk_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.get_bar_color(data['disk'])}; }}")

        # Network
        self.net_label.setText(f"↓ {data['download_kb']:.1f} KB/s  |  ↑ {data['upload_kb']:.1f} KB/s")

        # Top Processes
        procs = data.get("top_processes", [])
        for i in range(3):
            if i < len(procs):
                p_name = procs[i]['name']
                if len(p_name) > 18:
                    p_name = p_name[:15] + "..."
                p_cpu = procs[i]['cpu_percent']
                self.proc_labels[i].setText(f"{i+1}. {p_name} (%{p_cpu:.1f})")
            else:
                self.proc_labels[i].setText("-")

    def changeEvent(self, event):
        if event.type() == event.Type.ActivationChange and not self.isActiveWindow():
            self.hide()
        super().changeEvent(event)