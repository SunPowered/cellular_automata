import tkinter as tk
from cellular_automata.ui import CellularAutomataUI as UI


if __name__ == "__main__":
	root = tk.Tk()
	ca = UI(root)
	ca.mainloop()