# APP4 Enhanced FSM Football Planner with Custom Modern GUI
import sys
import random
import json
import csv
import os
from dataclasses import dataclass, field
from typing import List, Optional
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox, QFileDialog, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QPalette
from PyQt5.QtWidgets import QToolButton, QSizePolicy

# === FSM Core Models ===
@dataclass
class FSMState:
    name: str
    action: str
    success_transition: Optional[str] = None
    failure_transition: Optional[str] = None
    success_prob: float = 1.0

    def to_dict(self):
        return self.__dict__

@dataclass
class FSMachine:
    initial_state: str
    states: List[FSMState] = field(default_factory=list)

    def get_state(self, name: str) -> Optional[FSMState]:
        for state in self.states:
            if state.name == name:
                return state
        return None

# === Parsing Logic ===
TASKS_MAPPING = {
    'pass': ['GO_TO_BALL', 'ALIGNMENT', 'PASS'],
    'block': ['GO_TO_BALL', 'BLOCK'],
    'shoot': ['GO_TO_BALL', 'ALIGNMENT', 'SHOOT']
}

def decode_instruction(instruction: str) -> List[str]:
    instruction = instruction.lower()
    task_flow = []
    for key, actions in TASKS_MAPPING.items():
        count = instruction.count(key)
        for _ in range(count):
            task_flow.extend(actions)
            instruction = instruction.replace(key, '', 1)
    return task_flow

# === FSM Construction ===
def construct_fsm(tasks: List[str]) -> FSMachine:
    states = []
    for i, task in enumerate(tasks):
        sname = f"Q{i}"
        success = f"Q{i+1}" if i + 1 < len(tasks) else "GOAL_STATE"
        failure = f"FAIL_{task.upper()}"
        prob = round(random.uniform(0.85, 0.95), 2)
        states.append(FSMState(sname, task, success, failure, prob))

    states.append(FSMState("GOAL_STATE", "GOAL_COMPLETE"))
    for task in set(tasks):
        states.append(FSMState(f"FAIL_{task.upper()}", f"FAILED_{task.upper()}", success_prob=1.0))

    return FSMachine(initial_state="Q0", states=states)

# === FSM Simulation ===
def animate_fsm(fsm: FSMachine):
    event_log = []
    current = fsm.get_state(fsm.initial_state)
    while current:
        event_log.append((f"{current.name}: Performing {current.action} (Success Rate: {current.success_prob:.2f})", None))
        if random.random() <= current.success_prob:
            event_log.append((f"✔️ Success → {current.success_transition}", 'lime'))
            if current.success_transition == "GOAL_STATE":
                event_log.append(("🏁 Mission Completed Successfully!", 'lime'))
                break
            current = fsm.get_state(current.success_transition)
        else:
            event_log.append((f"❌ Failure → {current.failure_transition}", 'orange'))
            event_log.append(("🛑 Mission Terminated.", 'orange'))
            break
    return event_log

# === Custom GUI ===
class FSMPlannerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSM Planner Pro")
        self.setGeometry(150, 150, 900, 680)
        self.machine = None
        self.setup_ui()

    def setup_ui(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#1e1e2f"))
        palette.setColor(QPalette.Base, QColor("#2c2c3a"))
        palette.setColor(QPalette.Text, QColor("#eeeeee"))
        palette.setColor(QPalette.Button, QColor("#3c3c4c"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        title = QLabel("⚙️ FSM Football Strategy Designer")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #9cdcfe")
        layout.addWidget(title)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Write an action here")
        self.input_line.setFont(QFont("Segoe UI", 12))
        self.input_line.setStyleSheet("padding: 8px; background-color: #2c2c3a; color: #ffffff; border: 1px solid #444")
        layout.addWidget(self.input_line)

        self.example_toggle = QToolButton()
        self.example_toggle.setText("📘 Action Examples")
        self.example_toggle.setCheckable(True)
        self.example_toggle.setChecked(False)
        self.example_toggle.setStyleSheet("QToolButton { background-color: #3c3c4c; color: #ffffff; padding: 6px 10px; font-size: 13px; border-radius: 4px; } QToolButton:checked { background-color: #505068; }")
        self.example_toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.example_toggle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.example_toggle)

        self.example_box = QTextEdit()
        self.example_box.setReadOnly(True)
        self.example_box.setFont(QFont("Segoe UI", 10))
        self.example_box.setStyleSheet("background-color: #2c2c3a; color: #cccccc; border: 1px solid #444; padding: 6px")
        self.example_box.setText(
            "🧠 Try These Creative Moves:\n"
            "- 'Pass the ball to R2' → Tasks: GO_TO_BALL → ALIGNMENT → PASS\n"
            "- 'Intercept and block' → Tasks: GO_TO_BALL → BLOCK\n"
            "- 'Go for a goal' → Tasks: GO_TO_BALL → ALIGNMENT → SHOOT\n"
            "- 'Pass then shoot' → Sequence: GO_TO_BALL → ALIGNMENT → PASS → GO_TO_BALL → ALIGNMENT → SHOOT\n"
            "- 'Block and counter-pass' → Sequence: GO_TO_BALL → BLOCK → GO_TO_BALL → ALIGNMENT → PASS"
        )
        self.example_box.setVisible(False)
        layout.addWidget(self.example_box)

        self.example_toggle.toggled.connect(lambda checked: self.example_box.setVisible(checked))

        button_bar = QHBoxLayout()
        for label, handler in [("➕ Generate", self.generate_logic), ("▶️ Simulate", self.run_simulation), ("💾 Export", self.export_logic), ("🧹 Clear", self.reset_fields)]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btn.setStyleSheet("QPushButton { background-color: #3c3c4c; color: #ffffff; padding: 8px 20px; font-size: 14px; border-radius: 6px; } QPushButton:hover { background-color: #505068; }")
            button_bar.addWidget(btn)
        layout.addLayout(button_bar)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 11))
        self.output_console.setStyleSheet("background-color: #1e1e2f; color: #dcdcdc; border: 1px solid #555")
        layout.addWidget(self.output_console)

        self.setLayout(layout)

    def generate_logic(self):
        raw = self.input_line.text()
        tasks = decode_instruction(raw)
        if not tasks:
            self.output_console.setText("❗ Instruction not recognized. Use: pass, shoot, block.")
            return
        self.machine = construct_fsm(tasks)
        output = "FSM Structure\n-----------------\n"
        for state in self.machine.states:
            output += f"[{state.name}] {state.action} → {state.success_transition} / fail → {state.failure_transition} (p={state.success_prob})\n"
        self.output_console.setText(output)

    def run_simulation(self):
        if not self.machine:
            QMessageBox.warning(self, "No FSM", "Please generate an FSM before simulation.")
            return
        self.output_console.clear()
        for line, color in animate_fsm(self.machine):
            self.insert_log(line, color)

    def insert_log(self, message, color):
        cursor = self.output_console.textCursor()
        style = QTextCharFormat()
        if color:
            style.setForeground(QColor(color))
        cursor.setCharFormat(style)
        cursor.insertText(message + '\n')

    def export_logic(self):
        if not self.machine:
            QMessageBox.warning(self, "No FSM", "Generate the FSM first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export FSM JSON", "fsm_model.json", "JSON Files (*.json)")
        if path:
            with open(path, 'w') as f:
                json.dump([s.to_dict() for s in self.machine.states], f, indent=4)
            QMessageBox.information(self, "Exported", f"FSM saved to: {path}")

    def reset_fields(self):
        self.machine = None
        self.input_line.clear()
        self.output_console.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = FSMPlannerUI()
    gui.show()
    sys.exit(app.exec_())
