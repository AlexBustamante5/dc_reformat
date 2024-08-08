# python3 reformat.py non_dupes_records reformat_records

import os
import xml.etree.ElementTree as ET
import argparse
import argparse
from pymarc import parse_xml_to_array
from xml.dom import minidom

def get_dc_fields(file_path):
    '''
    extracts dublin core fields from a MARC XML file
    takes in path to the MARC XML file
    returns a list of tuples containing dc tags and their values, and the identifier
    '''
    dc_fields = []
    
    with open(file_path, 'rb') as file:
        reader = parse_xml_to_array(file)
        for record in reader:
            for field in record.get_fields('245'):
                dc_fields.append(("dc:title", field['a']))

            for field in record.get_fields('100'):
                dc_fields.append(("dc:creator", field['a']))

            for field in record.get_fields('700'):
                subfield_a = field.get_subfields('a')
                for value in subfield_a:
                    dc_fields.append(("dc:creator", value))

            #hard code type
            dc_fields.append(("dc:type","Book"))

            for field in record.get_fields('260'):
                dc_fields.append(("dc:publisher", field['a']))

            for field in record.get_fields('260'):
                dc_fields.append(("dc:date", field['c']))

            for field in record.get_fields('505'):
                for subfield in field.get_subfields('a'):
                    dc_fields.append(("dc:description", subfield))

            for field in record.get_fields('650'):
                dc_fields.append(("dc:subject", field['a']))

            for field in record.get_fields('999'):
                if 'c' in field:
                    identifier = "https://ilob-olbi.juliencouturecentre.ca/cgi-bin/koha/opac-detail.pl?biblionumber=" + field['c']
                    dc_fields.append(("dc:identifier", identifier))
    
    return dc_fields, identifier

def create_dc_tree(dc_fields, identifier):
    '''
    creates XML tree with dc fields
    takes:
        dc_fields (list)
        identifier (str)
    returns root element of the XML tree.
    '''
    root = ET.Element("record")

    sub_1 = ET.SubElement(root, "header")

    sub_2 = ET.SubElement(sub_1, "identifier")
    sub_2.text = identifier

    sub_3 = ET.SubElement(root, "metadata")

    namespaces = {
    "xmlns:oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "xmlns:dc": "http://purl.org/dc/elements/1.1/",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsi:schemaLocation": "http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
    }

    sub_4 = ET.SubElement(sub_3, "oai_dc:dc", namespaces)

    for tag, value in dc_fields:
        field_element = ET.SubElement(sub_4, tag)
        field_element.text = value
    
    return root

def write_pretty_xml(root, output_path):
    '''
    writes the XML tree to a file with pretty printing
    takes:
        root (Element)
        output_path (str)
    '''
    # tree = ET.ElementTree(root)
    # tree.write(output_path, encoding='utf-8', xml_declaration=True)

    # ET.tostring serializes the root element and its children to a byte string using utf-8 encoding
    # .decode converts the byte string to a regular string
    xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # minidom.parseString(xml_str) takes the XML string and parses it into a DOM structure
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ", newl='\n', encoding=None)

    # remove the XML declaration
    pretty_xml_str = '\n'.join(pretty_xml_str.split('\n')[1:])

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml_str)

def reformat(input_path, output_path):

    dc_fields, identifier = get_dc_fields(input_path)
    root = create_dc_tree(dc_fields, identifier)
    write_pretty_xml(root, output_path)

def main(input_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)
    
    for input_name in os.listdir(input_folder):
        if input_name.endswith('.xml'):
            output_name = input_name.replace('.xml', '_dc2.xml')
            output_path = os.path.join(output_folder, output_name)
            input_path = os.path.join(input_folder, input_name)

            try:
                reformat(input_path, output_path)
            except Exception as e:
                print(f"Error processing {input_name} : {e}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process MARCXML records and reformats it into Dublin Core with added fields.')
    parser.add_argument('input_folder', help='Path to the input record files')
    parser.add_argument('output_folder', help='Directory to save the reformated record files')
    args = parser.parse_args()

    main(args.input_folder, args.output_folder)
