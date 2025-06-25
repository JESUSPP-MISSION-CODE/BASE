import sys
import numpy as np
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QWidget, QPushButton, QLabel, QFileDialog, QSlider,
                               QSpinBox, QGroupBox, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random

class SignalViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("시간 기반 신호 데이터 뷰어")
        self.setGeometry(100, 100, 1200, 800)
        
        # 데이터 저장 변수
        self.data = None
        self.time_data = None
        self.signal_data = None
        self.current_xlim = None
        self.current_ylim = None
        self.zoom_factor = 1.0
        self.pan_start = None
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        
        # 상단 컨트롤 패널
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # 그래프 영역
        self.create_plot_area()
        main_layout.addWidget(self.canvas)
        
        # 하단 상태바
        status_layout = QHBoxLayout()
        self.status_label = QLabel("파일을 로드하거나 샘플 데이터를 생성하세요")
        status_layout.addWidget(self.status_label)
        main_layout.addLayout(status_layout)
        
    def create_control_panel(self):
        control_group = QGroupBox("컨트롤 패널")
        control_layout = QGridLayout(control_group)
        
        # 파일 로드 버튼
        self.load_btn = QPushButton("파일 로드")
        self.load_btn.clicked.connect(self.load_file)
        control_layout.addWidget(self.load_btn, 0, 0)
        
        # 샘플 데이터 생성 버튼
        self.generate_btn = QPushButton("샘플 데이터 생성")
        self.generate_btn.clicked.connect(self.generate_sample_data)
        control_layout.addWidget(self.generate_btn, 0, 1)
        
        # 줌 컨트롤
        zoom_label = QLabel("줌:")
        control_layout.addWidget(zoom_label, 0, 2)
        
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(10, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.zoom_changed)
        control_layout.addWidget(self.zoom_slider, 0, 3)
        
        self.zoom_spinbox = QSpinBox()
        self.zoom_spinbox.setRange(10, 200)
        self.zoom_spinbox.setValue(100)
        self.zoom_spinbox.setSuffix("%")
        self.zoom_spinbox.valueChanged.connect(self.zoom_spinbox_changed)
        control_layout.addWidget(self.zoom_spinbox, 0, 4)
        
        # 네비게이션 버튼
        nav_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("전체 보기")
        self.reset_btn.clicked.connect(self.reset_view)
        nav_layout.addWidget(self.reset_btn)
        
        self.zoom_in_btn = QPushButton("줌 인")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        nav_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("줌 아웃")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        nav_layout.addWidget(self.zoom_out_btn)
        
        self.pan_left_btn = QPushButton("←")
        self.pan_left_btn.clicked.connect(self.pan_left)
        nav_layout.addWidget(self.pan_left_btn)
        
        self.pan_right_btn = QPushButton("→")
        self.pan_right_btn.clicked.connect(self.pan_right)
        nav_layout.addWidget(self.pan_right_btn)
        
        control_layout.addLayout(nav_layout, 1, 0, 1, 5)
        
        return control_group
    
    def create_plot_area(self):
        # matplotlib figure 생성
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        # 마우스 이벤트 연결
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "신호 데이터 파일 선택", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # 파일 로드
                data = pd.read_csv(file_path, delimiter='\t', header=None)
                if len(data.columns) >= 2:
                    self.time_data = data.iloc[:, 0].values
                    self.signal_data = data.iloc[:, 1].values
                    self.data = data
                    self.plot_data()
                    self.status_label.setText(f"파일 로드됨: {file_path}")
                else:
                    QMessageBox.warning(self, "오류", "파일 형식이 올바르지 않습니다. 최소 2개의 열이 필요합니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일 로드 중 오류가 발생했습니다: {str(e)}")
    
    def generate_sample_data(self):
        # 샘플 신호 데이터 생성
        duration = 100  # 초
        sample_rate = 100  # Hz
        t = np.linspace(0, duration, duration * sample_rate)
        
        # 복합 신호 생성 (사인파 + 노이즈 + 스파이크)
        signal = (np.sin(2 * np.pi * 1 * t) +  # 1Hz 기본 신호
                 0.5 * np.sin(2 * np.pi * 5 * t) +  # 5Hz 고주파
                 0.3 * np.sin(2 * np.pi * 0.2 * t) +  # 0.2Hz 저주파
                 0.1 * np.random.randn(len(t)))  # 노이즈
        
        # 스파이크 추가
        spike_indices = np.random.choice(len(t), size=10, replace=False)
        signal[spike_indices] += 2 * np.random.randn(len(spike_indices))
        
        self.time_data = t
        self.signal_data = signal
        self.data = pd.DataFrame({'time': t, 'signal': signal})
        
        self.plot_data()
        self.status_label.setText("샘플 데이터가 생성되었습니다.")
    
    def plot_data(self):
        if self.data is None:
            return
            
        self.ax.clear()
        self.ax.plot(self.time_data, self.signal_data, 'b-', linewidth=0.8)
        self.ax.set_xlabel('시간 (초)')
        self.ax.set_ylabel('신호 값')
        self.ax.set_title('시간 기반 신호 데이터')
        self.ax.grid(True, alpha=0.3)
        
        # 현재 뷰 범위 저장
        self.current_xlim = self.ax.get_xlim()
        self.current_ylim = self.ax.get_ylim()
        
        self.canvas.draw()
    
    def zoom_changed(self, value):
        self.zoom_spinbox.setValue(value)
        self.zoom_factor = value / 100.0
        self.apply_zoom()
    
    def zoom_spinbox_changed(self, value):
        self.zoom_slider.setValue(value)
        self.zoom_factor = value / 100.0
        self.apply_zoom()
    
    def apply_zoom(self):
        if self.current_xlim is None:
            return
            
        x_center = (self.current_xlim[0] + self.current_xlim[1]) / 2
        y_center = (self.current_ylim[0] + self.current_ylim[1]) / 2
        
        x_range = (self.current_xlim[1] - self.current_xlim[0]) / self.zoom_factor
        y_range = (self.current_ylim[1] - self.current_ylim[0]) / self.zoom_factor
        
        self.ax.set_xlim(x_center - x_range/2, x_center + x_range/2)
        self.ax.set_ylim(y_center - y_range/2, y_center + y_range/2)
        self.canvas.draw()
    
    def reset_view(self):
        if self.data is None:
            return
        self.ax.set_xlim(self.time_data.min(), self.time_data.max())
        self.ax.set_ylim(self.signal_data.min(), self.signal_data.max())
        self.current_xlim = self.ax.get_xlim()
        self.current_ylim = self.ax.get_ylim()
        self.zoom_factor = 1.0
        self.zoom_slider.setValue(100)
        self.zoom_spinbox.setValue(100)
        self.canvas.draw()
    
    def zoom_in(self):
        self.zoom_factor *= 1.2
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_slider.setValue(min(200, zoom_percent))
        self.zoom_spinbox.setValue(min(200, zoom_percent))
        self.apply_zoom()
    
    def zoom_out(self):
        self.zoom_factor /= 1.2
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_slider.setValue(max(10, zoom_percent))
        self.zoom_spinbox.setValue(max(10, zoom_percent))
        self.apply_zoom()
    
    def pan_left(self):
        if self.current_xlim is None:
            return
        x_range = self.current_xlim[1] - self.current_xlim[0]
        pan_distance = x_range * 0.1
        self.ax.set_xlim(self.current_xlim[0] - pan_distance, self.current_xlim[1] - pan_distance)
        self.current_xlim = self.ax.get_xlim()
        self.canvas.draw()
    
    def pan_right(self):
        if self.current_xlim is None:
            return
        x_range = self.current_xlim[1] - self.current_xlim[0]
        pan_distance = x_range * 0.1
        self.ax.set_xlim(self.current_xlim[0] + pan_distance, self.current_xlim[1] + pan_distance)
        self.current_xlim = self.ax.get_xlim()
        self.canvas.draw()
    
    def on_mouse_press(self, event):
        if event.button == 1:  # 좌클릭
            self.pan_start = (event.xdata, event.ydata)
    
    def on_mouse_release(self, event):
        self.pan_start = None
    
    def on_mouse_move(self, event):
        if self.pan_start is None or event.xdata is None:
            return
        
        if event.button == 1:  # 좌클릭 드래그로 패닝
            dx = event.xdata - self.pan_start[0]
            dy = event.ydata - self.pan_start[1]
            
            self.ax.set_xlim(self.current_xlim[0] - dx, self.current_xlim[1] - dx)
            self.ax.set_ylim(self.current_ylim[0] - dy, self.current_ylim[1] - dy)
            
            self.current_xlim = self.ax.get_xlim()
            self.current_ylim = self.ax.get_ylim()
            self.canvas.draw()
    
    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom_in()
        elif event.button == 'down':
            self.zoom_out()

def create_sample_signal_file():
    """샘플 신호 데이터 파일 생성"""
    duration = 100  # 초
    sample_rate = 100  # Hz
    t = np.linspace(0, duration, duration * sample_rate)
    
    # 복합 신호 생성
    signal = (np.sin(2 * np.pi * 1 * t) +  # 1Hz 기본 신호
             0.5 * np.sin(2 * np.pi * 5 * t) +  # 5Hz 고주파
             0.3 * np.sin(2 * np.pi * 0.2 * t) +  # 0.2Hz 저주파
             0.1 * np.random.randn(len(t)))  # 노이즈
    
    # 스파이크 추가
    spike_indices = np.random.choice(len(t), size=10, replace=False)
    signal[spike_indices] += 2 * np.random.randn(len(spike_indices))
    
    # 파일로 저장
    data = pd.DataFrame({'time': t, 'signal': signal})
    data.to_csv('sample_signal.txt', sep='\t', index=False, header=False)
    print("샘플 신호 파일이 생성되었습니다: sample_signal.txt")

if __name__ == '__main__':
    # 샘플 파일 생성
    create_sample_signal_file()
    
    app = QApplication(sys.argv)
    viewer = SignalViewer()
    viewer.show()
    sys.exit(app.exec())
