
# 코드의 주요 특징
-  구조화된 레이아웃: 
QGroupBox를 사용하여 관련된 위젯들을 "Basic Interactions"와 "More Widgets Showcase" 두 그룹으로 묶었습니다.   
전체적으로는 QVBoxLayout을, 위젯이 많은 하단부는 QGridLayout을 사용하여 체계적으로 배치했습니다.  

-  다양한 위젯 추가:
  - QCheckBox: 체크하거나 해제할 수 있는 박스입니다.  
  - QRadioButton: 그룹 내에서 하나만 선택 가능하며, QHBoxLayout을 이용해 가로로 배치했습니다.  
  - QComboBox: 여러 항목 중 하나를 선택하는 드롭다운 메뉴입니다.  
  - QSlider: 마우스로 드래그하여 0부터 100까지의 값을 선택할 수 있는 슬라이더입니다.  

## 중앙 상태 라벨: 
상단에 있는 status_label(QLabel)이 모든 위젯의 현재 상태를 표시하는 역할을 합니다.  
어떤 위젯을 조작하든 그 결과가 이 라벨에 텍스트로 나타나므로, 각 위젯의 시그널이 어떻게 작동하는지 명확하게 확인할 수 있습니다.  

## 정리된 시그널-슬롯 연결: 
__init__ 메서드의 마지막 부분에서 모든 시그널과 슬롯의 연결을 한곳에 모아 관리하므로 코드의 가독성이 좋습니다.  
이 예제를 통해 PySide6의 기본적인 위젯 대부분과 레이아웃 관리, 그리고 시그널-슬롯 메커니즘을 효과적으로 학습하실 수 있을 겁니다.  

_create_actions 메서드:
QAction 객체를 생성합니다. QAction은 메뉴 항목, 툴바 버튼 등이 공유할 수 있는 '동작'입니다. "Exit"와 "About" 두 가지 액션을 만들었습니다.
self.style().standardIcon(...)을 사용하여 Qt에 내장된 표준 아이콘을 찾아 액션에 아이콘을 추가했습니다.
각 액션의 triggered 시그널을 self.close (창 닫기), self.show_about_dialog (다이얼로그 표시) 같은 슬롯에 연결했습니다.
_create_menu_bar 와 _create_tool_bar 메서드:
self.menuBar()를 호출하여 메뉴바를 가져오고, addMenu()로 "File", "Help" 메뉴를 추가한 뒤, addAction()으로 미리 만들어 둔 액션을 추가합니다. &File의 &는 단축키(Alt+F)를 지정하는 역할을 합니다.
QToolBar를 생성하고 addToolBar()로 메인 윈도우에 추가한 뒤, 마찬가지로 addAction()으로 액션을 추가하여 아이콘 버튼을 만듭니다.
상태바 (statusBar):
__init__에서 self.statusBar().showMessage("Ready")를 호출하여 초기 메시지를 설정했습니다.
각 위젯의 상태가 변경되는 슬롯 함수(예: checkbox_toggled) 안에서 self.statusBar().showMessage("...", 2000) 코드를 추가했습니다. 이는 메시지를 2000밀리초(2초) 동안 보여준 뒤 사라지게 하여, 사용자에게 실시간 피드백을 제공합니다.
show_about_dialog 메서드:
QMessageBox.about()이라는 정적 메서드를 사용하여 간단한 정보 다이얼로그를 쉽게 생성합니다. "Help" > "About" 메뉴나 툴바의 'About' 아이콘을 클릭하면 이 메서드가 호출됩니다.
