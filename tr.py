import cv2

# مسار الفيديو
VIDEO_PATH = r'C:\Users\ZS\Downloads\my_vid.mp4'

# إعداد النافذة
WINDOW_NAME = "Object Tracker"
cv2.namedWindow(WINDOW_NAME)

# فتح الفيديو
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"Error: Unable to open video file: {VIDEO_PATH}")
    exit()

# متغيرات التتبع
tracker = cv2.TrackerCSRT_create()  # اختيار نوع التراكر
initBB = None  # Bounding Box للجسم
tracking = False  # حالة التتبع


def click_and_track(event, x, y, flags, param):
    """
    دالة استدعاء عند النقر على الجسم بالفأرة
    """
    global initBB, tracker, tracking

    if event == cv2.EVENT_LBUTTONDOWN:  # عند النقر بزر الفأرة الأيسر
        print(f"Clicked at: x={x}, y={y}")
        tracker = cv2.TrackerCSRT_create()  # إعادة إنشاء التراكر
        # حجم مستطيل أولي حول النقطة
        box_size = 50  # حجم المستطيل
        x1 = max(0, x - box_size)
        y1 = max(0, y - box_size)
        x2 = min(frame.shape[1], x + box_size)
        y2 = min(frame.shape[0], y + box_size)
        initBB = (x1, y1, x2 - x1, y2 - y1)  # تحديد Bounding Box
        tracker.init(frame, initBB)  # بدء التتبع
        tracking = True


# ربط الماوس بنافذة العرض
cv2.setMouseCallback(WINDOW_NAME, click_and_track)

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    # إذا كان هناك تتبع جارٍ، نقوم بتحديث موقع الجسم
    if tracking:
        success, box = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            print("Tracking failed!")
            tracking = False

    # عرض الإطار
    cv2.imshow(WINDOW_NAME, frame)

    # إنهاء العرض عند الضغط على "q"
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# تحرير الموارد
cap.release()
cv2.destroyAllWindows()
