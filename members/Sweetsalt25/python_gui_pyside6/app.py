#!/usr/bin/env python3
"""
PySide6 종합 학습 실습 프로젝트
각 탭별로 PySide6의 다양한 기능들을 체계적으로 학습할 수 있습니다.
"""

import sys
import json
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, 
    QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QSlider, 
    QProgressBar, QCheckBox, QRadioButton, QButtonGroup,
    QListWidget, QTableWidget, QTableWidgetItem, QTreeWidget, 
    QTreeWidgetItem, QGroupBox, QSplitter, QScrollArea,
    QFileDialog, QMessageBox, QInputDialog, QColorDialog,
    QFontDialog, QDialog, QDialogButtonBox, QFormLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QSystemTrayIcon,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsEllipseItem, QGraphicsTextItem, QListView
)
from PySide6.QtCore import (
    Qt, QTimer, QThread, Signal, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QSize, QSettings, QStandardPaths,
    QUrl, QMimeData, QStringListModel
)
from PySide6.QtGui import (
    QFont, QColor, QPalette, QPixmap, QPainter, QPen, QBrush,
    QIcon, QAction, QKeySequence, QDragEnterEvent, QDropEvent,
    QDrag, QCursor
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis


class WorkerThread(QThread):
    """백그라운드 작업을 위한 워커 스레드"""
    progress_updated = Signal(int)
    task_completed = Signal(str)
    
    def __init__(self, task_type="default"):
        super().__init__()
        self.task_type = task_type
        self.should_stop = False
    
    def run(self):
        if self.task_type == "progress":
            for i in range(101):
                if self.should_stop:
                    break
                time.sleep(0.05)
                self.progress_updated.emit(i)
            self.task_completed.emit("진행률 작업 완료!")
        
        elif self.task_type == "calculation":
            result = 0
            for i in range(1000000):
                if self.should_stop:
                    break
                result += i
                if i % 50000 == 0:
                    progress = int((i / 1000000) * 100)
                    self.progress_updated.emit(progress)
            self.task_completed.emit(f"계산 완료! 결과: {result}")
    
    def stop(self):
        self.should_stop = True


class BasicWidgetsTab(QWidget):
    """기본 위젯들을 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("1. 기본 위젯 학습")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 텍스트 입력 그룹
        text_group = QGroupBox("텍스트 입력 위젯")
        text_layout = QFormLayout()
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("한 줄 텍스트 입력")
        text_layout.addRow("QLineEdit:", self.line_edit)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("여러 줄 텍스트 입력")
        self.text_edit.setMaximumHeight(100)
        text_layout.addRow("QTextEdit:", self.text_edit)
        
        text_group.setLayout(text_layout)
        layout.addWidget(text_group)
        
        # 선택 위젯 그룹
        selection_group = QGroupBox("선택 위젯")
        selection_layout = QFormLayout()
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(["옵션 1", "옵션 2", "옵션 3", "옵션 4"])
        selection_layout.addRow("QComboBox:", self.combo_box)
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(50)
        selection_layout.addRow("QSpinBox:", self.spin_box)
        
        self.double_spin_box = QDoubleSpinBox()
        self.double_spin_box.setRange(0.0, 10.0)
        self.double_spin_box.setSingleStep(0.1)
        self.double_spin_box.setValue(5.0)
        selection_layout.addRow("QDoubleSpinBox:", self.double_spin_box)
        
        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)
        
        # 체크박스와 라디오버튼 그룹
        check_radio_group = QGroupBox("체크박스와 라디오버튼")
        check_radio_layout = QVBoxLayout()
        
        # 체크박스들
        self.check1 = QCheckBox("체크박스 1")
        self.check2 = QCheckBox("체크박스 2")
        self.check3 = QCheckBox("체크박스 3")
        check_radio_layout.addWidget(self.check1)
        check_radio_layout.addWidget(self.check2)
        check_radio_layout.addWidget(self.check3)
        
        # 라디오버튼 그룹
        self.radio_group = QButtonGroup()
        self.radio1 = QRadioButton("라디오 1")
        self.radio2 = QRadioButton("라디오 2")
        self.radio3 = QRadioButton("라디오 3")
        self.radio1.setChecked(True)
        
        self.radio_group.addButton(self.radio1)
        self.radio_group.addButton(self.radio2)
        self.radio_group.addButton(self.radio3)
        
        check_radio_layout.addWidget(self.radio1)
        check_radio_layout.addWidget(self.radio2)
        check_radio_layout.addWidget(self.radio3)
        
        check_radio_group.setLayout(check_radio_layout)
        layout.addWidget(check_radio_group)
        
        # 슬라이더와 프로그레스바
        slider_progress_group = QGroupBox("슬라이더와 프로그레스바")
        slider_progress_layout = QVBoxLayout()
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        slider_progress_layout.addWidget(QLabel("QSlider:"))
        slider_progress_layout.addWidget(self.slider)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(50)
        slider_progress_layout.addWidget(QLabel("QProgressBar:"))
        slider_progress_layout.addWidget(self.progress_bar)
        
        # 슬라이더와 프로그레스바 연결
        self.slider.valueChanged.connect(self.progress_bar.setValue)
        
        slider_progress_group.setLayout(slider_progress_layout)
        layout.addWidget(slider_progress_group)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        test_button = QPushButton("값 출력하기")
        test_button.clicked.connect(self.show_values)
        button_layout.addWidget(test_button)
        
        clear_button = QPushButton("초기화")
        clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_button)
        
        layout.addLayout(button_layout)
        
        # 결과 표시 영역
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(100)
        self.result_text.setReadOnly(True)
        layout.addWidget(QLabel("결과:"))
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
    
    def show_values(self):
        """현재 모든 위젯의 값을 표시"""
        values = []
        values.append(f"LineEdit: {self.line_edit.text()}")
        values.append(f"TextEdit: {self.text_edit.toPlainText()[:50]}...")
        values.append(f"ComboBox: {self.combo_box.currentText()}")
        values.append(f"SpinBox: {self.spin_box.value()}")
        values.append(f"DoubleSpinBox: {self.double_spin_box.value()}")
        
        checked_boxes = []
        if self.check1.isChecked(): checked_boxes.append("체크박스 1")
        if self.check2.isChecked(): checked_boxes.append("체크박스 2")
        if self.check3.isChecked(): checked_boxes.append("체크박스 3")
        values.append(f"체크된 박스: {', '.join(checked_boxes) if checked_boxes else '없음'}")
        
        selected_radio = self.radio_group.checkedButton().text() if self.radio_group.checkedButton() else "없음"
        values.append(f"선택된 라디오: {selected_radio}")
        values.append(f"슬라이더 값: {self.slider.value()}")
        
        self.result_text.setText("\n".join(values))
    
    def clear_all(self):
        """모든 위젯 초기화"""
        self.line_edit.clear()
        self.text_edit.clear()
        self.combo_box.setCurrentIndex(0)
        self.spin_box.setValue(0)
        self.double_spin_box.setValue(0.0)
        self.check1.setChecked(False)
        self.check2.setChecked(False)
        self.check3.setChecked(False)
        self.radio1.setChecked(True)
        self.slider.setValue(0)
        self.result_text.clear()


class LayoutsTab(QWidget):
    """레이아웃 관리자를 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # 제목
        title = QLabel("2. 레이아웃 관리자 학습")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # 스플리터로 영역 나누기
        splitter = QSplitter(Qt.Horizontal)
        
        # VBoxLayout 예제
        vbox_group = QGroupBox("QVBoxLayout (수직)")
        vbox_layout = QVBoxLayout()
        for i in range(4):
            btn = QPushButton(f"버튼 {i+1}")
            vbox_layout.addWidget(btn)
        vbox_group.setLayout(vbox_layout)
        splitter.addWidget(vbox_group)
        
        # HBoxLayout 예제
        hbox_group = QGroupBox("QHBoxLayout (수평)")
        hbox_layout = QHBoxLayout()
        for i in range(4):
            btn = QPushButton(f"버튼 {i+1}")
            hbox_layout.addWidget(btn)
        hbox_group.setLayout(hbox_layout)
        
        # GridLayout 예제
        grid_group = QGroupBox("QGridLayout (격자)")
        grid_layout = QGridLayout()
        
        positions = [(i, j) for i in range(3) for j in range(3)]
        for position in positions:
            btn = QPushButton(f"{position[0]},{position[1]}")
            grid_layout.addWidget(btn, *position)
        grid_group.setLayout(grid_layout)
        
        # 오른쪽 영역에 HBox와 Grid를 수직으로 배치
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(hbox_group)
        right_layout.addWidget(grid_group)
        right_widget.setLayout(right_layout)
        
        splitter.addWidget(right_widget)
        
        main_layout.addWidget(splitter)
        
        # FormLayout 예제
        form_group = QGroupBox("QFormLayout (폼)")
        form_layout = QFormLayout()
        
        form_layout.addRow("이름:", QLineEdit())
        form_layout.addRow("나이:", QSpinBox())
        form_layout.addRow("이메일:", QLineEdit())
        form_layout.addRow("국가:", QComboBox())
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        self.setLayout(main_layout)


class ListTreeTableTab(QWidget):
    """리스트, 트리, 테이블 위젯을 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("3. 리스트, 트리, 테이블 위젯 학습")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 상단 컨트롤
        control_layout = QHBoxLayout()
        
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("추가할 항목 입력")
        control_layout.addWidget(self.item_input)
        
        add_list_btn = QPushButton("리스트에 추가")
        add_list_btn.clicked.connect(self.add_to_list)
        control_layout.addWidget(add_list_btn)
        
        add_tree_btn = QPushButton("트리에 추가")
        add_tree_btn.clicked.connect(self.add_to_tree)
        control_layout.addWidget(add_tree_btn)
        
        add_table_btn = QPushButton("테이블에 추가")
        add_table_btn.clicked.connect(self.add_to_table)
        control_layout.addWidget(add_table_btn)
        
        layout.addLayout(control_layout)
        
        # 메인 스플리터
        main_splitter = QSplitter(Qt.Horizontal)
        
        # 리스트 위젯
        list_group = QGroupBox("QListWidget")
        list_layout = QVBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.addItems([f"리스트 항목 {i+1}" for i in range(5)])
        self.list_widget.itemClicked.connect(self.on_list_item_clicked)
        list_layout.addWidget(self.list_widget)
        
        list_control_layout = QHBoxLayout()
        remove_list_btn = QPushButton("선택 항목 삭제")
        remove_list_btn.clicked.connect(self.remove_from_list)
        clear_list_btn = QPushButton("전체 삭제")
        clear_list_btn.clicked.connect(self.list_widget.clear)
        list_control_layout.addWidget(remove_list_btn)
        list_control_layout.addWidget(clear_list_btn)
        list_layout.addLayout(list_control_layout)
        
        list_group.setLayout(list_layout)
        main_splitter.addWidget(list_group)
        
        # 트리 위젯
        tree_group = QGroupBox("QTreeWidget")
        tree_layout = QVBoxLayout()
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["항목", "설명"])
        
        # 초기 트리 항목들
        root1 = QTreeWidgetItem(["루트 1", "첫 번째 루트"])
        child1 = QTreeWidgetItem(["자식 1-1", "첫 번째 자식"])
        child2 = QTreeWidgetItem(["자식 1-2", "두 번째 자식"])
        root1.addChildren([child1, child2])
        
        root2 = QTreeWidgetItem(["루트 2", "두 번째 루트"])
        child3 = QTreeWidgetItem(["자식 2-1", "세 번째 자식"])
        root2.addChild(child3)
        
        self.tree_widget.addTopLevelItems([root1, root2])
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        tree_layout.addWidget(self.tree_widget)
        
        tree_control_layout = QHBoxLayout()
        expand_btn = QPushButton("모두 펼치기")
        expand_btn.clicked.connect(self.tree_widget.expandAll)
        collapse_btn = QPushButton("모두 접기")
        collapse_btn.clicked.connect(self.tree_widget.collapseAll)
        tree_control_layout.addWidget(expand_btn)
        tree_control_layout.addWidget(collapse_btn)
        tree_layout.addLayout(tree_control_layout)
        
        tree_group.setLayout(tree_layout)
        main_splitter.addWidget(tree_group)
        
        layout.addWidget(main_splitter)
        
        # 테이블 위젯
        table_group = QGroupBox("QTableWidget")
        table_layout = QVBoxLayout()
        
        self.table_widget = QTableWidget(4, 3)
        self.table_widget.setHorizontalHeaderLabels(["이름", "나이", "직업"])
        
        # 초기 데이터
        sample_data = [
            ["김철수", "25", "개발자"],
            ["이영희", "30", "디자이너"],
            ["박민수", "35", "기획자"],
            ["최지영", "28", "마케터"]
        ]
        
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row, col, item)
        
        self.table_widget.cellClicked.connect(self.on_table_cell_clicked)
        table_layout.addWidget(self.table_widget)
        
        table_control_layout = QHBoxLayout()
        add_row_btn = QPushButton("행 추가")
        add_row_btn.clicked.connect(self.add_table_row)
        remove_row_btn = QPushButton("선택 행 삭제")
        remove_row_btn.clicked.connect(self.remove_table_row)
        table_control_layout.addWidget(add_row_btn)
        table_control_layout.addWidget(remove_row_btn)
        table_layout.addLayout(table_control_layout)
        
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # 상태 표시
        self.status_label = QLabel("선택된 항목이 여기에 표시됩니다.")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def add_to_list(self):
        text = self.item_input.text().strip()
        if text:
            self.list_widget.addItem(text)
            self.item_input.clear()
    
    def add_to_tree(self):
        text = self.item_input.text().strip()
        if text:
            current = self.tree_widget.currentItem()
            if current:
                child = QTreeWidgetItem([text, "새로 추가된 항목"])
                current.addChild(child)
                current.setExpanded(True)
            else:
                root = QTreeWidgetItem([text, "새 루트 항목"])
                self.tree_widget.addTopLevelItem(root)
            self.item_input.clear()
    
    def add_to_table(self):
        text = self.item_input.text().strip()
        if text:
            self.add_table_row(text)
            self.item_input.clear()
    
    def remove_from_list(self):
        current_row = self.list_widget.currentRow()
        if current_row >= 0:
            self.list_widget.takeItem(current_row)
    
    def add_table_row(self, name="새 항목"):
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 0, QTableWidgetItem(name))
        self.table_widget.setItem(row_count, 1, QTableWidgetItem("0"))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem("미정"))
    
    def remove_table_row(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            self.table_widget.removeRow(current_row)
    
    def on_list_item_clicked(self, item):
        self.status_label.setText(f"리스트에서 선택됨: {item.text()}")
    
    def on_tree_item_clicked(self, item, column):
        self.status_label.setText(f"트리에서 선택됨: {item.text(0)} - {item.text(1)}")
    
    def on_table_cell_clicked(self, row, column):
        item = self.table_widget.item(row, column)
        text = item.text() if item else ""
        self.status_label.setText(f"테이블 셀 선택됨: ({row}, {column}) = {text}")


class DialogsTab(QWidget):
    """다이얼로그와 파일 처리를 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("4. 다이얼로그와 파일 처리 학습")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 메시지 다이얼로그 그룹
        msg_group = QGroupBox("메시지 다이얼로그")
        msg_layout = QGridLayout()
        
        info_btn = QPushButton("정보 메시지")
        info_btn.clicked.connect(self.show_info_message)
        msg_layout.addWidget(info_btn, 0, 0)
        
        warning_btn = QPushButton("경고 메시지")
        warning_btn.clicked.connect(self.show_warning_message)
        msg_layout.addWidget(warning_btn, 0, 1)
        
        error_btn = QPushButton("오류 메시지")
        error_btn.clicked.connect(self.show_error_message)
        msg_layout.addWidget(error_btn, 1, 0)
        
        question_btn = QPushButton("질문 메시지")
        question_btn.clicked.connect(self.show_question_message)
        msg_layout.addWidget(question_btn, 1, 1)
        
        msg_group.setLayout(msg_layout)
        layout.addWidget(msg_group)
        
        # 입력 다이얼로그 그룹
        input_group = QGroupBox("입력 다이얼로그")
        input_layout = QGridLayout()
        
        text_input_btn = QPushButton("텍스트 입력")
        text_input_btn.clicked.connect(self.get_text_input)
        input_layout.addWidget(text_input_btn, 0, 0)
        
        int_input_btn = QPushButton("숫자 입력")
        int_input_btn.clicked.connect(self.get_int_input)
        input_layout.addWidget(int_input_btn, 0, 1)
        
        item_input_btn = QPushButton("항목 선택")
        item_input_btn.clicked.connect(self.get_item_input)
        input_layout.addWidget(item_input_btn, 1, 0)
        
        double_input_btn = QPushButton("실수 입력")
        double_input_btn.clicked.connect(self.get_double_input)
        input_layout.addWidget(double_input_btn, 1, 1)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # 선택 다이얼로그 그룹
        selection_group = QGroupBox("선택 다이얼로그")
        selection_layout = QGridLayout()
        
        color_btn = QPushButton("색상 선택")
        color_btn.clicked.connect(self.select_color)
        selection_layout.addWidget(color_btn, 0, 0)
        
        font_btn = QPushButton("폰트 선택")
        font_btn.clicked.connect(self.select_font)
        selection_layout.addWidget(font_btn, 0, 1)
        
        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)
        
        # 파일 다이얼로그 그룹
        file_group = QGroupBox("파일 다이얼로그")
        file_layout = QGridLayout()
        
        open_file_btn = QPushButton("파일 열기")
        open_file_btn.clicked.connect(self.open_file)
        file_layout.addWidget(open_file_btn, 0, 0)
        
        save_file_btn = QPushButton("파일 저장")
        save_file_btn.clicked.connect(self.save_file)
        file_layout.addWidget(save_file_btn, 0, 1)
        
        open_dir_btn = QPushButton("폴더 선택")
        open_dir_btn.clicked.connect(self.open_directory)
        file_layout.addWidget(open_dir_btn, 1, 0)
        
        open_multiple_btn = QPushButton("여러 파일 선택")
        open_multiple_btn.clicked.connect(self.open_multiple_files)
        file_layout.addWidget(open_multiple_btn, 1, 1)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 커스텀 다이얼로그
        custom_dialog_btn = QPushButton("커스텀 다이얼로그")
        custom_dialog_btn.clicked.connect(self.show_custom_dialog)
        layout.addWidget(custom_dialog_btn)
        
        # 결과 표시 영역
        self.result_display = QTextEdit()
        self.result_display.setMaximumHeight(150)
        self.result_display.setReadOnly(True)
        layout.addWidget(QLabel("결과:"))
        layout.addWidget(self.result_display)
        
        self.setLayout(layout)
    
    def show_info_message(self):
        QMessageBox.information(self, "정보", "이것은 정보 메시지입니다.")
        self.result_display.append("정보 메시지가 표시되었습니다.")
    
    def show_warning_message(self):
        QMessageBox.warning(self, "경고", "이것은 경고 메시지입니다.")
        self.result_display.append("경고 메시지가 표시되었습니다.")
    
    def show_error_message(self):
        QMessageBox.critical(self, "오류", "이것은 오류 메시지입니다.")
        self.result_display.append("오류 메시지가 표시되었습니다.")
    
    def show_question_message(self):
        reply = QMessageBox.question(self, "질문", "계속 진행하시겠습니까?", 
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.result_display.append("사용자가 '예'를 선택했습니다.")
        else:
            self.result_display.append("사용자가 '아니오'를 선택했습니다.")
    
    def get_text_input(self):
        text, ok = QInputDialog.getText(self, "텍스트 입력", "이름을 입력하세요:")
        if ok and text:
            self.result_display.append(f"입력된 텍스트: {text}")
    
    def get_int_input(self):
        num, ok = QInputDialog.getInt(self, "숫자 입력", "나이를 입력하세요:", 25, 0, 150, 1)
        if ok:
            self.result_display.append(f"입력된 숫자: {num}")
    
    def get_double_input(self):
        num, ok = QInputDialog.getDouble(self, "실수 입력", "키를 입력하세요 (cm):", 170.0, 0.0, 300.0, 1)
        if ok:
            self.result_display.append(f"입력된 실수: {num}")
    
    def get_item_input(self):
        items = ["사과", "바나나", "오렌지", "포도", "딸기"]
        item, ok = QInputDialog.getItem(self, "항목 선택", "좋아하는 과일을 선택하세요:", items, 0, False)
        if ok and item:
            self.result_display.append(f"선택된 항목: {item}")
    
    def select_color(self):
        color = QColorDialog.getColor(Qt.white, self, "색상 선택")
        if color.isValid():
            self.result_display.append(f"선택된 색상: {color.name()}")
    
    def select_font(self):
        font, ok = QFontDialog.getFont(QFont("Arial", 12), self, "폰트 선택")
        if ok:
            self.result_display.append(f"선택된 폰트: {font.family()}, {font.pointSize()}pt")
    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 열기", "", 
                                                  "모든 파일 (*);;텍스트 파일 (*.txt);;이미지 파일 (*.png *.jpg *.jpeg)")
        if file_path:
            self.result_display.append(f"선택된 파일: {file_path}")
    
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "파일 저장", "", 
                                                  "텍스트 파일 (*.txt);;모든 파일 (*)")
        if file_path:
            self.result_display.append(f"저장할 파일: {file_path}")
    
    def open_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "폴더 선택")
        if dir_path:
            self.result_display.append(f"선택된 폴더: {dir_path}")
    
    def open_multiple_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "여러 파일 선택", "", 
                                                    "모든 파일 (*);;텍스트 파일 (*.txt)")
        if file_paths:
            self.result_display.append(f"선택된 파일들: {len(file_paths)}개")
            for path in file_paths[:3]:  # 처음 3개만 표시
                self.result_display.append(f"  - {path}")
            if len(file_paths) > 3:
                self.result_display.append(f"  ... 외 {len(file_paths) - 3}개")
    
    def show_custom_dialog(self):
        dialog = CustomDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name, age, email = dialog.get_data()
            self.result_display.append(f"커스텀 다이얼로그 결과: {name}, {age}세, {email}")


