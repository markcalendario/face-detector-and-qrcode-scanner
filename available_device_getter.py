import cv2

def get_available_device_index():
  device_index = -1

  while True:
    camera = cv2.VideoCapture(device_index)
    is_temp_cam_capturing, _ = camera.read()
    camera.release()
    
    if is_temp_cam_capturing:
      break
    else:
      print("Device", device_index, "not working.")

    device_index = device_index + 1

  return device_index