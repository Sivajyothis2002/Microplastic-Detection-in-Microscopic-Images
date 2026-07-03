import streamlit as st

st.set_page_config(
    page_title="Microplastic Detector",
    layout="wide"
)

import cv2
import os
import numpy as np
from PIL import Image
from ultralytics import YOLO
import matplotlib.pyplot as plt


# import streamlit as st
# import cv2
# import os
# import numpy as np
# from PIL import Image
# from ultralytics import YOLO
# import matplotlib.pyplot as plt

# Class names and colors
CLASS_NAMES = ['fiber', 'film', 'fragment', 'pellet']
CLASS_COLORS = {
    'fiber': (0, 255, 0),
    'film': (255, 0, 0),
    'fragment': (0, 0, 255),
    'pellet': (255, 255, 0)
}

# Load model
@st.cache_resource
def load_model():
    model_path = 'best.pt'  # Place the trained model in the same folder
    return YOLO(model_path)

model = load_model()

# Helper to draw boxes
def draw_boxes(image, results):
    img = np.array(image.convert("RGB"))
    h, w = img.shape[:2]

    for box in results.boxes:
        cls_id = int(box.cls.item())
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        color = CLASS_COLORS[CLASS_NAMES[cls_id]]
        label = f"{CLASS_NAMES[cls_id]}"
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return img

# Streamlit UI
st.title("🧪 Microplastic Detection & Classification")

st.sidebar.header("Upload Test Image")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Run inference
    results = model(image)[0]
    
    # Draw predictions
    result_img = draw_boxes(image, results)

    # Show predictions
    st.subheader("🔍 Detection Results")
    st.image(result_img, caption="Predicted Bounding Boxes", use_container_width=True)

    # Class Count
    class_counts = {cls: 0 for cls in CLASS_NAMES}
    for box in results.boxes:
        cls_id = int(box.cls.item())
        class_counts[CLASS_NAMES[cls_id]] += 1

    st.subheader("📊 Detected Microplastics Count")
    st.json(class_counts)

else:
    st.info("Upload an image from the sidebar to begin.")
