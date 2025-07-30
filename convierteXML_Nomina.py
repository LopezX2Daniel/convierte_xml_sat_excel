# Actualizar la variable de "directorio_padre"
# En la variable "VERSION" se declara la versión del CFDI para procesar el parsing específico
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

VERSION = "1.1"
# VERSION = "1.2"

fechaHoy = datetime.today().strftime("%Y-%m-%d %H:%M")
print("Inicio:", fechaHoy)

directorio_padre = r"/home/files/Downloads/XML"
acumulado = {}
sepan_cuantos = 0


if VERSION == "1.1":
    for archivo in os.listdir(fr"{directorio_padre}"):
        if archivo[-4:].lower() == ".xml":
            arbol = ET.parse(fr"{directorio_padre}/{archivo}")
            raiz = arbol.getroot()
            dict_cfdi_1 = raiz.attrib

            if dict_cfdi_1["TipoDeComprobante"] == "N":
                dict_datos_cfdi = {}
                listado_conceptos = []
                dict_datos_cfdi["Archivo"] = archivo

                dict_datos_cfdi["TipoDeComprobante"] = dict_cfdi_1["TipoDeComprobante"]

                for rama in raiz:
                    # EMISOR
                    if "Emisor" in str(rama):
                        try:
                            dict_datos_cfdi["RFC_EMISOR"] = rama.attrib["Rfc"]
                        except Exception as e:
                            dict_datos_cfdi["RFC_EMISOR"] = "NO DISPONIBLE"
                        try:
                            dict_datos_cfdi["NOMBRE_EMISOR"] = rama.attrib["Nombre"]
                        except Exception as e:
                            dict_datos_cfdi["NOMBRE_EMISOR"] = "NO DISPONIBLE"

                    # RECEPTOR
                    if "Receptor" in str(rama):
                        try:
                            dict_datos_cfdi["RFC_RECEPTOR"] = rama.attrib["Rfc"]
                        except Exception as e:
                            dict_datos_cfdi["RFC_RECEPTOR"] = "NO DISPONIBLE"
                        try:
                            dict_datos_cfdi["NOMBRE_RECEPTOR"] = rama.attrib["Nombre"]
                        except Exception as e:
                            dict_datos_cfdi["NOMBRE_RECEPTOR"] = "NO DISPONIBLE"

                    # DATOS COMPLEMENTARIOS
                    if "Complemento" in str(rama):
                        if "TimbreFiscalDigital" in str(rama[0]):
                                dict_datos_cfdi["UUID"] = rama[0].attrib["UUID"]
                                dict_datos_cfdi["FechaTimbrado"] = rama[0].attrib["FechaTimbrado"]

                        if "Nomina" in str(rama[1]):
                            dict_datos_cfdi["TotalDeducciones"] = rama[1].attrib["TotalDeducciones"]
                            dict_datos_cfdi["TotalPercepciones"] = rama[1].attrib["TotalPercepciones"]
                            dict_datos_cfdi["TotalOtrosPagos"] = rama[1].attrib["TotalOtrosPagos"]
                            dict_datos_cfdi["FechaInicialPago"] = rama[1].attrib["FechaInicialPago"]
                            dict_datos_cfdi["FechaFinalPago"] = rama[1].attrib["FechaFinalPago"]

                            if "Emisor" in str(rama[1][0]):
                                dict_datos_cfdi["RegistroPatronal"] = rama[1][0].attrib["RegistroPatronal"]

                    # COMPLEMENTOS
                    if "Complemento" in str(rama):
                        for subrama in rama:
                            if "Nomina" in str(subrama):
                                for subsubrama in subrama:
                                    if "Percepciones" in str(subsubrama):
                                        for percepcion in subsubrama:
                                            listado_conceptos.append(percepcion.attrib)

                                    if "Deducciones" in str(subsubrama):
                                        for deduccion in subsubrama:
                                            listado_conceptos.append(deduccion.attrib)

                for folio, concepto_unico in enumerate(listado_conceptos):
                    dict_temporal = concepto_unico
                    dict_temporal.update(dict_datos_cfdi)
                    acumulado[sepan_cuantos] = dict_temporal
                    sepan_cuantos+= 1


    df = pd.DataFrame.from_dict(acumulado, orient="index")
    df["Importe"] = df["Importe"].astype(float)
    df["ImporteGravado"] = df["ImporteGravado"].astype(float)
    df["ImporteExento"] = df["ImporteExento"].astype(float)
    df["TotalPercepciones"] = df["TotalPercepciones"].astype(float)
    df["TotalDeducciones"] = df["TotalDeducciones"].astype(float)
    df["TotalOtrosPagos"] = df["TotalOtrosPagos"].astype(float)
    df = df[["Archivo", "UUID", "NOMBRE_RECEPTOR", "RFC_RECEPTOR", "NOMBRE_EMISOR", "RFC_EMISOR", "TipoDeComprobante", "FechaTimbrado", "RegistroPatronal",
             "FechaInicialPago", "FechaFinalPago", "Clave", "TipoPercepcion", "TipoDeduccion", "Concepto", "Importe", "ImporteGravado", "ImporteExento",
             "TotalPercepciones", "TotalDeducciones", "TotalOtrosPagos"]]
    df.to_excel(fr"{directorio_padre}/xml_leidos.xlsx", index=False)

    fechaHoy = datetime.today().strftime("%Y-%m-%d %H:%M")
    print("Terminado:", fechaHoy)

    print("Excel disponible en: ", fr"{directorio_padre}/xml_leidos.xlsx")

