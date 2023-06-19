from xml.dom import minidom
import sys
import os
import uuid


class XMLKeyAdder:
    @staticmethod
    def main(xml_file_path):

        XMLKeyAdder.add_keys_to_xml(xml_file_path)

    @staticmethod
    def add_keys_to_xml(file_path):
        try:
            # Create a minidom object to parse the XML file
            doc = minidom.parse(file_path)

            # Call the methods to add primary and foreign keys
            XMLKeyAdder.add_primary_and_foreign_keys(
                doc.documentElement, None, None)

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
    def add_primary_and_foreign_keys(element, parent_key, grandparent_key):
        # Generate the primary key as uuid 6 digit string
        primaryKey = str(uuid.uuid4().int)[0:6]
        if element.tagName == "ns2:pdmData":
            element.tagName = "ns2"
        # Remove all existing attributes from the 'ns2' element
            for attr_name in list(element.attributes.keys()):
                element.removeAttribute(attr_name)
        # Set the 'primaryKey' attribute of the current element
        element.setAttribute("primaryKey", primaryKey)

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
                    child, element.getAttribute("primaryKey"), parent_key)

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
