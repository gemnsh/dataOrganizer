import cv2
import numpy as np
import pyautogui

rect_start = None
rect_end = None
drawing = False
captured_frame = None

green=(0,255,0)
red=(0,0,255)
white=(255,255,255)

def draw_rectangle(event, x, y, flags, param):
    global rect_start, rect_end, drawing, captured_frame

    if event == cv2.EVENT_LBUTTONDOWN:
        rect_start = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            rect_end = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        rect_end = (x, y)
        drawing = False

def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

captured_frame = capture_screen()

cv2.namedWindow("Screen Capture")
cv2.setMouseCallback("Screen Capture", draw_rectangle)
cv2.setWindowProperty("Screen Capture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def gts(t):
    (w,h),_=cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    return w,h

while True:
    if captured_frame is not None:
        temp_frame = captured_frame.copy()

        if rect_start and rect_end:
            cv2.rectangle(temp_frame, rect_start, rect_end,green, 2)

        if rect_start and rect_end:
            width = abs(rect_end[0] - rect_start[0])
            height = abs(rect_end[1] - rect_start[1])
            if height != 0:
                aspect_ratio = width / height
                ratio_text =[f"W:{width}px",f"H:{height}px",f"R:{aspect_ratio:.2f}"]

                offset = 5
                text_x = rect_end[0] + offset
                text_y=[rect_start[1]+40*i for i in range(1,4)]
                w=[0]*3
                h=[0]*3
                for i in range(3):
                    w[i],h[i]=gts(ratio_text[i])
                    cv2.rectangle(temp_frame, (text_x, text_y[i] - h[i] - offset), (text_x+offset + w[i], text_y[i] + offset), white, -1)
                    cv2.putText(temp_frame, ratio_text[i], (text_x, text_y[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
        cv2.imshow("Screen Capture", temp_frame)

    key = cv2.waitKey(1)
    if key != -1 or cv2.getWindowProperty("Screen Capture", cv2.WND_PROP_VISIBLE) < 1:  # 키가 입력된 경우, -1이 아닐 때 종료
        break

cv2.destroyAllWindows()
