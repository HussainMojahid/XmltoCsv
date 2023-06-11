import csv
import xml.etree.ElementTree as ET


def convert_xml_to_csv(xml_file):
    tree = ET.parse(xml_file)
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

        # Check if non-blank columns contain only primary key and foreign key columns
        # Replace with actual primary key column names
        primary_key_columns = set(
            ["primary_key_column1", "primary_key_column2"])
        # Replace with actual foreign key column names
        foreign_key_columns = set(
            ["foreign_key_column1", "foreign_key_column2"])
        if set(non_blank_columns).issubset(primary_key_columns.union(foreign_key_columns)):
            return

        filtered_data = [
            [row[column_names.index(column)] for column in non_blank_columns] for row in data]

        if filtered_data:  # Check if filtered data has any rows
            csv_file_name = parent_tag + ".csv"
            with open(csv_file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(non_blank_columns)
                writer.writerows(filtered_data)
            print(f"CSV file '{csv_file_name}' has been created successfully.")

    parent_tags = set(element.tag for element in root.iter())

    for parent_tag in parent_tags:
        process_parent_tag(parent_tag)


xml_file_path = 'input.xml'
convert_xml_to_csv(xml_file_path)
