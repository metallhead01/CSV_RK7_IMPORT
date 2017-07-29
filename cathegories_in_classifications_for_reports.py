import csv
import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3
import logging


class CathegoriesInClassifications:
    def __init__(self, ip_address, port, user_name, password, log_level, log_level_num):
        self.ip_address = ip_address
        self.port = port
        self.user_name = user_name
        self.password = password
        self.log_level = log_level
        self.log_level_num = log_level_num

    def cathegory_in_classification_creation(self):

        FORMAT = '%(asctime)s : LOG : %(levelname)s - %(message)s'
        logger_my_functions = logging.getLogger()
        numeric_level = getattr(logger_my_functions, self.log_level.upper(), self.log_level_num)
        logging.basicConfig(level=numeric_level, format=FORMAT)

        with open('carte_menu.csv', newline='', ) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            l_ist = list(reader)

        l_ist_cat_in_class = []
        ok_count = 0
        error_count = 0
        for i in l_ist:
            if i[10] not in l_ist_cat_in_class and i[10] is not None and i[10] != " " and i[10] != "":
                xml_classifications_request_string = '<RK7Query><RK7CMD CMD="GetRefData" ' \
                                                     'RefName="ClassificatorGroups" IgnoreEnums="1" ' \
                                                     'WithChildItems="2" WithMacroProp="1" MacroPropTags="1" ' \
                                                     'OnlyActive="1" PropMask="items.(Ident,Code,GUIDString,Name,AltName,MainParentIdent,NumInGroup,RIChildItems.(ItemIdent))"/></RK7Query>'
                ip_string = 'https://' + self.ip_address + ":" + self.port + '/rk7api/v0/xmlinterface.xml'
                urllib3.disable_warnings()
                response = requests.get(ip_string, data=xml_classifications_request_string, auth=("UCS", "1"),
                                        verify=False)
                parsed_element_list = ET.fromstring(response.content)
                for item in parsed_element_list.findall("./RK7Reference/Items/Item"):
                    attr_of_item_node = (item.attrib)
                    if i[8] == attr_of_item_node.get("Name"):
                        RK7Query = ET.Element("RK7Query")
                        RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="classificatorgroups")
                        Items = ET.SubElement(RK7Command, "Items")
                        ET.SubElement(Items, "Item", attrib={ "MainParentIdent":attr_of_item_node.get("GUIDString"),
                                                             "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                             "Code": "1002" + i[9], "Name": i[10], "AltName": i[10],
                                                             "Status": "rsActive", "ExtCode": "1002" + i[9]}).text
                        tree = ET.ElementTree(RK7Query)
                        # print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
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
                            l_ist_cat_in_class.append(i[10])

        print("ok_count: " + str(ok_count))
        print("error_count: " + str(error_count))
