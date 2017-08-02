import menu_group_ver_2
import service_print_classification
import classifications_for_reports
import cathegories_in_classifications_for_reports_ver_2
import modi_schemes
import modi_groups
import modi
import dishes

service_print_GUID = "{71B5617A-00D7-48EE-91A4-4A82C4F62642}"
ip_address = "192.168.88.150"
port = "16662"
user_name = "UCS"
password = "1"
log_level = "info"
log_level_num = 20

# Создаем группы меню_ver_2
create_menu_groups = menu_group_ver_2.MenuGroup(ip_address, port, user_name, password, log_level, log_level_num)
create_menu_groups.menu_group_creation()

# Создаем классификацию для сервис печати
create_classification_for_service_print = service_print_classification.ServicePrintClassification(service_print_GUID, ip_address, port, user_name, password, log_level, log_level_num)
create_classification_for_service_print.classification_creation()
# Создаем классификации и категории в классификациях для отчетов
create_cathegories_for_reports = cathegories_in_classifications_for_reports_ver_2.CathegoriesInClassifications(ip_address, port, user_name, password, log_level, log_level_num)
create_cathegories_for_reports.cathegory_in_classification_creation()

# Создаем схемы модификаторов
create_modi_schemes = modi_schemes.ModiSchemes(ip_address, port, user_name, password, log_level, log_level_num)
create_modi_schemes.modi_schemes()
# Создаем группы модификаторов
create_modi_groups = modi_groups.ModiGroups(ip_address, port, user_name, password, log_level, log_level_num)
create_modi_groups.modi_groups()

# Создаем модификаторы
create_modi = modi.Modi(ip_address, port, user_name, password, log_level, log_level_num)
create_modi.modi_creation()

# Создаем блюда
dishes = dishes.Dishes(ip_address, port, user_name, password, log_level, log_level_num)
dishes.dish_creation()
