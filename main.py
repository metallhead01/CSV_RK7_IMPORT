import csv
with open('carte_menu_1.csv', newline='', ) as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    l_ist = list(reader)

l_ist_libellé_famille = []
l_ist_libellé_s_famille =[]
l_ist_lib_fenetre =[]
l_ist_lib_chain_fen = []
for i in l_ist:
    for b in i:
        if i[8] not in l_ist_libellé_famille and i[8] is not None and i[8] != " " and i[8] != "":
            l_ist_libellé_famille.append(i[8])

for i in l_ist:
    for g in i:
        if i[17] not in l_ist_lib_fenetre and i[17] is not None and i[17] != " " and i[17] != "":
            l_ist_lib_fenetre.append(i[17])
for i in l_ist:
    for d in i:
        if i[10] not in l_ist_libellé_s_famille and i[10] is not None and i[10] != " " and i[10] != "":
            l_ist_libellé_s_famille.append(i[10])

for i in l_ist:
    for e in i:
        if i[19] not in l_ist_lib_chain_fen and i[19] is not None and i[19] != " " and i[19] != "":
            l_ist_lib_chain_fen.append(i[19])

print(l_ist_libellé_famille)
print(l_ist_libellé_s_famille)
print(l_ist_lib_fenetre)
print(l_ist_lib_chain_fen)

count = 0
count_1 = 0
count_2 = 0
count_3 = 0
for num_1 in l_ist_libellé_famille:
    count+=1
print(count)
for num_3 in l_ist_libellé_s_famille:
    count_3+=1
print(count_3)
for num in l_ist_lib_fenetre:
    count_1+=1
print(count_1)
for num_2 in l_ist_lib_chain_fen:
    count_2+=1
print(count_2)

