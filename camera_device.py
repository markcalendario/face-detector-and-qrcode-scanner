import cv2

def get_available_camera():

  # Allow loop to test camera indices from -50 to 100
  for camera_index in range(-50, 101):
    camera = cv2.VideoCapture(camera_index)
    is_cam_capturing, _ = camera.read()
    camera.release()

    # If camera is available then return the index
    if is_cam_capturing:
      return camera_index
  
  # If there are no camera available, return None
  return None