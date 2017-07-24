import csv
import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3

class MenuGroup:
    def __init__(self):
        pass

    def menu_group_creation(self):
        with open('carte_menu.csv', newline='', ) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            l_ist = list(reader)

        l_ist_menu_group = []
        ok_count = 0
        error_count = 0
        for i in l_ist:
            for b in i:
                if i[17] not in l_ist_menu_group and i[17] is not None and i[17] != " " and i[17] != "":
                    RK7Query = ET.Element("RK7Query")
                    RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="CATEGLIST")
                    Items = ET.SubElement(RK7Command, "Items")
                    ET.SubElement(Items, "Item", attrib={"GUIDString":'{' + str(uuid.uuid4()) + '}',
                                                 "Code":"1000" + i[16], "Name":i[17], "AltName":i[17], "Status":"rsActive",
                                                 "ExtCode":"1000" + i[16]}).text

                    tree = ET.ElementTree(RK7Query)
                    #print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
                    xml_send_string_create_item = ET.tostring(RK7Query, encoding='UTF-8', method='xml')
                    ip_string = 'https://' + "192.168.45.49" + ":" + "16662" + '/rk7api/v0/xmlinterface.xml'
                    urllib3.disable_warnings()
                    response_GUID = requests.get(ip_string, data=xml_send_string_create_item, auth=("UCS", "1"), verify=False)
                    #print(response_GUID.content)
                    parsed_response = ET.fromstring(response_GUID.content)
                    for item in parsed_response.findall("."):
                        attr_of_item_node = item.attrib
                        if attr_of_item_node.get("Status") == "Ok":
                            ok_count += 1
                        else:
                            error_count += 1
                    l_ist_menu_group.append(i[17])
        print("ok_count: " + str(ok_count))
        print("error_count: " + str(error_count))