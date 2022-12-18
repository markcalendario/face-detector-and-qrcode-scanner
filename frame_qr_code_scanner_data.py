from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Toplevel, messagebox
import cv2, os
from camera_device import get_available_camera
from colors import colors

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.path.join(OUTPUT_PATH, './assets/frame2')

def relative_to_assets(path):
    return os.path.join(ASSETS_PATH, path)

class frame_qr_code_scanner:
	def __init__(self, root):
		self.root = root
		self.top = Toplevel(self.root)
		self.top.resizable(False, False)
		self.top.geometry("662x408")
		self.top.configure(bg = colors.get('white'))
		self.top.protocol("WM_DELETE_WINDOW",  self.handle_close)
	
	def show_qr_code_scanner_frame(self):
		self.root.withdraw()

		self.canvas = Canvas(
			self.top,
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
			outline="")

		self.canvas.create_text(
    	70.0,
    	7.5,
			anchor="nw",
			text="QR SCANNER",
			fill=colors.get('white'),
			font=("Arial Black", 16)
		)

		self.canvas.create_text(
			70.0,
    	36.0,
    	anchor="nw",
    	text="Face Detection and QR Code Recognition System",
    	fill=colors.get('white'),
    	font=("Arial", 9)
    )

		logo = PhotoImage(
			file=relative_to_assets("../logo.png")
    )

		self.canvas.create_image(40.0, 35.0, image = logo)

		self.canvas.create_rectangle(
    	36.0,
    	189.0,
    	625.0,
    	380.0,
    	fill=colors.get('gray'),
    	outline=""
    )

		self.canvas.create_text(
			36.0,
			76.0,
			anchor="nw",
			text="Show QR Code on the camera.",
			fill=colors.get('black'),
			font=("Arial", 9)
		)

		start_qrcode_scanning_btn_image = PhotoImage(
			file=relative_to_assets("start_qr_code_scan_btn.png")
    )

		start_qrcode_scanning_btn = Button(
			self.top,
    	image=start_qrcode_scanning_btn_image,
    	borderwidth=0,
    	highlightthickness=0,
    	command=self.start_qr_scan,
    	relief="flat"
		)

		start_qrcode_scanning_btn.place(
    	x=36.0,
    	y=121.0,
    	width=589.0,
    	height=58.0
    )

		image_qrcode = PhotoImage(
    	file=relative_to_assets("qr_code.png")
    )

		self.canvas.create_image(
    	331.0,
    	254.0,
    	image=image_qrcode
    )

		self.result_text = self.canvas.create_text(
    	331.0,
    	310.0,
    	anchor="center",
    	text="Result will appear here.",
    	fill=colors.get('black'),
    	font=("Arial Black", 13)
  	)

		self.canvas.create_text(
			36.0,
			96.0,
			anchor="nw",
			text="Press Esc to quit.",
			fill=colors.get('black'),
			font=("Arial Black", 9)
		)

		self.top.mainloop()

	def draw_text(self, img, text, font=cv2.FONT_HERSHEY_PLAIN, pos=(0, 0), font_scale=3, font_thickness=2, text_color=(0, 255, 0), text_color_bg=(0, 0, 0)):
			x, y = pos
			text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
			text_w, text_h = text_size
			cv2.rectangle(img, pos, (x + text_w + 10, y + text_h + 10), text_color_bg, -1)
			cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

			return text_size

	def read_qrcodes(self, detector, frame):

		qr_data_text, bbox, _ = detector.detectAndDecode(frame)
		self.canvas.itemconfig(self.result_text, text=qr_data_text if qr_data_text else "No QR Code Detected" )
		self.canvas.update()

		if not qr_data_text:
			return frame

		point_1 = [int(point_1_floats) for point_1_floats in bbox[0][0]]
		point_2 = [int(point_2_floats) for point_2_floats in bbox[0][2]]
		
		frame = cv2.rectangle(frame, point_1, point_2, colors.get('qr_code_scan'), 2)

		# Initialize Font
		font = cv2.FONT_HERSHEY_COMPLEX 

		self.draw_text(frame, qr_data_text, font, (point_1[0], point_1[1] - 38), 1, 2, (255, 255, 255), colors.get('qr_code_scan'))

		return frame

	def start_qr_scan(self):

		available_camera_index = get_available_camera()
		detector = cv2.QRCodeDetector()

		if available_camera_index == None:
			messagebox.showerror("Camera is not detected", "You do not have available camera. Please make sure your camera is turned on and connected.")
			self.top.destroy()
			self.root.deiconify()
			return

		camera = cv2.VideoCapture(available_camera_index)
		is_device_capturing, frame = camera.read()

		while is_device_capturing:
			is_device_capturing, frame = camera.read()

			if cv2.waitKey(1) == 27:
				break

			frame = self.read_qrcodes(detector, frame)
			
			cv2.imshow('Real Time - QR Code Scanner', frame)
			
		camera.release()
		cv2.destroyAllWindows()
		

	def handle_close(self):
		self.root.deiconify()
		self.top.destroy()
