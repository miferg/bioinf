"""
rename_fasta.py es un script que va a tomar un
archivo multi fasta y le cambia los nombres
a las secuencias a un mismo formato.
"""
# Definir los nombres de los archivos
archivo_entrada = 'GCF_000208925.1_JCVI_ESG2_1.0_protein.faa'
identificador = '>entamoeba_'
archivo_de_salida = 'prueba3.faa'

# A partir de este punto no editar.
# Cargar el archivo original en una lista con lineas
handle = open(archivo_entrada, 'r')
archivo_crudo = handle.read()
handle.close()

archivo_sep = archivo_crudo.split('\n')

# Cambiar los nombres y escribir el nuevo archivo
salida = open(archivo_de_salida, 'w')
contador = 1

for i in archivo_sep:
    if '>' in i:
        i = identificador + str(contador)
        contador += 1
    salida.write(i + '\n')
salida.close()
print('¡Terminado!')
print('Puedes ir a comer.')
print('Archivo nuevo guardado como: ' + archivo_de_salida)
print()
