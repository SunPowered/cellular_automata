import tkinter as tk
from tkinter.ttk import Style
import numpy as np
from cellular_automata.ca import Population

CELL_SIZE = 2

class CellularAutomataUI(tk.Frame):

	def __init__(self, root):
		super().__init__(root)
		self.setup_ui()
		self.cells = Population(self.population_size.get(), self.rule_number.get())
		self.reset()

	def setup_ui(self):
		"""Create and pack the UI the widgets"""
		self.master.title("Cellular Automata")
		self.style = Style()
		self.style.theme_use('default')
		self.pack(fill=tk.BOTH, expand=True)

		self.canvas = tk.Canvas(self, bg='white', relief=tk.RAISED, borderwidth=1, width=CELL_SIZE*200, height=CELL_SIZE*200)
		self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, anchor=tk.N, expand=True)

		frm_params = tk.Frame(self, width=30)
		frm_params.pack(fill=tk.Y, side=tk.LEFT)

		lbl_params = tk.Label(frm_params, text="Parameters", justify='right', font=('Helvetica', 12, 'underline'))
		lbl_params.pack(side=tk.TOP, padx=5, pady=5, anchor='n', fill=tk.X, expand=True)
		
		frm_pop_size = tk.Frame(frm_params)
		frm_pop_size.pack(side=tk.TOP, pady=2, fill=tk.X, expand=True)
		self.population_size = tk.IntVar()
		self.population_size.set(200)
		self.spn_pop_size = tk.Spinbox(frm_pop_size, from_=20, to_=2000, increment=10, justify='center', width=5, textvariable=self.population_size)
		self.spn_pop_size.pack(side=tk.LEFT, padx=3, pady=3)
		lbl_pop_size = tk.Label(frm_pop_size, text="Size (N)", justify='left')
		lbl_pop_size.pack(side=tk.LEFT, padx=3, pady=3)

		frm_disp_iter = tk.Frame(frm_params)
		frm_disp_iter.pack(side=tk.TOP, pady=2, fill=tk.X, expand=True)
		self.display_iteration_size = tk.IntVar()
		self.display_iteration_size.set(200)
		self.spn_disp_iter = tk.Spinbox(frm_disp_iter, from_=25, to_=200, increment=5, justify='center', width=5, textvariable=self.display_iteration_size)
		self.spn_disp_iter.pack(side=tk.LEFT, padx=3, pady=3)
		lbl_disp_iter = tk.Label(frm_disp_iter, text="Display Iterations")
		lbl_disp_iter.pack(side=tk.LEFT, padx=3, pady=3)

		frm_rule_num = tk.Frame(frm_params)
		frm_rule_num.pack(side=tk.TOP, pady=2, fill=tk.X, expand=True)
		self.rule_number = tk.IntVar()
		self.rule_number.set(30)
		self.spn_rule_num = tk.Spinbox(frm_rule_num, from_=0, to_=256, justify='center', width=5, textvariable=self.rule_number)
		self.spn_rule_num.pack(side=tk.LEFT, pady=3, padx=3)
		lbl_rule_num = tk.Label(frm_rule_num, text="Rule No.")
		lbl_rule_num.pack(side=tk.LEFT, pady=3)

		frm_do_scroll = tk.Frame(frm_params)
		frm_do_scroll.pack(side=tk.TOP, pady=2, expand=True)

		self.do_scroll = tk.BooleanVar()
		self.cb_do_scroll = tk.Checkbutton(frm_do_scroll, text="Scroll", variable=self.do_scroll)
		self.cb_do_scroll.pack(side=tk.RIGHT, expand=True)

		frm_btns = tk.Frame(frm_params)
		frm_btns.pack(side=tk.BOTTOM, pady=5, expand=True)

		self.iter = tk.IntVar()
		self.iter.set(1)
		lbl_iter = tk.Label(frm_params, textvariable=self.iter)
		lbl_iter.pack(side=tk.TOP, padx=3, pady=3, expand=True)
		btn_run = tk.Button(frm_btns, text="Run", font=('Helvetica', 14, 'bold'), command=self.run_once)
		btn_run.pack(side=tk.LEFT, padx=3, pady=3) 
		btn_step = tk.Button(frm_btns, text='Step', command=self.step)
		btn_step.pack(side=tk.LEFT, padx=3, pady=3)
		btn_reset = tk.Button(frm_btns, text='Reset', command=self.reset)
		btn_reset.pack(side=tk.LEFT, padx=3, pady=3)

	def reset(self):

		if not self.do_scroll.get():
			self.cells = Population(self.population_size.get(), self.rule_number.get())
		self.canvas.delete('all')
		self.iter.set(1)
		self.draw_line(self.iter.get())

	def draw_rect(self, x, y):
		"""
		Draw a single rectangle at the given coordinates
		"""
		# TODO: Auto compute cellsize from parameters and canvas window size
		self.canvas.create_rectangle(
			x*CELL_SIZE, 		# x1
			y*CELL_SIZE, 		# y1
			(x+1)*CELL_SIZE, 	# x2
			(y+1)*CELL_SIZE,	# y2 
			fill='black'
		)

	def draw_line(self, line):
		"""
		Draw a population line on the canvas at a given line
		"""
		for x in np.where(self.cells.cells)[0]:
			self.draw_rect(x, line)

	def step(self):
		self.iter.set(self.iter.get() + 1)  # Increment iterator
		self.cells.transform()
		self.draw_line(self.iter.get())

	def update(self):
		if self.iter.get() < self.display_iteration_size.get():
			self.step()
			self.master.after(12, self.update)

	def run_once(self):
		self.reset()
		self.update()