class CustomDialog(QDialog):
    """커스텀 다이얼로그 예제"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("사용자 정보 입력")
        self.setModal(True)
        self.resize(300, 200)
        
        layout = QVBoxLayout()
        
        # 폼 레이아웃
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        form_layout.addRow("이름:", self.name_edit)
        
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 150)
        self.age_spin.setValue(25)
        form_layout.addRow("나이:", self.age_spin)
        
        self.email_edit = QLineEdit()
        form_layout.addRow("이메일:", self.email_edit)
        
        layout.addLayout(form_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        ok_button = QPushButton("확인")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        return self.name_edit.text(), self.age_spin.value(), self.email_edit.text()


class ThreadsTimersTab(QWidget):
    """스레드와 타이머를 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("5. 스레드와 타이머 학습")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 타이머 그룹
        timer_group = QGroupBox("QTimer 예제")
        timer_layout = QVBoxLayout()
        
        # 현재 시간 표시
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 14))
        timer_layout.addWidget(self.time_label)
        
        # 타이머 컨트롤
        timer_control_layout = QHBoxLayout()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
        start_timer_btn = QPushButton("타이머 시작")
        start_timer_btn.clicked.connect(lambda: self.timer.start(1000))
        timer_control_layout.addWidget(start_timer_btn)
        
        stop_timer_btn = QPushButton("타이머 정지")
        stop_timer_btn.clicked.connect(self.timer.stop)
        timer_control_layout.addWidget(stop_timer_btn)
        
        timer_layout.addLayout(timer_control_layout)
        
        # 카운트다운 타이머
        countdown_layout = QHBoxLayout()
        
        self.countdown_spin = QSpinBox()
        self.countdown_spin.setRange(1, 60)
        self.countdown_spin.setValue(10)
        self.countdown_spin.setSuffix("초")
        countdown_layout.addWidget(QLabel("카운트다운:"))
        countdown_layout.addWidget(self.countdown_spin)
        
        self.countdown_label = QLabel("0")
        self.countdown_label.setFont(QFont("Arial", 16, QFont.Bold))
        countdown_layout.addWidget(self.countdown_label)
        
        start_countdown_btn = QPushButton("카운트다운 시작")
        start_countdown_btn.clicked.connect(self.start_countdown)
        countdown_layout.addWidget(start_countdown_btn)
        
        timer_layout.addLayout(countdown_layout)
        
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_value = 0
        
        timer_group.setLayout(timer_layout)
        layout.addWidget(timer_group)
        
        # 스레드 그룹
        thread_group = QGroupBox("QThread 예제")
        thread_layout = QVBoxLayout()
        
        # 진행률 표시
        self.thread_progress = QProgressBar()
        self.thread_progress.setRange(0, 100)
        thread_layout.addWidget(self.thread_progress)
        
        self.thread_status = QLabel("대기 중...")
        thread_layout.addWidget(self.thread_status)
        
        # 스레드 컨트롤
        thread_control_layout = QHBoxLayout()
        
        progress_thread_btn = QPushButton("진행률 작업 시작")
        progress_thread_btn.clicked.connect(lambda: self.start_thread_task("progress"))
        thread_control_layout.addWidget(progress_thread_btn)
        
        calc_thread_btn = QPushButton("계산 작업 시작")
        calc_thread_btn.clicked.connect(lambda: self.start_thread_task("calculation"))
        thread_control_layout.addWidget(calc_thread_btn)
        
        stop_thread_btn = QPushButton("작업 중지")
        stop_thread_btn.clicked.connect(self.stop_thread_task)
        thread_control_layout.addWidget(stop_thread_btn)
        
        thread_layout.addLayout(thread_control_layout)
        
        thread_group.setLayout(thread_layout)
        layout.addWidget(thread_group)
        
        # 애니메이션 그룹
        animation_group = QGroupBox("QPropertyAnimation 예제")
        animation_layout = QVBoxLayout()
        
        # 애니메이션 대상 버튼
        self.animation_button = QPushButton("애니메이션 버튼")
        self.animation_button.setFixedSize(200, 50)
        animation_layout.addWidget(self.animation_button)
        
        # 애니메이션 컨트롤
        animation_control_layout = QHBoxLayout()
        
        move_btn = QPushButton("이동 애니메이션")
        move_btn.clicked.connect(self.animate_move)
        animation_control_layout.addWidget(move_btn)
        
        resize_btn = QPushButton("크기 애니메이션")
        resize_btn.clicked.connect(self.animate_resize)
        animation_control_layout.addWidget(resize_btn)
        
        fade_btn = QPushButton("투명도 애니메이션")
        fade_btn.clicked.connect(self.animate_opacity)
        animation_control_layout.addWidget(fade_btn)
        
        animation_layout.addLayout(animation_control_layout)
        
        # 애니메이션 객체들
        self.move_animation = QPropertyAnimation(self.animation_button, b"geometry")
        self.resize_animation = QPropertyAnimation(self.animation_button, b"size")
        self.opacity_animation = QPropertyAnimation(self.animation_button, b"windowOpacity")
        
        animation_group.setLayout(animation_layout)
        layout.addWidget(animation_group)
        
        # 초기 시간 업데이트
        self.update_time()
        
        self.setLayout(layout)
    
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"현재 시간: {current_time}")
    
    def start_countdown(self):
        self.countdown_value = self.countdown_spin.value()
        self.countdown_label.setText(str(self.countdown_value))
        self.countdown_timer.start(1000)
    
    def update_countdown(self):
        self.countdown_value -= 1
        self.countdown_label.setText(str(self.countdown_value))
        if self.countdown_value <= 0:
            self.countdown_timer.stop()
            self.countdown_label.setText("완료!")
            QMessageBox.information(self, "알림", "카운트다운이 완료되었습니다!")
    
    def start_thread_task(self, task_type):
        if self.worker_thread and self.worker_thread.isRunning():
            QMessageBox.warning(self, "경고", "이미 작업이 실행 중입니다.")
            return
        
        self.worker_thread = WorkerThread(task_type)
        self.worker_thread.progress_updated.connect(self.thread_progress.setValue)
        self.worker_thread.task_completed.connect(self.on_thread_completed)
        self.worker_thread.start()
        
        self.thread_status.setText(f"{task_type} 작업 실행 중...")
        self.thread_progress.setValue(0)
    
    def stop_thread_task(self):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
            self.thread_status.setText("작업이 중지되었습니다.")
    
    def on_thread_completed(self, message):
        self.thread_status.setText(message)
        QMessageBox.information(self, "완료", message)
    
    def animate_move(self):
        start_rect = self.animation_button.geometry()
        end_rect = QRect(start_rect.x() + 100, start_rect.y(), start_rect.width(), start_rect.height())
        
        self.move_animation.setDuration(1000)
        self.move_animation.setStartValue(start_rect)
        self.move_animation.setEndValue(end_rect)
        self.move_animation.setEasingCurve(QEasingCurve.OutBounce)
        self.move_animation.start()
    
    def animate_resize(self):
        start_size = self.animation_button.size()
        end_size = QSize(start_size.width() + 50, start_size.height() + 20)
        
        self.resize_animation.setDuration(1000)
        self.resize_animation.setStartValue(start_size)
        self.resize_animation.setEndValue(end_size)
        self.resize_animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.resize_animation.start()
    
    def animate_opacity(self):
        self.opacity_animation.setDuration(2000)
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setKeyValueAt(0.5, 0.1)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()


