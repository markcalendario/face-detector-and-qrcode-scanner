from pathlib import Path
import os
import cv2
from tkinter import Canvas, Button, PhotoImage, Toplevel, messagebox
from camera_device import get_available_camera
from colors import colors

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.path.join(OUTPUT_PATH, './assets/frame1')

def relative_to_assets(path):
    return os.path.join(ASSETS_PATH, path)

class face_detector_data_frame():
	def __init__(self, root):
		self.root = root
		self.top = Toplevel(self.root)
		self.top.geometry("662x408")
		self.top.configure(bg = "#FFFFFF")
		self.top.protocol("WM_DELETE_WINDOW",  self.handle_close)

	def show_face_detector_data_frame(self):
		self.root.withdraw()

		self.canvas = Canvas(
			self.top,
			bg = "#FFFFFF",
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
			text="FACE DETECTOR",
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

		self.indicator_rectangle_container = self.canvas.create_rectangle(
    	36.0,
    	189.0,
    	625.0,
    	380.0,
    	fill=colors.get('gray'),
    	outline=""
    )

		self.image_warn = PhotoImage(
    	file=relative_to_assets("warning_mark.png")
    )
    
		self.image_check = PhotoImage(
    	file=relative_to_assets("check_mark.png")
    )

		self.face_detection_indicator_image = self.canvas.create_image(
    	331.0,
    	254.0,
    	image=self.image_warn
    )

		self.indicator_text = self.canvas.create_text(
    	331.0,
    	310.0,
    	anchor="center",
    	text="Detection has not yet started.",
    	fill=colors.get('black'),
    	font=("Arial Black", 13)
  	)

		self.canvas.create_text(
			36.0,
			76.0,
			anchor="nw",
			text="Please be still while detecting your face.",
			fill=colors.get('black'),
			font=("Arial", 9)
		)

		self.canvas.create_text(
			36.0,
			96.0,
			anchor="nw",
			text="Press Esc to quit.",
			fill=colors.get('black'),
			font=("Arial Black", 9)
		)

		start_face_detection_btn_image = PhotoImage(
			file=relative_to_assets("start_face_detection.png")
    )

		start_face_detection_btn = Button(
			self.top,
    	image=start_face_detection_btn_image,
    	borderwidth=0,
    	highlightthickness=0,
    	command=self.display_face_detection_feed,
    	relief="flat"
		)

		start_face_detection_btn.place(
    	x=36.0,
    	y=121.0,
    	width=589.0,
    	height=58.0
    )

		self.top.resizable(False, False)
		self.top.mainloop()

	def display_face_detection_feed(self):
    # Load the Haar cascade file for detecting faces
		face_cascade = cv2.CascadeClassifier(os.path.join(OUTPUT_PATH, 'haarcascades', 'haarcascade_frontalface_alt2.xml'))

    # Initialize the video capture object
		available_camera_index = get_available_camera()

		if available_camera_index == None:
			messagebox.showerror("Camera is not detected", "You do not have available camera. Please make sure your camera is turned on and connected.")
			self.top.destroy()
			self.root.deiconify()
			return

		camera = cv2.VideoCapture(available_camera_index)
		is_camera_capturing, frame = camera.read()


		while is_camera_capturing:
			# Grab the frame from the video capture object
			is_camera_capturing, frame = camera.read()

			# Convert the frame to grayscale
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Look for faces in the frame using the loaded cascade file
			faces = face_cascade.detectMultiScale(gray, 1.1, 4)

			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 8), 2)


			cv2.imshow('Video', frame)

			# Terminate if user pressed Escape key
			if cv2.waitKey(1) == 27:
				break
			if len(faces) != 0:
				self.canvas.itemconfig(self.face_detection_indicator_image, image=self.image_check)
			else:
				self.canvas.itemconfig(self.face_detection_indicator_image, image=self.image_warn)

			self.canvas.itemconfig(self.indicator_text, text=f"{len(faces)} Face(s) Detected")
			self.top.update()
		
		camera.release()
		cv2.destroyWindow('Video')


	def handle_close(self):
		self.root.deiconify()
		self.top.destroy()