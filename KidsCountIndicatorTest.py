import os
import sys
import pandas as pd

from locations_dict import locations_dict
from valid_data_formats import valid_data_formats


def validate_excel_data(file_path):
    errors = []

    try:
        df = pd.read_excel(file_path)

       # Iterate over the DataFrame row by row
        for index, row in df.iterrows():
            # Check if location is known
            if row['Location'] not in locations_dict:
                errors.append(f"Unknown location '{row['Location']}' in row {index + 2}. Value is {row['Location']}")
            else:
                # Check if LocationId matches with the dictionary
                expected_location_id = locations_dict[row['Location']]
                if row['LocationId'] != expected_location_id:
                    errors.append(f"Mismatched LocationId for '{row['Location']}' (Expected: {expected_location_id}, Found: {row['LocationId']}) in row {index + 2}")

            # Check for percentage data format
            if row['DataFormat'] == 'Percent':
                if not 0.00 <= row['Data'] <= 1.00:
                    errors.append(f"Non-decimal value {row['Data']} in 'Data' column for percentage format in row {index + 2}.")

            # Check for valid values in 'Data' column
            valid_types = (float, int)
            valid_values = ['NA', 'LNE']

            if row['DataFormat'] not in valid_data_formats:
                errors.append(f"Invalid data format '{row['DataFormat']}' in row {index + 2}")

            if not (isinstance(row['Data'], valid_types) or row['Data'] in valid_values):
                errors.append(f"Invalid value '{row['Data']}' in 'Data' column in row {index + 2}")

    except Exception as e:
        errors.append(f"Error processing Excel file: {e}")

    return errors

def is_valid_excel_file(file_path) -> bool:
    if not os.path.exists(file_path):
        print(f"The file path {file_path} does not exist.")
        return False

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() != '.xlsx':
        print(f"The file {file_path} is not an Excel file (.xlsx).")
        return False

    try:
        pd.read_excel(file_path)
        return True
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return False

def get_location_of_kids_count_indicator_excel_file() -> str:
    # Check if there is exactly one argument (excluding the script name)
    if len(sys.argv) == 2:
        kidsCountDataFile = sys.argv[1]
    else:
        # Ask the user for the file path if it's not provided as an argument
        print("Please provide the full filepath to the KidsCountIndicator data file")
        kidsCountDataFile = input()

    # Validate the provided file path
    if is_valid_excel_file(kidsCountDataFile):
        return kidsCountDataFile
    else:
        print("Invalid Excel file. Press the enter key to exit")
        input()
        exit()
    
kidsCountIndicatorExcelFile = get_location_of_kids_count_indicator_excel_file()

validation_errors = validate_excel_data(kidsCountIndicatorExcelFile)
if validation_errors:
    for error in validation_errors:
        print(error)
    print("")
    print("Please resolve the errors above.")
else:
    print("No errors found in the Excel file, congratulations!")