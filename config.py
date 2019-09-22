from bunch import Bunch
C = Bunch()


'''
Main server settings
'''
# robotics_module
C.initial_pos = [0, 90, 0, 0]
C.body_lengths = [0, 12, 15, 18.54]

# arduino_module
C.arduino_port = 'COM3'

'''
OCR server settings
'''
C.ocr_server_port = 8080
