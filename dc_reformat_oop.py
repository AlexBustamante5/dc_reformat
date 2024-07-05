import xml.etree.ElementTree as ET
import os

class DCReformat:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.input_path = ""
        self.output_path = ""

    def generate_file(self):
        os.makedirs(self.output_folder, exist_ok=True)
        for input_name in os.listdir(self.input_folder):
            # print(input_name)
            output_name = input_name.replace('.dublin-core.xml', '_dc2.xml')
            self.output_path = os.path.join(self.output_folder, output_name)
        # debug
            if input_name.endswith('.xml'):
                self.input_path = os.path.join(self.input_folder + input_name)

                try:
                    self.reformat(self.input_path, self.output_path)
                except Exception as e:
                    print(f"Error processing {input_name} : {e}")
                    continue
                
    def reformat(input_path, output_path):
        try:
            tree = ET.parse(input_path)
            root = tree.getroot()

            # get identifier
            split = input_path.split('.')
            id_no = split[0].split('-')[1]
            identifier = "https://ilob-olbi.juliencouturecentre.ca:8888/cgi-bin/koha/catalogue/detail.pl?biblionumber=" + id_no

            # oai_dc
            key = "oai_dc:dc"
            value = '''xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                            xmlns:dc="http://purl.org/dc/elements/1.1/"
                            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                            xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd"'''

            # list of tuples
            dc_fields = []

            # iterates over each elem in the xml
            for child in root:
                # extracts field name + value
                field_key = child.tag.split('}')[-1]
                field_value = child.text.strip() if child.text else ''
                
                dc_fields.append((field_key, field_value))
            
            for dc_field in dc_fields:
                if dc_field[0].strip() == "type":
                    dc_field_list = list(dc_field)
                    dc_field_list[1] = "Book"
                    dc_fields[dc_fields.index(dc_field)] = tuple(dc_field_list)
            # print(dc_fields)

            # creates new list without identifiers
            updated_fields = [field for field in dc_fields if field[0].strip() != "identifier"]
            ## debug
            # for field in updated_fields:
            #     print(field)

            with open(output_path, 'w') as file:
                file.write('<record> \n' + '\t<header> \n')
                file.write('\t \t <identifier>'+ identifier + '</identifier> \n')
                file.write('\t</header> \n\t<metadata> \n')
                file.write('\t\t<'+ key +' ' + value +'>\n')

                # iterates over list of tuples
                for field in updated_fields:
                    line = "\t\t\t<dc:" + field[0].strip() + ">" + field[1] + " </dc:" + field[0].strip() + ">"
                    file.write(line + '\n')

                file.write('\t\t\t<identifier>'+ identifier + '</identifier> \n')
                file.write('\t\t</'+ key +'>\n')
                file.write('\t</metadata>\n')
                file.write('</record>')
            
        except Exception as e:
            raise e