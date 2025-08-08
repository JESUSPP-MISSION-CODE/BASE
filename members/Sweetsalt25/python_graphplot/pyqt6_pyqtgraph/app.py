import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
import pyqtgraph as pg

class SignalViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Viewer with Live Update & FFT")
        self.resize(1000, 700)

        
        # Layouts
        main_layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        # Widgets
        self.label = QLabel("Load a signal file to begin")
        self.time_plot = pg.PlotWidget(title="Time Domain")
        self.freq_plot = pg.PlotWidget(title="Frequency Domain")
        self.load_button = QPushButton("Load Signal File")
        self.reset_button = QPushButton("Reset View")
        self.fft_button = QPushButton("Show FFT")
        self.live_button = QPushButton("Start Live Update")

        # Add widgets
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.fft_button)
        button_layout.addWidget(self.live_button)

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.time_plot)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.freq_plot)

        # Connections
        self.load_button.clicked.connect(self.load_file)
        self.reset_button.clicked.connect(self.reset_view)
        self.fft_button.clicked.connect(self.show_fft)
        self.live_button.clicked.connect(self.toggle_live_update)

        # Data
        self.x_data = None
        self.y_data = None
        self.curve = self.time_plot.plot([], [])
        self.fft_curve = self.freq_plot.plot([], [])
        self.live_mode = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_live_data)

        # Plot settings
        self.time_plot.setMouseEnabled(x=True, y=True)
        self.freq_plot.setMouseEnabled(x=True, y=True)

        self.x1 = None
        self.x2 = None
        self.line1 = None
        self.line2 = None
        self.time_plot.scene().sigMouseClicked.connect(self.handle_mouse_click)


    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Open Signal File", "", "Text Files (*.txt)"
        )
        if fname:
            self.label.setText(f"Loaded file: " + fname)
            data = np.loadtxt(fname, delimiter=",")
            self.x_data = data[:, 0]
            self.y_data = data[:, 1]
            self.curve.setData(self.x_data, self.y_data)
            self.time_plot.enableAutoRange()

    def clear_lines(self):
        self.x1 = None
        self.x2 = None
        if self.line1:
            self.time_plot.removeItem(self.line1)
            self.line1 = None
        if self.line2:
            self.time_plot.removeItem(self.line2)
            self.line2 = None

    def reset_view(self):
        if self.x_data is not None:
            self.curve.setData(self.x_data, self.y_data)
            self.time_plot.enableAutoRange()
            self.clear_lines()

    def show_fft(self):
        if self.y_data is not None:
            N = len(self.y_data)
            dt = self.x_data[1] - self.x_data[0]
            freq = np.fft.rfftfreq(N, d=dt)
            fft_vals = np.abs(np.fft.rfft(self.y_data))
            self.fft_curve.setData(freq, fft_vals)
            self.freq_plot.enableAutoRange()

    def toggle_live_update(self):
        if not self.live_mode:
            self.live_mode = True
            self.live_button.setText("Stop Live Update")
            self.x_data = []
            self.y_data = []
            self.timer.start(100)  # update every 100 ms
        else:
            self.live_mode = False
            self.live_button.setText("Start Live Update")
            self.timer.stop()

    def update_live_data(self):
        if self.x_data is None or self.y_data is None:
            self.x_data = []
            self.y_data = []

        # 시간 증가
        t = self.x_data[-1] + 0.1 if self.x_data else 0

        # 실시간으로 변화하는 신호 생성 (예: 주기적으로 주파수 변화)
        freq = 1 + 0.5 * np.sin(0.1 * t)  # 주파수가 천천히 변함
        new_y = np.sin(2 * np.pi * freq * t) + 0.3 * np.random.randn()

        self.x_data.append(t)
        self.y_data.append(new_y)

        # 최근 500개만 유지
        self.x_data = self.x_data[-500:]
        self.y_data = self.y_data[-500:]

        self.curve.setData(self.x_data, self.y_data)

    def handle_mouse_click(self, event):
        mouse_point = self.time_plot.plotItem.vb.mapSceneToView(event.scenePos())
        x = mouse_point.x()

        if event.button() == Qt.MouseButton.LeftButton:
            if event.double():
                # 더블클릭일 경우 확대
                if self.x1 is not None and self.x2 is not None:
                    x_min, x_max = sorted([self.x1, self.x2])
                    if x_min <= x <= x_max:
                        self.time_plot.setXRange(x_min, x_max, padding=0)
            else:
                # 일반 클릭일 경우 수직선 추가
                if self.x1 is None:
                    self.x1 = x
                    if self.line1:
                        self.time_plot.removeItem(self.line1)
                    self.line1 = self.create_draggable_line(x, "x1")
                    self.time_plot.addItem(self.line1)
                elif self.x2 is None:
                    self.x2 = x
                    if self.line2:
                        self.time_plot.removeItem(self.line2)
                    self.line2 = self.create_draggable_line(x, "x2")
                    self.time_plot.addItem(self.line2)
    
    def create_draggable_line(self, x, line_id):
        pen_normal = pg.mkPen('y', width=1)
        pen_active = pg.mkPen('b', width=4)

        line = pg.InfiniteLine(pos=x, angle=90, pen=pen_normal, movable=True)
        self.time_plot.addItem(line)

        def on_click():
            line.setPen(pen_active)

        def on_release():
            line.setPen(pen_normal)
            if line_id == "x1":
                self.x1 = line.value()
            elif line_id == "x2":
                self.x2 = line.value()

        line.sigClicked.connect(on_click)
        line.sigPositionChanged.connect(on_release)

        return line


    def mouseDoubleClickEvent(self, event):
        if self.x1 is not None and self.x2 is not None:
            x_min, x_max = sorted([self.x1, self.x2])
            mouse_point = self.time_plot.plotItem.vb.mapSceneToView(event.position())
            x = mouse_point.x()
            if x_min <= x <= x_max:
                self.time_plot.setXRange(x_min, x_max, padding=0)
                self.clear_lines()

    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = SignalViewer()
    viewer.show()
    sys.exit(app.exec())


