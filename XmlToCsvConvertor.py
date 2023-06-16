import csv
import xml.etree.ElementTree as ET
from XmlRelationshipGenerator import *
from XmlValidator import *
import sys


def convert_xml_to_csv(xml_file, xsd_file):
    output_folder = "output"
    is_xml_valid = False
    os.makedirs(output_folder, exist_ok=True)

    if xsd_file is not None:
        is_xml_valid = validate_xml_with_xsd(xml_file, xsd_file)
    else:
        is_xml_valid = validate_xml(xml_file)

    if is_xml_valid:
        temp_file = XMLKeyAdder.add_keys_to_xml(
            xml_file)  # Generating Relationship

        tree = ET.parse(temp_file)
        root = tree.getroot()

        def process_parent_tag(parent_tag):
            child_tags = set()
            attribute_names = set()

            for element in root.iter(parent_tag):
                child_tags.update(child.tag for child in element)
                attribute_names.update(element.attrib.keys())

            column_names = list(attribute_names) + list(child_tags)

            data = []
            for element in root.iter(parent_tag):
                row_data = []
                has_direct_value = False  # Flag to check if element has direct value
                for column_name in column_names:
                    if column_name in attribute_names:
                        row_data.append(element.attrib.get(
                            column_name, "").strip())
                    else:
                        child_element = element.find(column_name)
                        if child_element is not None and child_element.text is not None:
                            row_data.append(child_element.text.strip())
                            has_direct_value = True
                        else:
                            row_data.append("")
                if has_direct_value:  # Only append rows with direct values
                    data.append(row_data)

            non_blank_columns = [column for column in column_names if any(
                row[column_names.index(column)] != "" for row in data)]

            # Exclude elements with specific attribute combinations
            exclude_combinations = [
                {"businessId"},
                {"parentId"},
                {"primaryKey"},
                {"businessId", "parentId"},
                {"businessId", "primaryKey"},
                {"parentId", "primaryKey"},
                {"parentId", "primaryKey", "businessId"}
            ]
            if set(non_blank_columns) in exclude_combinations:
                return

            filtered_data = [
                [row[column_names.index(column)] for column in non_blank_columns] for row in data]

            if filtered_data:  # Check if filtered data has any rows
                os.makedirs(output_folder+"/"+parent_tag, exist_ok=True)
                csv_file_name = os.path.join(
                    (output_folder+"/"+parent_tag), parent_tag + ".csv")
                with open(csv_file_name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(non_blank_columns)
                    writer.writerows(filtered_data)
        print("CSV files has been created successfully.")

        parent_tags = set(element.tag for element in root.iter())

        for parent_tag in parent_tags:
            process_parent_tag(parent_tag)
        # os.remove(temp_file)
    else:
        print("Invalid XML")


if (len(sys.argv) == 1):
    print("Please provide XML path")
else:
    xml_file_path = sys.argv[1]
    xsd_file_path = None
    if len(sys.argv) >= 3:
        xsd_file_path = sys.argv[2]
    convert_xml_to_csv(xml_file_path, xsd_file_path)
