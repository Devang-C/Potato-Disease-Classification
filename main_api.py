from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image # used to read images 
import tensorflow as tf

app = FastAPI()

MODEL = tf.keras.models.load_model('models/1')
CLASS_NAMES = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

#function to read the file as image and return an array
def read_file_as_image(data)->np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

#writing the actual predict function
@app.post('/predict')
async def predict(file: UploadFile=File(...)):
    # convert the image file to bytes
    bytes = await file.read()

    image = read_file_as_image(bytes)

    img_batch = np.expand_dims(image,0)
    
    predictions = MODEL.predict(img_batch)
    index = np.argmax(predictions[0])

    predicted_class = CLASS_NAMES[index]
    confidence = np.max(predictions[0])

    return {
        'class': predicted_class,
        'confidence':float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run("main_api:app", host='localhost', port=8040,reload=True)