class GraphicsTab(QWidget):
    """그래픽스와 드로잉을 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("6. 그래픽스와 드로잉 학습")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 컨트롤 패널
        control_layout = QHBoxLayout()
        
        add_rect_btn = QPushButton("사각형 추가")
        add_rect_btn.clicked.connect(self.add_rectangle)
        control_layout.addWidget(add_rect_btn)
        
        add_circle_btn = QPushButton("원 추가")
        add_circle_btn.clicked.connect(self.add_circle)
        control_layout.addWidget(add_circle_btn)
        
        add_text_btn = QPushButton("텍스트 추가")
        add_text_btn.clicked.connect(self.add_text)
        control_layout.addWidget(add_text_btn)
        
        clear_btn = QPushButton("모두 지우기")
        clear_btn.clicked.connect(self.clear_scene)
        control_layout.addWidget(clear_btn)
        
        layout.addLayout(control_layout)
        
        # 그래픽스 뷰
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        
        # 씬 크기 설정
        self.graphics_scene.setSceneRect(0, 0, 400, 300)
        
        layout.addWidget(self.graphics_view)
        
        # 상태 정보
        self.graphics_status = QLabel("그래픽 항목: 0개")
        layout.addWidget(self.graphics_status)
        
        self.setLayout(layout)
        
        # 초기 항목들 추가
        self.add_rectangle()
        self.add_circle()
        self.add_text()
    
    def add_rectangle(self):
        import random
        
        rect = QGraphicsRectItem(
            random.randint(10, 300),
            random.randint(10, 200),
            random.randint(30, 100),
            random.randint(30, 80)
        )
        
        # 랜덤 색상
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        rect.setBrush(QBrush(color))
        rect.setPen(QPen(Qt.black, 2))
        
        self.graphics_scene.addItem(rect)
        self.update_status()
    
    def add_circle(self):
        import random
        
        circle = QGraphicsEllipseItem(
            random.randint(10, 300),
            random.randint(10, 200),
            random.randint(30, 100),
            random.randint(30, 100)
        )
        
        # 랜덤 색상
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        circle.setBrush(QBrush(color))
        circle.setPen(QPen(Qt.black, 2))
        
        self.graphics_scene.addItem(circle)
        self.update_status()
    
    def add_text(self):
        import random
        
        text_item = QGraphicsTextItem(f"텍스트 {len(self.graphics_scene.items()) + 1}")
        text_item.setPos(random.randint(10, 300), random.randint(10, 250))
        
        # 랜덤 색상
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        text_item.setDefaultTextColor(color)
        
        font = QFont("Arial", random.randint(12, 24))
        text_item.setFont(font)
        
        self.graphics_scene.addItem(text_item)
        self.update_status()
    
    def clear_scene(self):
        self.graphics_scene.clear()
        self.update_status()
    
    def update_status(self):
        count = len(self.graphics_scene.items())
        self.graphics_status.setText(f"그래픽 항목: {count}개")


class DatabaseTab(QWidget):
    """데이터베이스 연동을 학습하는 탭"""
    
    def __init__(self):
        super().__init__()
        self.db_path = "learning_project.db"
        self.init_db()
        self.init_ui()
        self.load_data()
    
    def init_db(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 샘플 데이터 추가 (테이블이 비어있는 경우에만)
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            sample_users = [
                ('김철수', 25, 'kim@example.com'),
                ('이영희', 30, 'lee@example.com'),
                ('박민수', 35, 'park@example.com'),
                ('최지영', 28, 'choi@example.com')
            ]
            cursor.executemany('INSERT INTO users (name, age, email) VALUES (?, ?, ?)', sample_users)
        
        conn.commit()
        conn.close()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("7. 데이터베이스 연동 학습 (SQLite)")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 입력 폼
        form_group = QGroupBox("사용자 추가/수정")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        form_layout.addRow("이름:", self.name_input)
        
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        form_layout.addRow("나이:", self.age_input)
        
        self.email_input = QLineEdit()
        form_layout.addRow("이메일:", self.email_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 버튼들
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("추가")
        add_btn.clicked.connect(self.add_user)
        button_layout.addWidget(add_btn)
        
        update_btn = QPushButton("수정")
        update_btn.clicked.connect(self.update_user)
        button_layout.addWidget(update_btn)
        
        delete_btn = QPushButton("삭제")
        delete_btn.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton("새로고침")
        refresh_btn.clicked.connect(self.load_data)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        # 검색
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("검색:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("이름 또는 이메일로 검색")
        self.search_input.textChanged.connect(self.search_users)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # 데이터 테이블
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(["ID", "이름", "나이", "이메일", "생성일"])
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.cellClicked.connect(self.on_table_cell_clicked)
        layout.addWidget(self.data_table)
        
        # 상태 표시
        self.db_status = QLabel()
        layout.addWidget(self.db_status)
        
        self.setLayout(layout)
    
    def load_data(self, search_term=None):
        """데이터베이스에서 데이터 로드"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if search_term:
            cursor.execute('''
                SELECT * FROM users 
                WHERE name LIKE ? OR email LIKE ? 
                ORDER BY created_at DESC
            ''', (f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        
        rows = cursor.fetchall()
        
        self.data_table.setRowCount(len(rows))
        
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                if col_idx == 4:  # 날짜 포맷팅
                    try:
                        dt = datetime.fromisoformat(data)
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                        item = QTableWidgetItem(formatted_date)
                    except:
                        item = QTableWidgetItem(str(data))
                else:
                    item = QTableWidgetItem(str(data))
                
                self.data_table.setItem(row_idx, col_idx, item)
        
        conn.close()
        self.db_status.setText(f"총 {len(rows)}개의 레코드")
    
    def add_user(self):
        """사용자 추가"""
        name = self.name_input.text().strip()
        age = self.age_input.value()
        email = self.email_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "경고", "이름을 입력해주세요.")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (name, age, email) VALUES (?, ?, ?)', 
                          (name, age, email))
            conn.commit()
            QMessageBox.information(self, "성공", "사용자가 추가되었습니다.")
            self.clear_form()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "오류", f"데이터베이스 오류: {e}")
        finally:
            conn.close()
    
    def update_user(self):
        """선택된 사용자 수정"""
        current_row = self.data_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "수정할 행을 선택해주세요.")
            return
        
        user_id = self.data_table.item(current_row, 0).text()
        name = self.name_input.text().strip()
        age = self.age_input.value()
        email = self.email_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "경고", "이름을 입력해주세요.")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE users SET name=?, age=?, email=? WHERE id=?', 
                          (name, age, email, user_id))
            conn.commit()
            QMessageBox.information(self, "성공", "사용자 정보가 수정되었습니다.")
            self.clear_form()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "오류", f"데이터베이스 오류: {e}")
        finally:
            conn.close()
    
    def delete_user(self):
        """선택된 사용자 삭제"""
        current_row = self.data_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 행을 선택해주세요.")
            return
        
        user_id = self.data_table.item(current_row, 0).text()
        user_name = self.data_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, "확인", 
                                   f"'{user_name}' 사용자를 삭제하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
                conn.commit()
                QMessageBox.information(self, "성공", "사용자가 삭제되었습니다.")
                self.load_data()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "오류", f"데이터베이스 오류: {e}")
            finally:
                conn.close()
    
    def search_users(self):
        """사용자 검색"""
        search_term = self.search_input.text().strip()
        self.load_data(search_term if search_term else None)
    
    def on_table_cell_clicked(self, row, column):
        """테이블 셀 클릭 시 폼에 데이터 로드"""
        if row >= 0:
            name = self.data_table.item(row, 1).text()
            age = int(self.data_table.item(row, 2).text())
            email = self.data_table.item(row, 3).text()
            
            self.name_input.setText(name)
            self.age_input.setValue(age)
            self.email_input.setText(email)
    
    def clear_form(self):
        """입력 폼 초기화"""
        self.name_input.clear()
        self.age_input.setValue(0)
        self.email_input.clear()


