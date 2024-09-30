import pandas as pd
import re  # Regular expressions for extracting numbers with units

# Load the CSV file
df = pd.read_csv("/Users/apple/Documents/PROGRAMMING/python/flaskApp/.venv/amazon/dataset/combined_data.csv")

# List of units (add more units as needed)
length_units = ["centimetre", "cm", "em", "inch", "in", "millimetre", "mm", "metre", "m", "foot", "ft", "yard", "yd"]
weight_units = ["kilogram", "kg", "kilograms", "kgs", "gram", "g", "grams", "gs", "milligram", "mg", "eg",
                "microgram", "µg", "ounce", "oz", "pound", "lb", "ton", "tons"]
volume_units = ["litre", "l", "liter", "liters", "millilitre", "ml", "milliliter", "milliliters",
                "gallon", "gal", "gallons", "quart", "qt", "quarts", "pint", "pt", "pints",
                "cup", "cups", "fluid ounce", "fl oz", "cubic inch", "cu in", "cubic foot", "cu ft",
                "centilitre", "cl", "decilitre", "dl", "imperial gallon", "imp gal", "microlitre", "µl"]  # Added more units
power_units = ["watt", "w", "watts", "kilowatt", "kw", "kilowatts", "volt", "v", "volts", "millivolt", "mv", "kilovolt", "kv",
               "ampere", "a", "amperes", "amps"]  # Added millivolt and kilovolt

# Function to convert units to their standard forms (modified to return the desired units)
def standardize_unit(value, unit):
    if unit in ["centimetre", "cm", "em"]:
        return value, "centimetre"
    elif unit in ["inch", "in"]:
        return value, "inch"
    elif unit in ["millimetre", "mm"]:
        return value, "millimetre"
    elif unit in ["metre", "m"]:
        return value, "metre"
    elif unit in ["foot", "ft"]:
        return value, "foot"
    elif unit in ["yard", "yd"]:
        return value, "yard"
    elif unit in ["kilogram", "kg", "kilograms", "kgs", "eg"]:
        return value, "kilogram"
    elif unit in ["gram", "g", "grams", "gs"]:
        return value, "gram"
    elif unit in ["milligram", "mg"]:
        return value, "milligram"
    elif unit in ["microgram", "µg"]:
        return value, "microgram"
    elif unit in ["ounce", "oz"]:
        return value, "ounce"
    elif unit in ["pound", "lb"]:
        return value, "pound"
    elif unit in ["ton", "tons"]:
        return value, "ton"
    elif unit in ["litre", "l", "liter", "liters"]:
        return value, "litre"
    elif unit in ["millilitre", "ml", "milliliter", "milliliters"]:
        return value, "millilitre"
    elif unit in ["gallon", "gal", "gallons"]:
        return value, "gallon"
    elif unit in ["quart", "qt", "quarts"]:
        return value, "quart"
    elif unit in ["pint", "pt", "pints"]:
        return value, "pint"
    elif unit in ["cup", "cups"]:
        return value, "cup"
    elif unit in ["fluid ounce", "fl oz"]:
        return value, "fluid ounce"
    elif unit in ["cubic inch", "cu in"]:
        return value, "cubic inch"
    elif unit in ["cubic foot", "cu ft"]:
        return value, "cubic foot"
    elif unit in ["centilitre", "cl"]:
        return value, "centilitre"
    elif unit in ["decilitre", "dl"]:
        return value, "decilitre"
    elif unit in ["imperial gallon", "imp gal"]:
        return value, "imperial gallon"
    elif unit in ["microlitre", "µl"]:
        return value, "microlitre"
    elif unit in ["watt", "w", "watts"]:
        return value, "watt"
    elif unit in ["kilowatt", "kw", "kilowatts"]:
        return value, "kilowatt"
    elif unit in ["volt", "v", "volts"]:
        return value, "volt"
    elif unit in ["millivolt", "mv"]:
        return value, "millivolt"
    elif unit in ["kilovolt", "kv"]:
        return value, "kilovolt"
    # ... (Add more unit conversions as needed) ...
    else:
        return value, unit  # Return the original unit if no conversion found


