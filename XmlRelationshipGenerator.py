
import xml.etree.ElementTree as ET

def add_primary_key(root, primary_key=1):
    root.set('primary_key', str(primary_key))
    for child in root:
        primary_key += 1
        add_primary_key(child, primary_key)

def add_foreign_key(root):
    for element in root.iter():
        for child in element:
            foreign_key = element.get('primary_key')
            if foreign_key is not None:
                child.set('foreign_key', foreign_key)

def add_keys_to_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    add_primary_key(root)
    add_foreign_key(root)
    tree.write(file_path)

# Usage
xml_file = "ts.xml"
add_keys_to_xml(xml_file)