class TextEditorWidget(QTextEdit):
    """A QTextEdit widget that accepts dropped files and emits a signal."""
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # For simplicity, we only open the first file dropped.
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path:
                self.fileDropped.emit(file_path)
        else:
            super().dropEvent(event)


class MainWindow(QMainWindow):
    """메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comprehensive PySide6 Widgets Demo")

        # --- Actions ---
        self._create_actions()

        # --- Menu Bar, Tool Bar, and Status Bar ---
        self._create_menu_bar()
        self._create_tool_bar()
        self.statusBar().showMessage("Ready")

        # --- Main layout and central widget ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # --- Text Editor Part ---
        editor_group_box = QGroupBox("Simple Text Editor (Drag & Drop a file here)")
        editor_layout = QVBoxLayout()
        self.text_edit = TextEditorWidget()
        self.text_edit.setPlaceholderText("File content will be shown here...")
        editor_layout.addWidget(self.text_edit)
        editor_group_box.setLayout(editor_layout)

        # --- Top Part: Basic Interactions ---
        top_group_box = QGroupBox("Basic Interactions")
        top_layout = QVBoxLayout()
        self.status_label = QLabel("Welcome! Interact with the widgets.")
        self.line_edit = QLineEdit("Type here to update the label")
        update_button = QPushButton("Update Text from Input")
        top_layout.addWidget(self.status_label)
        top_layout.addWidget(self.line_edit)
        top_layout.addWidget(update_button)
        top_group_box.setLayout(top_layout)

        # --- Middle Part: Various Widgets Showcase ---
        widgets_group_box = QGroupBox("More Widgets Showcase")
        grid_layout = QGridLayout()
        checkbox = QCheckBox("Toggle Me")
        grid_layout.addWidget(QLabel("QCheckBox:"), 0, 0)
        grid_layout.addWidget(checkbox, 0, 1)
        rb_group = QGroupBox("QRadioButton")
        rb_layout = QHBoxLayout()
        self.rb1 = QRadioButton("Option A")
        self.rb2 = QRadioButton("Option B")
        self.rb1.setChecked(True)
        rb_layout.addWidget(self.rb1)
        rb_layout.addWidget(self.rb2)
        rb_group.setLayout(rb_layout)
        grid_layout.addWidget(rb_group, 1, 0, 1, 2)
        combo = QComboBox()
        combo.addItems(["Item 1", "Item 2", "Item 3"])
        grid_layout.addWidget(QLabel("QComboBox:"), 2, 0)
        grid_layout.addWidget(combo, 2, 1)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        grid_layout.addWidget(QLabel("QSlider:"), 3, 0)
        grid_layout.addWidget(slider, 3, 1)
        widgets_group_box.setLayout(grid_layout)

        # --- Bottom Part: Model/View Demo ---
        mv_group_box = QGroupBox("Model/View Demo (QListView)")
        mv_layout = QVBoxLayout()
        self.list_view = QListView()
        self.list_model = QStringListModel(["Apple", "Banana", "Cherry"])
        self.list_view.setModel(self.list_model)
        mv_layout.addWidget(self.list_view)
        add_item_layout = QHBoxLayout()
        self.new_item_edit = QLineEdit()
        add_item_button = QPushButton("Add")
        add_item_layout.addWidget(self.new_item_edit)
        add_item_layout.addWidget(add_item_button)
        mv_layout.addLayout(add_item_layout)
        delete_item_button = QPushButton("Delete Selected")
        mv_layout.addWidget(delete_item_button)
        mv_group_box.setLayout(mv_layout)
        
        # Add group boxes to the main layout
        main_layout.addWidget(editor_group_box)
        main_layout.addWidget(top_group_box)
        main_layout.addWidget(widgets_group_box)
        main_layout.addWidget(mv_group_box)
        
        # --- Connect Signals to Slots ---
        update_button.clicked.connect(self.update_label_from_input)
        checkbox.toggled.connect(self.checkbox_toggled)
        self.rb1.toggled.connect(self.radio_button_toggled)
        combo.currentTextChanged.connect(self.combo_box_changed)
        slider.valueChanged.connect(self.slider_value_changed)
        add_item_button.clicked.connect(self.add_item)
        delete_item_button.clicked.connect(self.delete_item)
        self.list_view.selectionModel().selectionChanged.connect(
            lambda: delete_item_button.setEnabled(self.list_view.selectionModel().hasSelection())
        )
        delete_item_button.setEnabled(False)

        # Drag and drop connection
        self.text_edit.fileDropped.connect(self.load_file)

    def _create_actions(self):
        open_icon = self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon)
        self.open_action = QAction(QIcon(open_icon), "&Open...", self)
        self.open_action.triggered.connect(self.open_file)

        save_icon = self.style().standardIcon(self.style().StandardPixmap.SP_DialogSaveButton)
        self.save_action = QAction(QIcon(save_icon), "&Save...", self)
        self.save_action.triggered.connect(self.save_file)

        exit_icon = self.style().standardIcon(self.style().StandardPixmap.SP_DialogCloseButton)
        self.exit_action = QAction(QIcon(exit_icon), "&Exit", self)
        self.exit_action.triggered.connect(self.close)
        
        about_icon = self.style().standardIcon(self.style().StandardPixmap.SP_DialogHelpButton)
        self.about_action = QAction(QIcon(about_icon), "&About", self)
        self.about_action.triggered.connect(self.show_about_dialog)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _create_tool_bar(self):
        tool_bar = QToolBar("Main Tool Bar")
        self.addToolBar(tool_bar)
        tool_bar.addAction(self.open_action)
        tool_bar.addAction(self.save_action)
        tool_bar.addSeparator()
        tool_bar.addAction(self.exit_action)
        tool_bar.addAction(self.about_action)

    def show_about_dialog(self):
        about_text = "This is a comprehensive demo of PySide6 widgets."
        QMessageBox.about(self, "About This App", about_text)

    def update_label_from_input(self):
        text = self.line_edit.text()
        new_text = text if text else "Input is empty."
        self.status_label.setText(new_text)
        self.statusBar().showMessage(f"Updated text from input: {text}", 2000)

    def checkbox_toggled(self, checked):
        status = "Checked" if checked else "Unchecked"
        message = f"CheckBox is {status}"
        self.status_label.setText(message)
        self.statusBar().showMessage(message, 2000)

    def radio_button_toggled(self):
        if self.rb1.isChecked():
            message = "Radio Button 'Option A' selected"
        else:
            message = "Radio Button 'Option B' selected"
        self.status_label.setText(message)
        self.statusBar().showMessage(message, 2000)

    def combo_box_changed(self, text):
        message = f"ComboBox selection: {text}"
        self.status_label.setText(message)
        self.statusBar().showMessage(message, 2000)

    def slider_value_changed(self, value):
        message = f"Slider value: {value}"
        self.status_label.setText(message)
        self.statusBar().showMessage(message, 2000)

    def add_item(self):
        text = self.new_item_edit.text().strip()
        if not text:
            return
        row = self.list_model.rowCount()
        self.list_model.insertRow(row)
        index = self.list_model.index(row)
        self.list_model.setData(index, text)
        self.new_item_edit.clear()
        self.statusBar().showMessage(f"Added item: {text}", 2000)

    def delete_item(self):
        indexes = self.list_view.selectedIndexes()
        if not indexes:
            return
        index = indexes[0]
        item_text = self.list_model.data(index, Qt.ItemDataRole.DisplayRole)
        self.list_model.removeRow(index.row())
        self.statusBar().showMessage(f"Deleted item: {item_text}", 2000)

    def load_file(self, file_name):
        if not file_name:
            return
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_edit.setText(content)
            self.statusBar().showMessage(f"Opened '{file_name}'", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            self.load_file(file_name)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.statusBar().showMessage(f"Saved to '{file_name}'", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
