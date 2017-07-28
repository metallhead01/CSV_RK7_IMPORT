import csv
import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3
import logging


FORMAT = '%(asctime)s : LOG : %(levelname)s - %(message)s'
logger_my_functions = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class ModiSchemes:
    def __init__(self, ip_address, port, user_name, password):
        self.ip_address = ip_address
        self.port = port
        self.user_name = user_name
        self.password = password

    def modi_schemes(self):
        with open('modi_separate.csv', newline='', ) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            l_ist = list(reader)

        l_ist_modi_schemes = []
        ok_count = 0
        error_count = 0
        for i in l_ist:
            if i[17] not in l_ist_modi_schemes and i[17] is not None and i[17] != " " and i[17] != "":
                RK7Query = ET.Element("RK7Query")
                RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="modischemes")
                Items = ET.SubElement(RK7Command, "Items")
                ET.SubElement(Items, "Item", attrib={"GUIDString":'{' + str(uuid.uuid4()) + '}',"Code":"50" + i[16],
                              "Name":i[17], "AltName":i[17], "Status":"rsActive", "ModiSchemeType":"mstUsual",
                              "AutoOpen":"false", "IgnoreDefaultForKitchen":"false"}).text

                tree = ET.ElementTree(RK7Query)
                #print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
                xml_send_string_create_item = ET.tostring(RK7Query, encoding='UTF-8', method='xml')
                ip_string = 'https://' + self.ip_address + ":" + self.port + '/rk7api/v0/xmlinterface.xml'
                urllib3.disable_warnings()
                response_GUID = requests.get(ip_string, data=xml_send_string_create_item, auth=(self.user_name, self.password), verify=False)
                logger_my_functions.debug(response_GUID.content)
                parsed_response = ET.fromstring(response_GUID.content)
                for item in parsed_response.findall("."):
                    attr_of_item_node = item.attrib
                    if attr_of_item_node.get("Status") == "Ok":
                        ok_count += 1
                    else:
                        error_count += 1
                l_ist_modi_schemes.append(i[17])
        print("ok_count_scheme: " + str(ok_count))
        print("error_count_scheme: " + str(error_count))
