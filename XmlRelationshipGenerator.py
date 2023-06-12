from xml.dom import minidom
from datetime import datetime
import random
import sys
import os


class XMLKeyAdder:
    @staticmethod
    def main(xml_file_path):

        XMLKeyAdder.add_keys_to_xml(xml_file_path)

    @staticmethod
    def add_keys_to_xml(file_path):
        try:
            # Create a minidom object to parse the XML file
            doc = minidom.parse(file_path)

            # Check if a <businessId> tag is present
            business_id = XMLKeyAdder.get_business_id(doc)
            if business_id:
                # Call the methods to add primary and foreign keys
                XMLKeyAdder.add_primary_and_foreign_keys(
                    doc.documentElement, business_id, None, None)

                # Create the output directory if it doesn't exist
                output_dir = os.path.join(os.getcwd(), ".temp")
                os.makedirs(output_dir, exist_ok=True)

                # Generate the output file path
                output_file_path = os.path.join(output_dir, os.path.basename(
                    file_path).replace(".xml", "_output.xml"))

                # Write the modified document to the output file
                with open(output_file_path, "w") as output_file:
                    doc.writexml(output_file, encoding="utf-8")
                return output_file_path
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def get_business_id(doc):
        # Check if a <businessId> tag is present
        business_id_elements = doc.getElementsByTagName("businessId")
        if business_id_elements:
            business_id_element = business_id_elements[0]
            return business_id_element.firstChild.nodeValue

        return None

    @staticmethod
    def add_primary_and_foreign_keys(element, business_id, parent_key, grandparent_key):
        # Generate the primary key as current date and time along with a random integer between 10 and 100
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        random_key = str(random.randint(10, 100))
        primaryKey = now + random_key

        # Set the 'primaryKey' attribute of the current element
        element.setAttribute("primaryKey", primaryKey)

        # If a businessId is present, set the 'businessId' attribute of the current element
        if business_id:
            if element.tagName != 'business':
                element.setAttribute("businessId", business_id)

        # If the child tag occurs more than once, set the foreign key of the child tag to point to the great-grandparent
        if XMLKeyAdder.has_multiple_occurrences(element):
            element.setAttribute("parentId", grandparent_key)
        # If the child tag occurs only once, set the foreign key of the element to point to its immediate parent tag
        else:
            element.setAttribute("parentId", parent_key)

        # Process child elements recursively
        children = element.childNodes
        for child in children:
            if child.nodeType == child.ELEMENT_NODE:
                # Recursively call add_primary_and_foreign_keys for each child element
                XMLKeyAdder.add_primary_and_foreign_keys(
                    child, business_id, element.getAttribute("primaryKey"), parent_key)

    @staticmethod
    def has_multiple_occurrences(element):
        tag_name = element.tagName
        parent_node = element.parentNode
        count = 0

        # Count the number of occurrences of the element's tag name within its parent
        siblings = parent_node.childNodes
        for sibling in siblings:
            if sibling.nodeType == sibling.ELEMENT_NODE and sibling.nodeName == tag_name:
                count += 1
                if count > 1:
                    return True

        return False


# Entry point
if __name__ == "__main__":
    XMLKeyAdder.main(sys.argv[1])
