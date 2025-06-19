#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 계산기 애플리케이션
PyInstaller 배포 예제용
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("간단한 계산기")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # 현재 입력값
        self.current = "0"
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # 결과 표시 영역
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(expand=True, fill="both")
        
        self.display = tk.Entry(
            self.display_frame,
            font=("Arial", 16),
            textvariable=tk.StringVar(value=self.current),
            state="readonly",
            justify="right"
        )
        self.display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 버튼 프레임
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="both", expand=True)
        
        # 버튼 생성
        self.create_buttons()
        
    def create_buttons(self):
        # 버튼 레이아웃
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if i == 4 and j == 0:  # '0' 버튼은 2칸 차지
                    btn = tk.Button(
                        self.button_frame,
                        text=btn_text,
                        font=("Arial", 14),
                        command=lambda t=btn_text: self.on_button_click(t)
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=1, pady=1)
                elif i == 4 and j == 1:  # '0' 버튼 다음은 건너뛰기
                    continue
                else:
                    btn = tk.Button(
                        self.button_frame,
                        text=btn_text,
                        font=("Arial", 14),
                        command=lambda t=btn_text: self.on_button_click(t)
                    )
                    if i == 4 and j >= 2:  # '.' 과 '=' 버튼 위치 조정
                        btn.grid(row=i, column=j-1, sticky="nsew", padx=1, pady=1)
                    else:
                        btn.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
        
        # 격자 가중치 설정
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.button_frame.grid_columnconfigure(j, weight=1)
    
    def on_button_click(self, char):
        if self.result:
            self.current = "0"
            self.input_value = True
            self.result = False
        
        if char in "0123456789":
            self.number_press(char)
        elif char == ".":
            self.decimal_press()
        elif char in "+-×÷":
            self.operation_press(char)
        elif char == "=":
            self.equal_press()
        elif char == "C":
            self.clear_press()
        elif char == "±":
            self.sign_press()
        elif char == "%":
            self.percent_press()
        
        self.update_display()
    
    def number_press(self, num):
        if self.input_value:
            if self.current == "0":
                self.current = num
            else:
                self.current += num
        else:
            self.current = num
            self.input_value = True
    
    def decimal_press(self):
        if self.input_value:
            if "." not in self.current:
                self.current += "."
        else:
            self.current = "0."
            self.input_value = True
    
    def operation_press(self, op):
        if not self.input_value:
            if self.op:
                self.equal_press()
        else:
            self.total = float(self.current)
            self.input_value = False
        
        self.check_sum = True
        self.op = op
    
    def equal_press(self):
        if self.op and self.input_value:
            try:
                if self.op == "+":
                    self.total += float(self.current)
                elif self.op == "-":
                    self.total -= float(self.current)
                elif self.op == "×":
                    self.total *= float(self.current)
                elif self.op == "÷":
                    if float(self.current) == 0:
                        messagebox.showerror("오류", "0으로 나눌 수 없습니다!")
                        return
                    self.total /= float(self.current)
                
                self.current = str(self.total)
                self.input_value = False
                self.check_sum = False
                self.op = ""
                self.result = True
                
                # 정수인 경우 소수점 제거
                if self.current.endswith('.0'):
                    self.current = self.current[:-2]
                    
            except Exception as e:
                messagebox.showerror("오류", f"계산 중 오류가 발생했습니다: {str(e)}")
    
    def clear_press(self):
        self.current = "0"
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False
    
    def sign_press(self):
        if self.current != "0":
            if self.current[0] == "-":
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
    
    def percent_press(self):
        self.current = str(float(self.current) / 100)
        if self.current.endswith('.0'):
            self.current = self.current[:-2]
    
    def update_display(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current)
        self.display.config(state="readonly")

def main():
    # 프로그램 정보 출력
    print("=" * 50)
    print("간단한 계산기 v1.0")
    print("PyInstaller 배포 예제")
    print("=" * 50)
    
    # 실행 경로 확인 (PyInstaller로 패키징된 경우와 개발 환경 구분)
    if getattr(sys, 'frozen', False):
        # PyInstaller로 패키징된 경우
        application_path = os.path.dirname(sys.executable)
        print(f"실행 파일 경로: {application_path}")
    else:
        # 개발 환경에서 실행된 경우
        application_path = os.path.dirname(os.path.abspath(__file__))
        print(f"스크립트 경로: {application_path}")
    
    # GUI 생성 및 실행
    root = tk.Tk()
    app = Calculator(root)
    
    # 창 중앙 배치
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    print("계산기 GUI 시작")
    root.mainloop()
    print("프로그램 종료")

if __name__ == "__main__":
    main()