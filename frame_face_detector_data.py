"""
This file is the face detector frame of the system.
It holds a top level layout of a graphical user interface (GUI) for the face detector frame.
"""

import cv2, os
from pathlib import Path
from colors import colors
from tkinter import Canvas, Button, PhotoImage, Toplevel, messagebox
from camera_device import get_available_camera

# Initialize output path
# This path ensures that the assets of this frame will be found 
# if the system will be executed on the other device.
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.path.join(OUTPUT_PATH, './assets/frame1')

def relative_to_assets(path):
    return os.path.join(ASSETS_PATH, path)

# A face detector frame class
class face_detector_data_frame():
	def __init__(self, root):
		# Configure this frame as a top level of the root (main loop)
		self.root = root
		self.top = Toplevel(self.root)
		self.top.geometry("662x408")
		self.top.configure(bg = "#FFFFFF")
		self.top.protocol("WM_DELETE_WINDOW",  self.handle_close)

	def show_face_detector_data_frame(self):
		# Close a root window
		self.root.withdraw()

		# Construct a canvas for this frame
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
    	text="Face Detection and QR Code Scanner System",
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
		self.top.iconbitmap(relative_to_assets('../favicon.ico'))
		self.top.resizable(False, False)
		self.top.mainloop()

	def display_face_detection_feed(self):

    # Load the Haar cascade file for detecting faces
		# Haarcascade is a detection model for a particular object.
		# In this function, frontalface_alt2 is being used.
		# This haarcascade consists of 9,563 face model.

		face_cascade = cv2.CascadeClassifier(os.path.join(OUTPUT_PATH, 'haarcascades', 'haarcascade_frontalface_alt2.xml'))

    # Initialize the video capture object
		available_camera_index = get_available_camera()

		# If no available camera device
		if available_camera_index == None:
			messagebox.showerror("Camera is not detected", "You do not have available camera. Please make sure your camera is turned on and connected.")
			self.top.destroy()
			self.root.deiconify()
			return

		# Open a camera
		camera = cv2.VideoCapture(available_camera_index)
		is_camera_capturing, frame = camera.read()

		# While camera is getting frame
		while is_camera_capturing:

			# Continuously grab the frame from the video capture object
			is_camera_capturing, frame = camera.read()

			# Convert the frame to grayscale for better detection
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Look for near to similar faces in the frame using the loaded cascade file
			faces = face_cascade.detectMultiScale(gray, 1.1, 4)

			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
					cv2.rectangle(frame, (x, y), (x+w, y+h), colors.get('face_detector_box'), 2)

			cv2.imshow('Face Detector', frame)

			# Terminate if user pressed 'Esc' key
			if cv2.waitKey(1) == 27:
				break

			# If there are faces detected,
			# Then show a check indicator image
			if len(faces) != 0:
				self.canvas.itemconfig(self.face_detection_indicator_image, image=self.image_check)
			
			# Otherwise display a warning indicator image
			else:
				self.canvas.itemconfig(self.face_detection_indicator_image, image=self.image_warn)

			# Display count of faces detected on the canvas
			self.canvas.itemconfig(self.indicator_text, text=f"{len(faces)} Face(s) Detected")
			# Take effect the canvas content modification
			self.top.update()
		
		# Close the camera
		camera.release()
		cv2.destroyAllWindows()


	def handle_close(self):
		# Handles a close event

		# Display the root frame
		self.root.deiconify()
		# Pop the face detector frame from the frame stack
		self.top.destroy()