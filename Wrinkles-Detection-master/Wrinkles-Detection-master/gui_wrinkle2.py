import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def detect_wrinkles():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename()
    
    if file_path:
        # Load the selected image
        img = cv2.imread(file_path)
        
        if img is not None:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=10)
            
            # Initialize the number_of_edges variable
            number_of_edges = 0
            
            for x, y, w, h in faces:
                # Draw a rectangle around the detected face for visualization
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cropped_img = img[y:y+h, x:x+w]
                edges = cv2.Canny(cropped_img, 130, 1000)  # Adjust Canny thresholds
                number_of_edges = np.count_nonzero(edges)  # Update the variable
            
            if number_of_edges > 1000:  # Adjust the threshold as needed
                result_label.config(text=" Wrinkle Found")
            else:
                result_label.config(text="No Wrinkle Found")
            
            # Display the modified image with rectangles around detected faces
            display_image(img)
        else:
            print("Error: Could not load the image.")
            result_label.config(text="Error: Could not load the image")

def display_image(image):
    # Convert the image to RGB format for display
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    pil_image.thumbnail((400, 400))
    tk_image = ImageTk.PhotoImage(pil_image)
    image_label.config(image=tk_image)
    image_label.image = tk_image

# Create the main window
root = tk.Tk()
root.title("Wrinkle Detector")

# Create a button to detect wrinkles
detect_button = tk.Button(root, text="Detect Wrinkles", command=detect_wrinkles)
detect_button.pack()

# Create a label for displaying the result
result_label = tk.Label(root, text="")
result_label.pack()

# Create a label for displaying the image
image_label = tk.Label(root)
image_label.pack()

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Start the Tkinter main loop
root.mainloop()