if VERSION == "1.2":
    for archivo in os.listdir(fr"{directorio_padre}"):
        if archivo[-4:].lower() == ".xml":
            arbol = ET.parse(fr"{directorio_padre}/{archivo}")
            raiz = arbol.getroot()
            dict_cfdi_1 = raiz.attrib

            if dict_cfdi_1["TipoDeComprobante"] == "N":
                dict_datos_cfdi = {}
                listado_conceptos = []
                dict_datos_cfdi["Archivo"] = archivo

                dict_datos_cfdi["TipoDeComprobante"] = dict_cfdi_1["TipoDeComprobante"]

                for rama in raiz:
                    # EMISOR
                    if "Emisor" in str(rama):
                        try:
                            dict_datos_cfdi["RFC_EMISOR"] = rama.attrib["Rfc"]
                        except Exception as e:
                            dict_datos_cfdi["RFC_EMISOR"] = "NO DISPONIBLE"
                        try:
                            dict_datos_cfdi["NOMBRE_EMISOR"] = rama.attrib["Nombre"]
                        except Exception as e:
                            dict_datos_cfdi["NOMBRE_EMISOR"] = "NO DISPONIBLE"

                    # RECEPTOR
                    if "Receptor" in str(rama):
                        try:
                            dict_datos_cfdi["RFC_RECEPTOR"] = rama.attrib["Rfc"]
                        except Exception as e:
                            dict_datos_cfdi["RFC_RECEPTOR"] = "NO DISPONIBLE"
                        try:
                            dict_datos_cfdi["NOMBRE_RECEPTOR"] = rama.attrib["Nombre"]
                        except Exception as e:
                            dict_datos_cfdi["NOMBRE_RECEPTOR"] = "NO DISPONIBLE"

                    # DATOS COMPLEMENTARIOS
                    if "Complemento" in str(rama):
                        for subrama in rama:
                            if "TimbreFiscalDigital" in str(subrama):
                                dict_datos_cfdi["UUID"] = subrama.attrib["UUID"]
                                dict_datos_cfdi["FechaTimbrado"] = subrama.attrib["FechaTimbrado"]

                            if "Nomina" in str(subrama):
                                try:
                                    dict_datos_cfdi["TotalDeducciones"] = subrama.attrib["TotalDeducciones"]
                                except KeyError:
                                    dict_datos_cfdi["TotalDeducciones"] = "NO DISPONIBLE"
                                try:
                                    dict_datos_cfdi["FechaInicialPago"] = subrama.attrib["FechaInicialPago"]
                                except KeyError:
                                    dict_datos_cfdi["TotalDeducciones"] = "NO DISPONIBLE"
                                try:
                                    dict_datos_cfdi["FechaFinalPago"] = subrama.attrib["FechaFinalPago"]
                                except KeyError:
                                    dict_datos_cfdi["TotalDeducciones"] = "NO DISPONIBLE"
                                try:
                                    dict_datos_cfdi["TotalPercepciones"] = subrama.attrib["TotalPercepciones"]
                                except KeyError:
                                    dict_datos_cfdi["TotalDeducciones"] = "NO DISPONIBLE"
                                try:
                                    dict_datos_cfdi["TotalDeducciones"] = subrama.attrib["TotalDeducciones"]
                                except KeyError:
                                    dict_datos_cfdi["TotalDeducciones"] = "NO DISPONIBLE"
                                try:
                                    dict_datos_cfdi["TotalOtrosPagos"] = subrama.attrib["TotalOtrosPagos"]
                                except KeyError:
                                    dict_datos_cfdi["TotalDeducciones"] = "NO DISPONIBLE"

                                for subsubrama in subrama:
                                    if "Emisor" in str(subsubrama):
                                        dict_datos_cfdi["RegistroPatronal"] = subsubrama.attrib["RegistroPatronal"]

                                    if "Percepciones" in str(subsubrama):
                                        for percepcion in subsubrama:
                                            listado_conceptos.append(percepcion.attrib)

                                    if "Deducciones" in str(subsubrama):
                                        for deduccion in subsubrama:
                                            listado_conceptos.append(deduccion.attrib)

                for folio, concepto_unico in enumerate(listado_conceptos):
                    dict_temporal = concepto_unico
                    dict_temporal.update(dict_datos_cfdi)
                    acumulado[sepan_cuantos] = dict_temporal
                    sepan_cuantos+= 1

    df = pd.DataFrame.from_dict(acumulado, orient="index")
    df["Importe"] = df["Importe"].astype(float)
    df["ImporteGravado"] = df["ImporteGravado"].astype(float)
    df["ImporteExento"] = df["ImporteExento"].astype(float)
    df["TotalPercepciones"] = df["TotalPercepciones"].astype(float)
    df["TotalDeducciones"] = df["TotalDeducciones"].astype(float)
    df["TotalOtrosPagos"] = df["TotalOtrosPagos"].astype(float)
    df["Importe"] = df["Importe"].astype(float)
    df = df[["Archivo", "UUID", "NOMBRE_RECEPTOR", "RFC_RECEPTOR", "NOMBRE_EMISOR", "RFC_EMISOR", "TipoDeComprobante", "FechaTimbrado", "RegistroPatronal",
             "FechaInicialPago", "FechaFinalPago", "Clave", "TipoPercepcion", "TipoDeduccion", "Concepto", "Importe", "ImporteGravado", "ImporteExento",
             "TotalPercepciones", "TotalDeducciones", "TotalOtrosPagos"]]
    df.to_excel(fr"{directorio_padre}/xml_leidos.xlsx", index=False)

    fechaHoy = datetime.today().strftime("%Y-%m-%d %H:%M")
    print("Terminado:", fechaHoy)

    print("Excel disponible en: ", fr"{directorio_padre}/xml_leidos.xlsx")