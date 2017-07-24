import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3


RK7Query = ET.Element("RK7Query")
RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="MenuItems")
Items = ET.SubElement(RK7Command, "Items")
ET.SubElement(Items, "Item", attrib={"GUIDString":'{' + str(uuid.uuid4()) + '}',
                                     "MainParentIdent":"{B5E17EDB-D3F5-49B2-AEEB-9A0AA5A23838}", "Code":"6",
                                     "Name":"BALSAMIQUE", "AltName":"BALSAMIQUE", "Status":"rsActive", "TaxDishType":"1",
                                     "ExtCode":"6", "PRICETYPES-3":"15000", "CLASSIFICATORGROUPS-512":"513",
                                     "genKIT_NAME":"BALSAMIQUE SOME"}).text

tree = ET.ElementTree(RK7Query)
print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
xml_send_string_create_item = ET.tostring(RK7Query, encoding='UTF-8', method='xml')
#xml_request = '<RK7Query><RK7Command CMD="GetRefData" RefName="PRICETYPES"/></RK7Query>'
ip_string = 'https://' + "192.168.45.49" + ":" + "16662" + '/rk7api/v0/xmlinterface.xml'
urllib3.disable_warnings()
response_GUID = requests.get(ip_string, data=xml_send_string_create_item, auth=("UCS", "1"), verify=False)
print(response_GUID.content)
#parsed_element_list_GUID = ET.fromstring(response_GUID.content)
#print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
#tree.write("filename.xml",encoding="UTF-8",xml_declaration='<?xml version=\"1.0\" encoding=\"UTF-8\" ?>')