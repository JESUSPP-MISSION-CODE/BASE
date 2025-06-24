
# 코드의 주요 특징
-  구조화된 레이아웃:   
QGroupBox를 사용하여 관련된 위젯들을 "Basic Interactions"와 "More Widgets Showcase" 두 그룹으로 묶었습니다.   
전체적으로는 QVBoxLayout을, 위젯이 많은 하단부는 QGridLayout을 사용하여 체계적으로 배치했습니다.  

-  다양한 위젯 추가:
    - QCheckBox: 체크하거나 해제할 수 있는 박스입니다.  
    - QRadioButton: 그룹 내에서 하나만 선택 가능하며, QHBoxLayout을 이용해 가로로 배치했습니다.  
    - QComboBox: 여러 항목 중 하나를 선택하는 드롭다운 메뉴입니다.  
    - QSlider: 마우스로 드래그하여 0부터 100까지의 값을 선택할 수 있는 슬라이더입니다.  

-  중앙 상태 라벨:   
상단에 있는 status_label(QLabel)이 모든 위젯의 현재 상태를 표시하는 역할을 합니다.  
어떤 위젯을 조작하든 그 결과가 이 라벨에 텍스트로 나타나므로, 각 위젯의 시그널이 어떻게 작동하는지 명확하게 확인할 수 있습니다.  

- 정리된 시그널-슬롯 연결:   
__init__ 메서드의 마지막 부분에서 모든 시그널과 슬롯의 연결을 한곳에 모아 관리하므로 코드의 가독성이 좋습니다.  
이 예제를 통해 PySide6의 기본적인 위젯 대부분과 레이아웃 관리, 그리고 시그널-슬롯 메커니즘을 효과적으로 학습하실 수 있을 겁니다.  


# 창 상단에 메뉴바와 툴바가, 하단에는 상태바가 추가
- _create_actions 메서드:  
    - QAction 객체를 생성합니다. QAction은 메뉴 항목, 툴바 버튼 등이 공유할 수 있는 '동작'입니다. "Exit"와 "About" 두 가지 액션을 만들었습니다.
    - self.style().standardIcon(...)을 사용하여 Qt에 내장된 표준 아이콘을 찾아 액션에 아이콘을 추가했습니다.
각 액션의 triggered 시그널을 self.close (창 닫기), self.show_about_dialog (다이얼로그 표시) 같은 슬롯에 연결했습니다.

- _create_menu_bar 와 _create_tool_bar 메서드:  
    - self.menuBar()를 호출하여 메뉴바를 가져오고, addMenu()로 "File", "Help" 메뉴를 추가한 뒤, addAction()으로 미리 만들어 둔 액션을 추가합니다. &File의 &는 단축키(Alt+F)를 지정하는 역할을 합니다.
    - QToolBar를 생성하고 addToolBar()로 메인 윈도우에 추가한 뒤, 마찬가지로 addAction()으로 액션을 추가하여 아이콘 버튼을 만듭니다.
      
- 상태바 (statusBar):  
    - __init__에서 self.statusBar().showMessage("Ready")를 호출하여 초기 메시지를 설정했습니다.
    - 각 위젯의 상태가 변경되는 슬롯 함수(예: checkbox_toggled) 안에서 self.statusBar().showMessage("...", 2000) 코드를 추가했습니다. 이는 메시지를 2000밀리초(2초) 동안 보여준 뒤 사라지게 하여, 사용자에게 실시간 피드백을 제공합니다.
      
- show_about_dialog 메서드:
    - QMessageBox.about()이라는 정적 메서드를 사용하여 간단한 정보 다이얼로그를 쉽게 생성합니다. "Help" > "About" 메뉴나 툴바의 'About' 아이콘을 클릭하면 이 메서드가 호출됩니다.
 
