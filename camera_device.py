import cv2

def get_available_camera():

  for camera_index in range(-50, 101):
    camera = cv2.VideoCapture(camera_index)
    is_cam_capturing, _ = camera.read()
    camera.release()

    if is_cam_capturing:
      return camera_index
  
  return None