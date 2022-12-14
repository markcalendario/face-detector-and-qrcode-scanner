from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from frame_face_detector_data import face_detector_data_frame
from colors import colors
from frame_qr_code_scanner_data import frame_qr_code_scanner

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class main_frame():
	def __init__(self):
		self.root = Tk()
		self.root.configure(bg = "#FFFFFF")
		self.root.resizable(False, False)
		self.root.title("Face Detection and QR Code Scanner System")

		x_cordinate = int((self.root.winfo_screenwidth()/2) - (662/2))
		y_cordinate = int((self.root.winfo_screenheight()/2) - (408/2))
		self.root.geometry("{}x{}+{}+{}".format(662, 408, x_cordinate, y_cordinate))


	def show_frame(self):
		canvas = Canvas(
			self.root,
			bg = colors.get('white'),
			height = 408,
			width = 662,
			bd = 0,
			highlightthickness = 0,
			relief = "ridge"
		)

		canvas.place(x = 0, y = 0)
		canvas.create_rectangle(
			0.0,
			0.0,
			662.0,
			61.0,
			fill=colors.get('main'),
			outline=""
		)

		canvas.create_text(
    	25.0,
    	7.5,
			anchor="nw",
			text="GROUP 4",
			fill=colors.get('white'),
			font=("Arial Black", 16)
		)

		canvas.create_text(
			25.0,
    	36.0,
    	anchor="nw",
    	text="Face Detection and QR Code Recognition System",
    	fill=colors.get('white'),
    	font=("Arial", 9)
    )

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
		file=relative_to_assets("button_2.png"))

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
		frame = frame_qr_code_scanner(self.root)
		frame.show_qr_code_scanner_frame()

	def handle_face_detector_btn_click(self):
		frame = face_detector_data_frame(self.root)
		frame.show_face_detector_data_frame()
		



