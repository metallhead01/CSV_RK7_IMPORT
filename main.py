import menu_group
import service_print_classification
import classifications_for_reports
import cathegories_in_classifications_for_reports
import modi_groups
import modi


# Создаем группы меню
create_menu_groups = menu_group.MenuGroup()
create_menu_groups.menu_group_creation()
# Создаем классификацию для сервис печати
create_classification_for_service_print = service_print_classification.ServicePrintClassification("{71B5617A-00D7-48EE-91A4-4A82C4F62642}")
create_classification_for_service_print.classification_creation()
# Создаем классификацию для отчетов
create_classifications_for_reports = classifications_for_reports.ReportsClassification()
create_classifications_for_reports.classification_creation()
# Создаем категории в классификациях для отчетов
create_cathegories = cathegories_in_classifications_for_reports.CathegoriesInClassifications()
create_cathegories.cathegory_in_classification_creation()
# Создаем схемы модификаторов
create_modi_groups = modi_groups.ModiGroups()
create_modi_groups.modi_groups()
# Создаем модификаторы
create_modi = modi.Modi()
create_modi.modi_creation()