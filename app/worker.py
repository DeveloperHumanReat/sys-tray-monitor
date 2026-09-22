import time
import psutil
from PyQt6.QtCore import QThread, pyqtSignal

class StatsWorker(QThread):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval=1):
        super().__init__()
        self.interval = interval
        self._is_running = True

    def get_top_processes(self, limit=3):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                # cpu_percent değerini doğru almak için tekil çağırma
                info = proc.info
                if info['cpu_percent'] is not None and info['name']:
                    processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # CPU kullanımına göre büyükten küçüğe sırala
        processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
        return processes[:limit]

    def run(self):
        prev_net = psutil.net_io_counters()
        prev_time = time.time()
        
        # psutil cpu_percent ilk çağrıda 0 döner, ısınma turu yapıyoruz
        psutil.cpu_percent()

        while self._is_running:
            time.sleep(self.interval)
            curr_time = time.time()
            curr_net = psutil.net_io_counters()

            elapsed = curr_time - prev_time
            if elapsed <= 0:
                elapsed = 1

            bytes_sent_sec = (curr_net.bytes_sent - prev_net.bytes_sent) / elapsed
            bytes_recv_sec = (curr_net.bytes_recv - prev_net.bytes_recv) / elapsed

            prev_net = curr_net
            prev_time = curr_time

            cpu_val = psutil.cpu_percent()
            top_procs = self.get_top_processes()

            data = {
                "cpu": cpu_val,
                "ram": psutil.virtual_memory().percent,
                "disk": psutil.disk_usage('/').percent,
                "upload_kb": bytes_sent_sec / 1024,
                "download_kb": bytes_recv_sec / 1024,
                "top_processes": top_procs
            }

            self.stats_updated.emit(data)

    def stop(self):
        self._is_running = False
        self.wait()