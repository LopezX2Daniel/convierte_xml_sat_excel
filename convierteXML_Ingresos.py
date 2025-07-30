# Actualizar la variable de "directorio_padre"
# Dentro de la carpeta de directorio_padre, debe tener esta estructura con todos los XML a convertir:
# 📁 directorio_padre/
# ├── 📄 296391be-1ef4-4d1f-8d19-573ea4e9fa5d.xml
# ├── 📄 52f5f294-041c-11ef-a42f-00155d014009.xml
# ├── 📄 f84a94c8-c477-4461-a4cd-f11c63bcc623.xml
# └── 📄 4eeb0700-840d-42e9-8810-397584000f9d.xml

import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

fechaHoy = datetime.today().strftime("%Y-%m-%d %H:%M")
print("Inicio:", fechaHoy)

directorio_padre = r"/home/files/Downloads/XML"
acumulado = {}
sepan_cuantos = 0

tipo_datos = {"ClaveProdServ": str, "ClaveUnidad": str, "Descripcion": str, "Descuento": float,
              "IVA por CFDI": float, "ObjetoImp": str, "ValorUnitario": float, "Cantidad": float, "Archivo": str, "RFC_EMISOR": str,
              "NOMBRE_EMISOR": str, "RFC_RECEPTOR": str, "NOMBRE_RECEPTOR": str, "Impuesto": str,
              "TasaOCuota": float, "UUID": str, "FechaTimbrado": str, "PxQ": float}

for archivo in os.listdir(fr"{directorio_padre}"):
    if archivo[-4:].lower() == ".xml":
        arbol = ET.parse(fr"{directorio_padre}/{archivo}")
        raiz = arbol.getroot()
        dict_cfdi_1 = raiz.attrib

        if dict_cfdi_1["TipoDeComprobante"] == "I":
            dict_datos_cfdi = {}
            listado_conceptos = []
            dict_datos_cfdi["Archivo"] = archivo

            for rama in raiz:
                if "Emisor" in str(rama):
                    try:
                        dict_datos_cfdi["RFC_EMISOR"] = rama.attrib["Rfc"]
                    except Exception as e:
                        dict_datos_cfdi["RFC_EMISOR"] = "NO DISPONIBLE"
                    try:
                        dict_datos_cfdi["NOMBRE_EMISOR"] = rama.attrib["Nombre"]
                    except Exception as e:
                        dict_datos_cfdi["NOMBRE_EMISOR"] = "NO DISPONIBLE"

                if "Receptor" in str(rama):
                    try:
                        dict_datos_cfdi["RFC_RECEPTOR"] = rama.attrib["Rfc"]
                    except Exception as e:
                        dict_datos_cfdi["RFC_RECEPTOR"] = "NO DISPONIBLE"
                    try:
                        dict_datos_cfdi["NOMBRE_RECEPTOR"] = rama.attrib["Nombre"]
                    except Exception as e:
                        dict_datos_cfdi["NOMBRE_RECEPTOR"] = "NO DISPONIBLE"

                if "Impuestos" in str(rama):
                    try:
                        if "Traslados" in str(rama[0]):
                            if "Traslado" in str(rama[0]):
                                dict_datos_cfdi["Impuesto"] = rama[0][0].attrib["Impuesto"]
                                dict_datos_cfdi["TasaOCuota"] = rama[0][0].attrib["TasaOCuota"]
                                dict_datos_cfdi["IVA por CFDI"] = rama[0][0].attrib["Importe"]
                    except Exception as e:
                        pass

                if "Complemento" in str(rama):
                    if "TimbreFiscalDigital" in str(rama[0]):
                        dict_datos_cfdi["UUID"] = rama[0].attrib["UUID"]
                        dict_datos_cfdi["FechaTimbrado"] = rama[0].attrib["FechaTimbrado"]

                if "Conceptos" in str(rama):
                    for subrama in rama:
                        listado_conceptos.append(subrama.attrib)


            for folio, concepto_unico in enumerate(listado_conceptos):
                dict_temporal = concepto_unico
                PxQ = {"PxQ": float(concepto_unico["Cantidad"])*float(concepto_unico["ValorUnitario"])}
                dict_temporal.update(PxQ)
                dict_temporal.update(dict_datos_cfdi)
                acumulado[sepan_cuantos] = dict_temporal
                sepan_cuantos+= 1


df = pd.DataFrame.from_dict(acumulado, orient="index", columns = ["ClaveProdServ", "ClaveUnidad", "Descripcion", "Descuento", "IVA por CFDI", "ObjetoImp", "Cantidad", "ValorUnitario", "PxQ", "Archivo", "RFC_EMISOR", "NOMBRE_EMISOR", "RFC_RECEPTOR", "NOMBRE_RECEPTOR", "Impuesto", "TasaOCuota", "UUID", "FechaTimbrado"])
df = df.astype(tipo_datos)
df.to_excel(fr"{directorio_padre}/datos.xlsx", index=False)

fechaHoy = datetime.today().strftime("%Y-%m-%d %H:%M")
print("Terminado:", fechaHoy)

print("Excel disponible en: ", fr"{directorio_padre}/xml_leidos.xlsx")