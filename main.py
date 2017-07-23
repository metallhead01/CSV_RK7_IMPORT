import csv
with open('carte_menu.csv', newline='', ) as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    l_ist = list(reader)

l_ist_libellé_famille = []
l_ist_lib_fenetre =[]
for i in l_ist:
    for b in i:
        if i[8] not in l_ist_libellé_famille and i[8] is not None and i[8] != " " and i[8] != "":
            l_ist_libellé_famille.append(i[8])

for i in l_ist:
    for g in i:
        if i[17] not in l_ist_lib_fenetre and i[17] is not None and i[17] != " " and i[17] != "":
            l_ist_lib_fenetre.append(i[17])
print(l_ist_libellé_famille)
print(l_ist_lib_fenetre)

count = 0
count_1 = 0
for num in l_ist_lib_fenetre:
    count_1+=1
print(count_1)
for num_1 in l_ist_libellé_famille:
    count+=1
print(count)