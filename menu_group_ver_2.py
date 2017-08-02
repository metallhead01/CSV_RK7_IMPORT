import csv
import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3
import logging
'''Вторая итерация после точнения ТЗ заказчиком - изменена структура для импорта (заказчик решил использовать дополнительные колонки)'''


class MenuGroup:
    def __init__(self, ip_address, port, user_name, password, log_level, log_level_num):
        self.ip_address = ip_address
        self.port = port
        self.user_name = user_name
        self.password = password
        self.log_level = log_level
        self.log_level_num = log_level_num

    def menu_group_creation(self):

        logger_my_functions = logging.getLogger()
        FORMAT = '%(asctime)s : LOG : %(levelname)s - %(message)s'
        # Установили уровень 10 под DEBUG, остальные уровни с шагом 10 вверх: 20, 30, etc.
        numeric_level = getattr(logger_my_functions, self.log_level.upper(), self.log_level_num)
        logging.basicConfig(level=numeric_level, format=FORMAT)

        with open('carte_menu-structure.csv', newline='', encoding="utf-16-le") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            l_ist = list(reader)

        l_ist_menu_group = []
        l_ist_menu_group_sub_group = []
        l_ist_menu_group_sub_sub_group = []
        l_ist_menu_group_sub_sub_sub_group = []

        __ok_count = 0
        __error_count = 0
        def submenu_group_creation(a,b):
            ok_count = 0
            error_count = 0
            xml_classifications_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName="CATEGLIST" IgnoreEnums="1" ' \
                                                 'WithChildItems="2" WithMacroProp="1" MacroPropTags="1" ' \
                                                 'OnlyActive="1" PropMask="items.(Ident,Code,GUIDString,Name,AltName,MainParentIdent,NumInGroup,RIChildItems.(ItemIdent))"/></RK7Query>'
            ip_string = 'https://' + self.ip_address + ":" + self.port + '/rk7api/v0/xmlinterface.xml'
            urllib3.disable_warnings()
            response = requests.get(ip_string, data=xml_classifications_request_string,
                                    auth=(self.user_name, self.password),
                                    verify=False)
            parsed_element_list = ET.fromstring(response.content)
            for item in parsed_element_list.findall("./RK7Reference/Items/Item"):
                attr_of_item_node = (item.attrib)
                if i[a] == attr_of_item_node.get("Name"):
                    if i[b] not in l_ist_menu_group_sub_group and i[b] is not None and i[b] != " " and i[b] != "":
                        RK7Query = ET.Element("RK7Query")
                        RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="CATEGLIST")
                        Items = ET.SubElement(RK7Command, "Items")
                        ET.SubElement(Items, "Item", attrib={"GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                             "MainParentIdent": attr_of_item_node.get("Ident"),
                                                             "Name": i[b], "AltName": i[b],
                                                             "Status": "rsActive"}).text
                        tree = ET.ElementTree(RK7Query)
                        # print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
                        xml_send_string_create_item = ET.tostring(RK7Query, encoding='UTF-8', method='xml')
                        ip_string = 'https://' + self.ip_address + ":" + self.port + '/rk7api/v0/xmlinterface.xml'
                        urllib3.disable_warnings()
                        response_GUID = requests.get(ip_string, data=xml_send_string_create_item,
                                                     auth=(self.user_name, self.password), verify=False)
                        logger_my_functions.debug(response_GUID.content)
                        parsed_response = ET.fromstring(response_GUID.content)
                        for item in parsed_response.findall("."):
                            attr_of_item_node = item.attrib
                            if attr_of_item_node.get("Status") == "Ok":
                                ok_count += 1
                            else:
                                error_count += 1
                        l_ist_menu_group_sub_group.append(i[b])
            return ok_count, error_count

        for i in l_ist:
            if i[23] not in l_ist_menu_group and i[23] is not None and i[23] != " " and i[23] != "":
                RK7Query = ET.Element("RK7Query")
                RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="CATEGLIST")
                Items = ET.SubElement(RK7Command, "Items")
                ET.SubElement(Items, "Item", attrib={"GUIDString":'{' + str(uuid.uuid4()) + '}', "MainParentIdent":"0",
                              "Name":i[23], "AltName":i[23], "Status":"rsActive"}).text
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
                        __ok_count += 1
                    else:
                        __error_count += 1
                l_ist_menu_group.append(i[23])

        #print("ok_count: " + str(__ok_count))
        #print("error_count: " + str(__error_count))

        for i in l_ist:
            submenu_group_creation(23,24)

        #print("ok_count: " + str(__ok_count))
        #print("error_count: " + str(__error_count))

        for i in l_ist:
            submenu_group_creation(24, 25)

        #print("ok_count: " + str(__ok_count))
        #print("error_count: " + str(__error_count))

        for i in l_ist:
            submenu_group_creation(25, 26)

        #print("ok_count: " + str(__ok_count))
        #print("error_count: " + str(__error_count))
"""
ip_address = "192.168.88.150"
port = "16662"
user_name = "UCS"
password = "1"
log_level = "info"
log_level_num = 10

create = MenuGroup(ip_address, port, user_name, password, log_level, log_level_num)
create.menu_group_creation()
"""