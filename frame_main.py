"""
This file is a main frame of the system.
It holds a layout of a graphical user interface (GUI) for the main frame.
"""

# Imports
import os
from pathlib import Path
from colors import colors
from tkinter import Tk, Canvas, Button, PhotoImage
from frame_face_detector_data import face_detector_data_frame
from frame_qr_code_scanner_data import frame_qr_code_scanner

# Initialize output path
# This path ensures that the assets of this frame will be found 
# if the system will be executed on the other device.
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.path.join(OUTPUT_PATH, './assets/frame0')

def relative_to_assets(path):
    return os.path.join(ASSETS_PATH, path)

# A main frame class
class main_frame():
	def __init__(self):

		# Configure the GUI root of the system
		# This frame contains a main loop of the system.
		# It is the base frame of the frame stack.
		 
		self.root = Tk()
		self.root.configure(bg = colors.get('white'))
		self.root.resizable(False, False)
		self.root.title("Face Detection and QR Code Scanner System")
		self.root.iconbitmap(relative_to_assets('../favicon.ico'))


		# Ensure that the application will start on the center of the screen
		x_cordinate = int((self.root.winfo_screenwidth()/2) - (662/2))
		y_cordinate = int((self.root.winfo_screenheight()/2) - (408/2))
		self.root.geometry("{}x{}+{}+{}".format(662, 408, x_cordinate, y_cordinate))


	def show_frame(self):

		# Instantiate a canvas and configure layout
		self.canvas = Canvas(
			self.root,
			bg = colors.get('white'),
			height = 408,
			width = 662,
			bd = 0,
			highlightthickness = 0,
			relief = "ridge"
		)

		self.canvas.place(x = 0, y = 0)
		self.canvas.create_rectangle(
			0.0,
			0.0,
			662.0,
			61.0,
			fill=colors.get('main'),
			outline=""
		)

		self.canvas.create_text(
    	70.0,
    	7.5,
			anchor="nw",
			text="DECODE",
			fill=colors.get('white'),
			font=("Arial Black", 16)
		)

		self.canvas.create_text(
			70.0,
    	36.0,
    	anchor="nw",
    	text="Face Detection and QR Code Scanner System",
    	fill=colors.get('white'),
    	font=("Arial", 9)
    )

		logo = PhotoImage(
			file=relative_to_assets("../logo.png")
    )

		self.canvas.create_image(40.0, 35.0, image = logo)

		face_detector_btn_image = PhotoImage(
			file=relative_to_assets("button_1.png")
		)

		face_detector_btn = Button(
			self.root,
			image=face_detector_btn_image,
			borderwidth=0,
			highlightthickness=0,
			command=self.handle_face_detector_btn_click,
			relief="flat"
		)

		face_detector_btn.place(
			x=25.0,
			y=104.0,
			width=275.0,
			height=252.0
		)

		button_image_2 = PhotoImage(
			file=relative_to_assets("button_2.png")
		)

		button_2 = Button(
			self.root,
			image=button_image_2,
			borderwidth=0,
			highlightthickness=0,
			command=self.handle_qrcode_detector_btn_click,
			relief="flat"
		)

		button_2.place(
			x=362.0,
			y=104.0,
			width=275.0,
			height=252.0
		)

		self.root.mainloop()

	def handle_qrcode_detector_btn_click(self):
		# This functions opens the QR Code Scanner frame
		
		frame = frame_qr_code_scanner(self.root)
		frame.show_qr_code_scanner_frame()

	def handle_face_detector_btn_click(self):
		# This functions opens the QR Code Scanner frame

		frame = face_detector_data_frame(self.root)
		frame.show_face_detector_data_frame()
		