# 기본적인 모델/뷰 예제인 QListView와 QStringListModel을 사용하여 이 아키텍처를 애플리케이션에 추가
## 핵심 개념:
- 모델 (Model): 데이터 자체와 데이터 구조를 관리합니다. (예: 문자열 목록)
- 뷰 (View): 모델의 데이터를 사용자에게 보여주는 방법을 결정합니다. (예: 간단한 목록, 표, 트리)
- 컨트롤러 (Controller) 로직: 사용자 입력을 받아 모델을 변경합니다. 뷰는 모델이 변경되면 자동으로 업데이트됩니다.
<br>

- 모델/뷰 분리: QListView (뷰)는 데이터를 어떻게 보여줄지만 담당하고, QStringListModel (모델)은 실제 데이터("Apple", "Banana", "Cherry" 등)를 소유하고 관리합니다.
- 컨트롤러 로직 구현:
    - add_item 슬롯: "Add" 버튼을 누르면 QLineEdit의 텍스트를 가져와 모델에 직접 새 항목을 추가합니다. 뷰(QListView)를 직접 수정하지 않습니다.
    - delete_item 슬롯: "Delete Selected" 버튼을 누르면 뷰에서 선택된 항목의 인덱스를 가져와 모델에서 해당 행을 삭제합니다. 역시 모델만 변경합니다.
- 자동 업데이트: 모델이 변경되면(항목이 추가되거나 삭제되면), 뷰는 이 변경을 자동으로 감지하고 자신의 모습을 즉시 업데이트합니다. 이것이 모델/뷰 아키텍처의 가장 큰 장점입니다.
- UI 개선: 목록에서 아무것도 선택하지 않으면 "Delete Selected" 버튼이 비활성화됩니다. selectionChanged 시그널을 사용하여 선택 상태가 바뀔 때마다 버튼의 활성화 여부를 동적으로 제어합니다.

# 파일 열기 및 저장 기능을 추가

1. QTextEdit 위젯 추가: 여러 줄의 텍스트를 편집할 수 있는 위젯을 "Text Editor"라는 새 그룹 상자 안에 배치합니다.
2. "Open" 및 "Save" 액션 생성: 파일 메뉴와 툴바에서 사용할 "열기"와 "저장" 액션(QAction)을 정의합니다.
3. 파일 다이얼로그 (QFileDialog): "Open" 또는 "Save" 액션을 실행했을 때, 사용자가 파일을 선택하거나 저장할 위치를 지정할 수 있는 시스템 기본 파일 창을 띄웁니다.
4. 파일 입출력 로직 구현:
    - open_file 슬롯: 사용자가 선택한 텍스트 파일의 내용을 읽어와 QTextEdit에 표시합니다.
    - save_file 슬롯: QTextEdit에 있는 현재 내용을 사용자가 지정한 텍스트 파일에 저장합니다.

<br>

- QTextEdit 추가: 애플리케이션의 최상단에 "Simple Text Editor" 그룹이 생겼고, 그 안에 여러 줄의 텍스트를 담을 수 있는 QTextEdit 위젯을 배치했습니다.
- 새로운 액션과 슬롯:
    - _create_actions 메서드에 open_action과 save_action을 추가하고, 각각 open_file과 save_file이라는 새로운 슬롯에 연결했습니다.
    - 이 액션들은 "File" 메뉴와 툴바에도 추가되어 쉽게 접근할 수 있습니다.
- open_file 메서드:
    - QFileDialog.getOpenFileName()을 호출하여 파일 열기 대화상자를 띄웁니다.
    - 사용자가 파일을 선택하면, 해당 파일의 경로를 읽어 QTextEdit 위젯에 파일 내용을 표시합니다. (현재 구현은 파일 경로를 표시하도록 되어 있네요. 실제 내용을 읽어오도록 수정할 수 있습니다.)
    - 상태바에 작업 완료 메시지를 표시합니다.
- save_file 메서드:
    - QFileDialog.getSaveFileName()을 호출하여 파일 저장 대화상자를 띄웁니다.
    - 사용자가 파일 이름과 위치를 지정하면, QTextEdit 위젯의 전체 텍스트(toPlainText())를 가져와 해당 파일에 utf-8 인코딩으로 저장합니다.
    - 마찬가지로 상태바에 완료 메시지를 띄웁니다.
