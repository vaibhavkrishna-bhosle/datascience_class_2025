import cv2
import numpy as np

# Haar cascade (comes with OpenCV)
face_cascade = cv2.CascadeClassifier("D:\\satyam apps\\datascience_class_2025\\Database\\haarcascade_frontalface_default.xml")
if face_cascade.empty():
    raise RuntimeError("Could not load haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(2)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

print("Press 'q' to quit")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    output = frame.copy()

    for (x, y, w, h) in faces:
        # Face ROI bounds (safe clipping)
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(frame.shape[1], x + w), min(frame.shape[0], y + h)
        roi = output[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        # Strong blur on ROI
        blur_k = max(31, (min(w, h) // 2) | 1)  # odd kernel
        blurred_roi = cv2.GaussianBlur(roi, (blur_k, blur_k), 0)

        # Build radial circular alpha mask (1 in center -> 0 at edge)
        rh, rw = roi.shape[:2]
        cx, cy = rw / 2.0, rh / 2.0
        radius = min(rw, rh) * 0.48

        yy, xx = np.ogrid[:rh, :rw]
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

        # Feathered edge: full blur at center, smooth falloff near radius
        feather = radius * 0.25
        alpha = np.clip((radius - dist) / feather, 0, 1).astype(np.float32)
        alpha = alpha[..., None]  # shape (h, w, 1)

        # Blend blurred ROI with original ROI using radial mask
        blended = (alpha * blurred_roi + (1 - alpha) * roi).astype(np.uint8)
        output[y1:y2, x1:x2] = blended

    cv2.imshow("Radial Face Blur (Haar Cascade)", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()