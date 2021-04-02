"""
filter_blout.py filtra una tabla de salida de blast para quedarse solo con el mejor hit.
"""
import sys

if len(sys.argv) == 1:
    print ("Ejemplo: python3 filter_blout entrada.bout salida.best.bout")
    sys.exit()
else:
    nombre_entrada = sys.argv[1]
    nombre_salida = sys.argv[2]

handle = open(nombre_entrada, 'r')
tabla_raw = handle.read()
handle.close()

tabla_sep = tabla_raw.split('\n')

tabla_dic = {}
for i in tabla_sep:
    linea_sep = i.split("\t")
    if linea_sep[0] not in tabla_dic.keys():
        tabla_dic[linea_sep[0]] = [linea_sep]
    else:
        tabla_dic[linea_sep[0]] + [linea_sep]

salida = open(nombre_salida, 'w')
for i in tabla_dic.keys():
    mejor = tabla_dic[i][0]
    if len(tabla_dic[i]) > 1:
        for j in tabla_dic[i]:
            j_evalue = float(j[-2])
            if float(mejor[-2]) > j_evalue:
                mejor = j
    salida.write("\t".join(mejor) + "\n")
salida.close()
print("¡Terminado!")
