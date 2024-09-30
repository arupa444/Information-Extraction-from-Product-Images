# Information Extraction from Product Images

## Overview
Our prediction process involved two key steps:

1. **Image-to-Text Conversion**: Extracting textual data from the provided test images using Optical Character Recognition (OCR) technology.
2. **Information Extraction with NER**: Cleaning and processing the extracted text using Named Entity Recognition (NER) techniques to identify and extract specific information, ensuring a more accurate and targeted prediction.

## Flowchart of Processes
![Flowchart](path/to/image.png)

## Explanation

### Part 1: Image Text Extraction (Using Pytesseract)
1. **Import Libraries**: The code begins by importing necessary libraries such as `requests` (for HTTP requests), `PIL` (for handling images), `pytesseract` (for OCR), and `pandas` (for data manipulation).
2. **Load DataFrame**: The program loads a CSV file (`test.csv`) into a pandas DataFrame, which contains image URLs and relevant information.
3. **`extract_text_from_image` Function**: 
   - **Download Image**: Sends a GET request to the given URL to download the image.
   - **Open Image**: Opens the downloaded image using `PIL.Image.open`.
   - **OCR**: Uses `pytesseract.image_to_string` to extract text from the image.
   - **Error Handling**: Includes a `try-except` block to catch errors and return error messages.
4. **Apply OCR**: The function is applied to the 'image_link' column of the DataFrame, storing the extracted text in a new column called 'tesseract'.
5. **Save DataFrame**: The updated DataFrame with the extracted text is saved as a new CSV file (`csv/101000.csv`).

### Part 2: Entity Extraction and Unit Standardization
1. **Load and Prepare Data**: Loads a new CSV file (likely the one generated in Part 1) and defines lists of different unit types (e.g., length, weight, volume, power).
2. **`standardize_unit` Function**: Standardizes units to ensure consistency (e.g., "cm" to "centimeter").
3. **`process_text` Function**: 
   - **Lowercase Text**: Converts text to lowercase.
   - **Entity-Specific Logic**: Extracts values based on the 'entity_name' column (e.g., 'depth', 'width', 'item_weight').
   - **Regular Expressions**: Finds numerical values followed by specific units.
   - **Unit Standardization**: Calls the `standardize_unit` function for consistent unit representation.
   - **Print Values**: Prints the extracted values for debugging purposes.
4. **Apply Processing**: Applies `process_text` to each row of the DataFrame, storing results in the 'extracted_value' column.
5. **Entity-Unit Mapping**: Creates a dictionary `entity_unit_map` to store unique units found for each entity type.
6. **Save Results**: Saves the processed DataFrame to a new CSV file (`extracted_results_from_combined.csv`).

## Summary
We developed a two-step solution for extracting and standardizing information from product images:

1. **Optical Character Recognition (OCR)**: Using the Pytesseract library, we converted image data into machine-readable text.
   - Downloaded images via URLs.
   - Processed the images to extract textual content.
2. **Named Entity Recognition (NER)**: A rule-based NER system cleaned and analyzed the extracted text.
   - Text Preprocessing: Cleaned and prepared the text.
   - Entity-Specific Rules: Applied logic and regular expressions to extract numerical values and associated units.
   - Unit Standardization: Standardized units (e.g., "cm" to "centimeter") for consistency.

This automated process significantly enhanced the efficiency and accuracy of extracting and standardizing product information from images.