# Function to process each row of the DataFrame (modified)
def process_text(row):
    text = row['tesseract_cleaned']

    # Check if text is a string before applying .lower()
    if isinstance(text, str):
        text = text.lower()
    else:
        # Handle cases where text is not a string (e.g., NaN or float)
        return ""  # Or handle it differently as needed

    # Extract relevant information
    if row['entity_name'] in ['depth', 'width', 'height']:
        for unit in length_units:
            if unit in text:
                match = re.search(r"(\d+(\.\d+)?) ?{}".format(unit), text)  # Extract number with unit
                if match:
                    value, standardized_unit = standardize_unit(match.group(1), unit)
                    extracted_value = "{} {}".format(value, standardized_unit)
                    print(f"Extracted value for {row['image_link']}: {extracted_value}")
                    return extracted_value

    elif row['entity_name'] in ['item_weight', 'maximum_weight_recommendation']:
        for unit in weight_units:
            if unit in text:
                match = re.search(r"(\d+(\.\d+)?) ?{}".format(unit), text)  # Extract number with unit
                if match:
                    value, standardized_unit = standardize_unit(match.group(1), unit)
                    extracted_value = "{} {}".format(value, standardized_unit)
                    print(f"Extracted value for {row['image_link']}: {extracted_value}")
                    return extracted_value

    # Add more cases for voltage, wattage, volume, etc. (follow the same pattern)
    elif row['entity_name'] in ['voltage']:
        for unit in power_units:
            if unit in text and "watt" not in unit and "ampere" not in unit: # Exclude watt and ampere units
                match = re.search(r"(\d+(\.\d+)?) ?{}".format(unit), text)
                if match:
                    value, standardized_unit = standardize_unit(match.group(1), unit)
                    extracted_value = "{} {}".format(value, standardized_unit)
                    print(f"Extracted value for {row['image_link']}: {extracted_value}")
                    return extracted_value

    elif row['entity_name'] in ['wattage']:
        for unit in power_units:
            if unit in text and "volt" not in unit and "ampere" not in unit: # Exclude volt and ampere units
                match = re.search(r"(\d+(\.\d+)?) ?{}".format(unit), text)
                if match:
                    value, standardized_unit = standardize_unit(match.group(1), unit)
                    extracted_value = "{} {}".format(value, standardized_unit)
                    print(f"Extracted value for {row['image_link']}: {extracted_value}")
                    return extracted_value

    elif row['entity_name'] in ['item_volume']: # Changed 'volume' and 'capacity' to 'item_volume'
        for unit in volume_units:
            if unit in text:
                match = re.search(r"(\d+(\.\d+)?) ?({})".format(re.escape(unit)), text) # Escape unit for regex
                if match:
                    value = match.group(1)
                    standardized_unit = standardize_unit(value, unit)[1] # Get standardized unit
                    extracted_value = "{} {}".format(value, standardized_unit)
                    print(f"Extracted value for {row['image_link']}: {extracted_value}")
                    return extracted_value

    return ""

# Apply the processing function to each row
df['extracted_value'] = df.apply(process_text, axis=1)

# Create the entity_unit_map dictionary
entity_unit_map = {}
for entity_name in df['entity_name'].unique():
    entity_unit_map[entity_name] = set()
    for index, row in df.iterrows():
        if row['entity_name'] == entity_name and row['extracted_value']: # Check if extracted_value is not empty
            parts = row['extracted_value'].rsplit(" ", 1)  # Split on the last space
            if len(parts) == 2:
                value, unit = parts
                entity_unit_map[entity_name].add(unit)
            else:
                print(f"Error: Could not split extracted value: {row['extracted_value']}")

# Print the entity_unit_map
print(entity_unit_map)

# Save results
df.to_csv("extracted_results_from_combined.csv", index=False)

print("Processing complete. Results saved to extracted_results_from_combined.csv")
