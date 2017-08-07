import csv
import xml.etree.cElementTree as ET
import requests
import uuid
import urllib3
import logging
import sqlite3



class Dishes:
    def __init__(self, ip_address, port, user_name, password, log_level, log_level_num):
        self.ip_address = ip_address
        self.port = port
        self.user_name = user_name
        self.password = password
        self.log_level = log_level
        self.log_level_num = log_level_num

    def dish_creation(self):
        FORMAT = '%(asctime)s : LOG : %(levelname)s - %(message)s'
        logger_my_functions = logging.getLogger()
        numeric_level = getattr(logger_my_functions, self.log_level.upper(), self.log_level_num)
        logging.basicConfig(level=numeric_level, format=FORMAT)

        db = sqlite3.connect("rk7.db")
        cur = db.cursor()
        cur.execute('''DROP TABLE IF EXISTS CLASSIFICATORGROUPS''')
        cur.execute('''DROP TABLE IF EXISTS CATEGLIST''')
        cur.execute(
            '''CREATE TABLE CLASSIFICATORGROUPS ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT, GUID TEXT, Ident TEXT, MainParentIdent TEXT)''')
        cur.execute(
            '''CREATE TABLE CATEGLIST ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT, GUID TEXT, Ident TEXT, MainParentIdent TEXT)''')
        cur.close()

        with open('carte_menu-structure.csv', newline='', encoding="utf-16-le") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            l_ist = list(reader)

        def sql_db_filling(reference):
            db = sqlite3.connect("rk7.db")
            cur = db.cursor()
            xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName="' + reference + '" IgnoreEnums="1" ' \
                                                 'WithChildItems="2" WithMacroProp="1" MacroPropTags="1" ' \
                                                 'OnlyActive="1" PropMask="items.(Ident,Code,GUIDString,Name,AltName,MainParentIdent,NumInGroup,RIChildItems.(ItemIdent))"/></RK7Query>'
            ip_string = 'https://' + self.ip_address + ":" + self.port + '/rk7api/v0/xmlinterface.xml'
            urllib3.disable_warnings()
            response= requests.get(ip_string, data=xml_request_string, auth=(self.user_name, self.password), verify=False)
            parsed_element_list = ET.fromstring(response.content)
            for item_class in parsed_element_list.findall("./RK7Reference/Items/Item"):
                attr_of_item_node_class = (item_class.attrib)
                cur = db.cursor()
                cur.execute ('''INSERT INTO %s (Name, GUID, Ident, MainParentIdent) VALUES (?, ?, ?, ?)''' % (reference),
                             (attr_of_item_node_class.get("Name"), attr_of_item_node_class.get("GUIDString"),
                              attr_of_item_node_class.get("Ident"), attr_of_item_node_class.get("MainParentIdent")))

            cur.close()
            db.commit()
            db.close()

        ok_count = 0
        error_count = 0

        def xml_send():
            tree = ET.ElementTree(RK7Query)
            # print(ET.tostring(RK7Query, encoding='unicode', method='xml'))
            xml_send_string_create_item = ET.tostring(RK7Query, encoding='UTF-8', method='xml')
            ip_string = 'https://' + self.ip_address + ":" + self.port + '/rk7api/v0/xmlinterface.xml'
            urllib3.disable_warnings()
            response_GUID = requests.get(ip_string, data=xml_send_string_create_item,
                                         auth=(self.user_name, self.password), verify=False)
            #logger_my_functions.debug(response_GUID.content)
            parsed_response = ET.fromstring(response_GUID.content)
            for item in parsed_response.findall("."):
                attr_of_item_node = item.attrib
                if attr_of_item_node.get("Status") == "Ok":
                    global ok_count
                    #ok_count += 1
                else:
                    global error_count
                    #error_count += 1

        def sql_request(a):
            cur = db.cursor()
            cur_1 = db.cursor()
            cur_2 = db.cursor()
            cur_3 = db.cursor()
            cur.execute('SELECT * FROM CATEGLIST WHERE "Name"=(?)', (i[a],))
            # Famile
            cur_1.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" != "512"', (i[8],))
            # S famile
            cur_2.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?)', (i[10],))
            cur_3.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" = "512"'
                          , (i[8],))
            catheg = cur.fetchall()
            classif = cur_1.fetchall()
            classif_1 = cur_2.fetchall()
            service = cur_3.fetchall()
            return catheg, classif, classif_1, service


        sql_db_filling("CLASSIFICATORGROUPS")
        sql_db_filling("CATEGLIST")

        l_ist_dishes = []

        for i in l_ist:
            if i[1] not in l_ist_dishes and i[1] is not None and i[1] != " " and i[1] != "":
                if i[26] is not None and i[26] != " " and i[26] != "":
                    cur = db.cursor()
                    cur_1 = db.cursor()
                    cur_2 = db.cursor()
                    cur_3 = db.cursor()
                    cur.execute('SELECT * FROM CATEGLIST WHERE "Name"=(?)', (i[26],))
                    #Famile
                    cur_1.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" != "512"', (i[8],))
                    #S famile
                    cur_2.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?)', (i[10],))
                    cur_3.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" = "512"'
                                  , (i[8],))
                    catheg = cur.fetchall()
                    classif = cur_1.fetchall()
                    classif_1 = cur_2.fetchall()
                    service = cur_3.fetchall()
                    if i[26] == catheg[0][1]:
                        RK7Query = ET.Element("RK7Query")
                        RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="MENUITEMS")
                        Items = ET.SubElement(RK7Command, "Items")
                        if i[8] != " " and i[10] != " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent" : catheg[0][2],
                                                             "GUIDString" : '{' + str(uuid.uuid4()) + '}',
                                                             "Code": i[2], "Name" : i[1], "AltName" : i[3],
                                                             "Status": "rsActive", "PRICETYPES-3" : price,
                                                             "CLASSIFICATORGROUPS-" + classif[0][4] : classif[0][3],
                                                             "CLASSIFICATORGROUPS-" + classif_1[0][4] : classif_1[0][3],
                                                             "CLASSIFICATORGROUPS-" + service[0][4] : service[0][3],
                                                             "TaxDishType" : "2", "genKIT_NAME" : i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] != " " and i[10] == " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name" : i[1], "AltName" : i[3],
                                                                 "Status" : "rsActive", "PRICETYPES-3" : price,
                                                                 "CLASSIFICATORGROUPS-" + classif[0][4] : classif[0][3],
                                                                 "CLASSIFICATORGROUPS-" + service[0][4] : service[0][3],
                                                                 "TaxDishType" :"2", "genKIT_NAME" : i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] == " " and i[10] != " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName" : i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "CLASSIFICATORGROUPS-" + classif_1[0][4]: classif_1[0][3],
                                                                 "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] == " " and i[10] == " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName" : i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                    l_ist_dishes.append(i[1])
                elif [25] is not None and i[25] != " " and i[25] != "":
                    cur = db.cursor()
                    cur_1 = db.cursor()
                    cur_2 = db.cursor()
                    cur_3 = db.cursor()
                    cur.execute('SELECT * FROM CATEGLIST WHERE "Name"=(?)', (i[25],))
                    cur_1.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" != "512"', (i[8],))
                    cur_2.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?)', (i[10],))
                    cur_3.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" = "512"', (i[8],))
                    catheg = cur.fetchall()
                    classif = cur_1.fetchall()
                    classif_1 = cur_2.fetchall()
                    service = cur_3.fetchall()
                    if i[25] == catheg[0][1]:
                        RK7Query = ET.Element("RK7Query")
                        RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData", RefName="MENUITEMS")
                        Items = ET.SubElement(RK7Command, "Items")
                        if i[8] != " " and i[10] != " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                             "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                             "Code": i[2], "Name"  i[1], "AltName": i[3],
                                                             "Status": "rsActive", "PRICETYPES-3" : price,
                                                             "CLASSIFICATORGROUPS-" + classif[0][4] : classif[0][3],
                                                             "CLASSIFICATORGROUPS-" + classif_1[0][4] : classif_1[0][3],
                                                             "CLASSIFICATORGROUPS-" + service[0][4] : service[0][3],
                                                             "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] != " " and i[10] == " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName" : i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "CLASSIFICATORGROUPS-" + classif[0][4] : classif[0][3],
                                                                 "CLASSIFICATORGROUPS-" + service[0][4] : service[0][3],
                                                                 "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] == " " and i[10] != " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName" : i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "CLASSIFICATORGROUPS-" + classif_1[0][4]: classif_1[0][3],
                                                                 "TaxDishType":"2", "genKIT_NAME" : i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] == " " and i[10] == " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName": i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                    l_ist_dishes.append(i[1])
                elif [24] is not None and i[24] != " " and i[24] != "":
                    cur = db.cursor()
                    cur_1 = db.cursor()
                    cur_2 = db.cursor()
                    cur_3 = db.cursor()
                    cur.execute('SELECT * FROM CATEGLIST WHERE "Name"=(?)', (i[24],))
                    cur_1.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" != "512"', (i[8],))
                    cur_2.execute('SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?)', (i[10],))
                    cur_3.execute(
                        'SELECT * FROM CLASSIFICATORGROUPS WHERE "Name"=(?) AND "MainParentIdent" = "512"'
                        , (i[8],))
                    catheg = cur.fetchall()
                    classif = cur_1.fetchall()
                    classif_1 = cur_2.fetchall()
                    service = cur_3.fetchall()
                    if i[24] == catheg[0][1]:
                        RK7Query = ET.Element("RK7Query")
                        RK7Command = ET.SubElement(RK7Query, "RK7Command", CMD="SetRefData",
                                                   RefName="MENUITEMS")
                        Items = ET.SubElement(RK7Command, "Items")
                        if i[8] != " " and i[10] != " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                             "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                             "Code": i[2], "Name": i[1], "AltName": i[3],
                                                             "Status": "rsActive", "PRICETYPES-3" : price,
                                                             "CLASSIFICATORGROUPS-" + classif[0][4]: classif[0][3],
                                                             "CLASSIFICATORGROUPS-" + classif_1[0][4] : classif_1[0][3],
                                                             "CLASSIFICATORGROUPS-" + service[0][4]: service[0][3],
                                                             "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] != " " and i[10] == " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName": i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "CLASSIFICATORGROUPS-" + classif[0][4]: classif[0][3],
                                                                 "CLASSIFICATORGROUPS-" + service[0][4]: service[0][3],
                                                                 "TaxDishType":"2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] == " " and i[10] != " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString": '{' + str(uuid.uuid4()) + '}',
                                                                 "Code": i[2], "Name": i[1], "AltName": i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "CLASSIFICATORGROUPS-" + classif_1[0][4]: classif_1[0][3],
                                                                 "TaxDishType" : "2", "genKIT_NAME": i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                        elif i[8] == " " and i[10] == " ":
                            if i[4] != " ":
                                price = str(int(float(i[4]))*100)
                            else:
                                price = "0"
                            ET.SubElement(Items, "Item", attrib={"MainParentIdent": catheg[0][2],
                                                                 "GUIDString" : '{' + str(uuid.uuid4()) + '}',
                                                                 "Code" : i[2], "Name" : i[1], "AltName" : i[3],
                                                                 "Status": "rsActive", "PRICETYPES-3" : price,
                                                                 "TaxDishType" : "2", "genKIT_NAME" : i[21]}).text
                            cur.close()
                            cur_1.close()
                            cur_2.close()
                            cur_3.close()
                            xml_send()
                    l_ist_dishes.append(i[1])
                else:
                    l_ist_dishes.append(i[1])
                    pass
        print("ok_count_dish: " + str(ok_count))
        print("error_count_dish: " + str(error_count))
"""
service_print_GUID = "{71B5617A-00D7-48EE-91A4-4A82C4F62642}"
ip_address = "192.168.88.150"
port = "16662"
user_name = "UCS"
password = "1"
log_level = "info"
log_level_num = 10

create = Dishes(ip_address, port, user_name, password, log_level, log_level_num)
create.dish_creation()
"""