#-*- coding:utf-8 -*-
from tkinter import *
from tkinter import filedialog
import os

def check(byte):
		if len(byte) != 0:
			return ord(byte)
		else:
			return 0

class MainWindow:
	def __init__(self):
		window = Tk()
		window.title("HWP Malware Detector")
		window.geometry("500x300")
		window.resizable(False, False)
		# LABEL
		label = Label(window, text="HWP 악성코드 검사기")
		label.pack()
		# TEXT BOX
		self.txt_filename = Text(window)
		self.txt_filename.place(x =10, y=30, height=30, width=360)
		self.txt_log = Text(window)
		self.txt_log.place(x = 10, y = 70, height=200, width=360)
		scroll_y = Scrollbar(window, orient="vertical", command=self.txt_log.yview)
		scroll_y.pack(side="left", expand=True, fill="y")
		scroll_y.place(x = 10, y = 70, height=200, width=360)
		self.txt_log.configure(yscrollcommand=scroll_y.set)
		# BUTTON
		btn_fopen = Button(window, text="열기", command=self.btn_fopen_clicked)
		btn_fopen.place(x=380, y=30, height=30, width=50)
		btn_analysis = Button(window, text="분석", command=self.btn_analysis_clicked)
		btn_analysis.place(x=435, y=30, height=30, width=50)
		# HWP BINARY DATA
		self.hex_lst = []
		# MAINLOOP
		window.mainloop()

	def btn_fopen_clicked(self):
		filename = filedialog.askdirectory(initialdir="/",title='Please select a Directory that contains the HWP file.')
		print(filename)
		self.txt_filename.delete('1.0', END)
		self.txt_filename.insert(END, filename)

	def btn_analysis_clicked(self):
		dir_path = self.txt_filename.get('1.0', END)
		filenames = os.listdir(dir_path[:-1])
		print("폴더내 파일리스트 : ", filenames)
		for filename in filenames:
			name, ext = os.path.splitext(filename)
			if ext != '.hwp':
				continue
			try:
				with open(dir_path[:-1] + "\\" + filename, "rb") as f:
					self.hex_lst = []
					byte = f.read(1)
					while byte:
						self.hex_lst.append(check(byte))
						byte = f.read(1)
					print("Read Binary Data Done")
			except:
				print("%s는 존재하지 않는 파일입니다. 다시 확인해주세요." % filename.encode('utf8'))
				continue
			#print(self.hex_lst)
			self.txt_log.insert(END, "HWP 파일 사이즈는 %s" % len(self.hex_lst) + " bytes입니다. \n")
			self.txt_log.insert(END, "OLE 파일 구조를 가지고 있습니다. \n")
			print(len(self.hex_lst))


def main():
	MainWindow()

if __name__ == '__main__':
	main()