import lxml.etree as ET


def validate_xml_with_xsd(xml_file, xsd_file):
    print("With XSD")
    try:
        # Load the XML file and XSD schema
        xml_tree = ET.parse(xml_file)
        xsd_tree = ET.parse(xsd_file)
        xml_schema = ET.XMLSchema(xsd_tree)

        # Validate the XML file against the XSD schema
        is_valid = xml_schema.validate(xml_tree)

        if is_valid:
            print("XML file is valid. No errors found.")
            return True
        else:
            print("XML file is not valid. Errors found:")
            error_report = "\n".join(
                f"Line {error.line}: {error.message}" for error in xml_schema.error_log)
            print(error_report)
            return False

    except ET.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
    except ET.XMLSchemaError as e:
        print(f"XML Schema Error: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


def validate_xml(xml_file):
    print("Without XSD")

    # Load the XML file
    try:
        tree = ET.parse(xml_file)
        print("XML file is valid. No errors found.")
        return True
    except ET.XMLSyntaxError as e:
        print("XML file is not valid. Errors found:")
        error_report = f"Line {e.lineno}: {e.msg}"
        print(error_report)
        return False
