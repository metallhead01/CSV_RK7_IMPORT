import csv
import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3
import logging


FORMAT = '%(asctime)s : LOG : %(levelname)s - %(message)s'
logger_my_functions = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=FORMAT)


class ServicePrintClassification:
    def __init__(self, parent_GUID):
        self.parent_GUID = parent_GUID

    def classification_creation(self):
        with open('carte_menu.csv', newline='', ) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            l_ist = list(reader)

        l_ist_classification = []
        ok_count = 0
        error_count = 0
        for i in l_ist:
            if i[8] not in l_ist_classification and i[8] is not None and i[8] != " " and i[8] != "":
                RK7Query = ET.Element("RK7Query")
                RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="classificatorgroups")
                Items = ET.SubElement(RK7Command, "Items")
                ET.SubElement(Items, "Item", attrib={ "MainParentIdent":self.parent_GUID,"GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                     "Code": "1001" + i[7], "Name": i[8], "AltName": i[8], "Status": "rsActive",
                                                     "ExtCode": "1001" + i[8]}).text
                tree = ET.ElementTree(RK7Query)
                # print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
                xml_send_string_create_item = ET.tostring(RK7Query, encoding='UTF-8', method='xml')
                ip_string = 'https://' + "192.168.45.49" + ":" + "16662" + '/rk7api/v0/xmlinterface.xml'
                urllib3.disable_warnings()
                response_GUID = requests.get(ip_string, data=xml_send_string_create_item, auth=("UCS", "1"), verify=False)
                logger_my_functions.debug(response_GUID.content)
                parsed_response = ET.fromstring(response_GUID.content)
                for item in parsed_response.findall("."):
                    attr_of_item_node = item.attrib
                    if attr_of_item_node.get("Status") == "Ok":
                        ok_count += 1
                    else:
                        error_count += 1
                l_ist_classification.append(i[8])
        print("ok_count: " + str(ok_count))
        print("error_count: " + str(error_count))