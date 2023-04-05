# import cv2
# from pyzbar import pyzbar
#
#
# def decode_qr_code(image):
#     decoded_objects = pyzbar.decode(image)
#     for obj in decoded_objects:
#         print("Tipo:", obj.type)
#         print("Datos:", obj.data.decode("utf-8"))
#         print("Datos-tipo:", type(obj.data.decode("utf-8")))
#         print("\n")
#
#
# def main():
#     # Open the device in the first input argument, using the direct show backend.qq
#     s_video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#
#     # continually read and display frames
#     while True:
#         # Grab a frame from the device. This will wait until a frame is ready at this part of the code.
#         ret, img = s_video.read()
#
#         # Throw the frame onto a window - note that the name here matters and associated with an already open window
#         cv2.imshow("Stream Video", img)
#         decode_qr_code(img)
#
#         # Wait for 1 ms on this frame. The output here is any keys hit - hit q to exit. You can of course do other
#         # things here like save the output.
#         key = cv2.waitKey(1) & 0xff
#         if cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE) < 1:
#             keyCode = cv2.waitKey(key)
#             if (keyCode & 0xFF) == ord("q"):
#                 s_video.release()  # Release the webcam. If you forget to do this or the code crashes, in the worst case
#                 cv2.destroyAllWindows()
#                 break
#
#
# if __name__ == '__main__':
#     main()


a = {0: "logi 1", 3: "logi 3", 5: "logi 5"}

b = "logi 5"

for key, value in a.items():
    if b == value:
        print(key)

