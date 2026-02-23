import numpy as np
from PIL import Image

def process_image(image_data):
    """Resizes image for the AI model."""
    img = Image.open(image_data).convert('RGB')
    img = img.resize((224, 224)) # Standard for MobileNet
    return np.array(img) / 255.0

def mock_predict(image_array):
    """
    Simulates the AI Brain until we load the real model.
    Logic: If the image is 'too dark' or 'too plain', it's rejected.
    """
    avg_color = np.mean(image_array)
    if avg_color < 0.1 or avg_color > 0.9:
        return "Rejected", 0.0
    
    # Simulating a detection for the prototype
    classes = ["Common Rust", "Northern Leaf Blight", "Gray Leaf Spot", "Healthy"]
    prediction = classes[0] # Mocking Common Rust
    confidence = 0.88
    return prediction, confidence