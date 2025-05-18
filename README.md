# FSM Planner Pro

A modern Python application that converts natural-language football instructions into Finite State Machines (FSMs), simulates them step-by-step with probabilistic outcomes, and provides a sleek GUI for interaction.

---

## 🚀 Features

- Convert phrases like `"pass and shoot"` into FSM task sequences
- Custom dark mode GUI with intuitive layout and interactions
- Action example dropdown for user guidance
- Simulation log with color-coded success/failure outcomes
- Export FSM structures to JSON format
- Fully self-contained and extendable Python application

---

## 🖥️ Technologies Used

- **Python 3.11**
- **PyQt5** — GUI framework
- **Dataclasses** — For FSM model representation
- **JSON** — For data export

---

## 📦 Installation

1. **Clone this repository** 
3. Install PyQt5:
   ```bash
   pip install PyQt5
   ```
4. Run the app:
   ```bash
   python APP4 Fsm planner.py
   ```

---

## 🧠 Try These Creative Moves

These are some natural language inputs you can give the app:

- `'Pass the ball to R2'` → Tasks: GO_TO_BALL → ALIGNMENT → PASS
- `'Intercept and block'` → Tasks: GO_TO_BALL → BLOCK
- `'Go for a goal'` → Tasks: GO_TO_BALL → ALIGNMENT → SHOOT
- `'Pass then shoot'` → Sequence: GO_TO_BALL → ALIGNMENT → PASS → GO_TO_BALL → ALIGNMENT → SHOOT
- `'Block and counter-pass'` → Sequence: GO_TO_BALL → BLOCK → GO_TO_BALL → ALIGNMENT → PASS

---

## 🎮 How to Use

1. Launch the application.
2. Enter a football instruction in plain English.
3. Click **Generate** to see the FSM.
4. Click **Simulate** to visualize step-by-step execution.
5. Use the **Action Examples** toggle to see valid inputs.
6. Export your FSM via the **Export** button.

---

## 🧩 Future Ideas

- Live FSM graph view
- Light/dark theme toggle
- Real-time team strategy planner
- .exe packaging for Windows

---

## ✍️ Author

This project was built as part of the APP4 problem-based learning challenge for robotic football planning using FSMs.

---

## 👥 Contributors  
**The Team** : Theodoros CARRE, Dacshayan JEYANESHAN, Luka VUKOVIC, Thibaud TANTER, Luis RAMIREZ RAMIREZ

---

## 📜 License  
This project is licensed under the **ESME License** – Free to use and modify.
