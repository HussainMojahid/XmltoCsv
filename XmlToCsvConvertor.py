
import csv
import xml.etree.ElementTree as ET


def convert_xml_to_csv(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    def process_parent_tag(parent_tag):
        csv_file_name = parent_tag + ".csv"

        child_tags = set()
        attributes = set()

        for element in root.iter(parent_tag):
            child_tags.update(child.tag for child in element)
            attributes.update(element.attrib.keys())

        data = []
        non_blank_columns = list(child_tags) + list(attributes)

        for element in root.iter(parent_tag):
            row_data = []
            for child_tag in child_tags:
                child_element = element.find(child_tag)
                row_data.append(child_element.text.strip() if child_element is not None and child_element.text is not None else "")

            for attribute in attributes:
                row_data.append(element.attrib.get(attribute, ""))

            data.append(row_data)

        with open(csv_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(non_blank_columns)
            writer.writerows(data)

        print(f"CSV file '{csv_file_name}' has been created successfully.")

    parent_tags = set(element.tag for element in root.iter())

    for parent_tag in parent_tags:
        process_parent_tag(parent_tag)


xml_file_path = 'test.xml'
convert_xml_to_csv(xml_file_path)
