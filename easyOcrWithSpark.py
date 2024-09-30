from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, monotonically_increasing_id
from pyspark.sql.types import StringType
import easyocr
import numpy as np
import cv2
import requests
import csv
from PIL import Image
from io import BytesIO

# Initialize EasyOCR Reader (once per worker)
def create_reader():
    return easyocr.Reader(['en'])

# OCR processing function for each image URL
def process_image(image_url, row_index):  # Add row_index as input
    try:
        print(f"Processing image {row_index + 1}: {image_url}")  # Print progress
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        gray_img = img.convert('L')
        gray_img_np = np.array(gray_img)

        reader = create_reader()  # Initialize reader within the function
        results = reader.readtext(gray_img_np)

        detected_text = " ".join([text for (_, text, _) in results])
        return detected_text
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        return 'Error'

# Create SparkSession
spark = SparkSession.builder.appName("OCR_PySpark").getOrCreate()

# Read CSV data into a Spark DataFrame
df = spark.read.csv('/content/test.csv', header=True)

# Add a row index column
df = df.withColumn("row_index", monotonically_increasing_id())

# Register the OCR processing function as a UDF (include row_index)
ocr_udf = udf(process_image, StringType())

# Apply the UDF to the DataFrame (pass row_index)
df = df.withColumn("easyocr", ocr_udf(df["image_link"], df["row_index"]))

# Save the results to a new CSV file
df.write.csv('easy_ocr.csv', header=True, mode="overwrite")

# Stop the SparkSession
spark.stop()
