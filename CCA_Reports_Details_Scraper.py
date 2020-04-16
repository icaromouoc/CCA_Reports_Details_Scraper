## Inés Caro Molina y Ángel Carrasco Núñez
# Basado en Python 3.9
from bs4 import BeautifulSoup
import requests
import urllib3
import pandas as pd
import re
import sys
import time

## Cambio de comportamientos para la aplicación
# Desactiva los warning provenientes del certificado de la web
urllib3.disable_warnings()
# Cambio el agente para que pueda discriminarse en las estadisticas de tráfico de la web
user_agent = {"User-Agent": "Practica-Web-Scraping"}

## Debido al uso de redirectores de la web, localizo el delimitador final
def LookForDelimeter(url):
    # Extraigo el contenido
    page_processing = requests.get(url, headers=user_agent, verify=False).text 

    # Localizo la paginacion
    soup = BeautifulSoup(page_processing, "html.parser")
    pagination = soup.find(id="pagination")

    # Busco el LookForDelimeter final
    delimeter_last = pagination.find_all('a')
    last_page = str(delimeter_last[-1:])
    end_page=last_page.split('>')[1].split('<')[0]

    return (end_page)

## Elimino los "espacios" dentro de los datos
def DataCuration(BD_data):
    cured_data = str(BD_data[0]).strip()
    return cured_data
            
## Extraigo la información de la web seleccionada
def WebProcessing(url):
    # Extraigo el contenido
    page_processing = requests.get(url, headers=user_agent, verify=False).text 
    soup = BeautifulSoup(page_processing, "html.parser")

    # Obtengo el nombre del departamento
    department_name = soup.h1.text.strip()
    
    # Preparo las listas
    department_name_list = []
    code_name_list = []
    title_name_list = []
    boja_published_list = []
    complete_report_list = []
    resume_report_list = []
    boja_link_list = []
    time_auditing_list = []
    year_of_audit_list = []
    
    # Recorro la web    
    table = soup.find('table')
    table_rows = table.find_all('tr')
    for tr in table_rows:
            # Extraigo el contenido de la fila
            td = tr.find_all('td')

            # Nombre de la actuación (nombre de la auditoría)
            code_name = DataCuration(td[1].contents)

            # Año de la actuación
            code_year_pattern = re.compile(r'\d{1,4}$')
            code_year = code_year_pattern.findall(code_name)
            
            
            # Obtengo los enlaces a los informes
            a_item = []
            for a_items in tr.find_all("a"):
                a_item.append(a_items.attrs["href"])

            # Doto de valores por defecto a los informes
            complete_report = "No está accesible el informe completo"
            resume_report = "No está accesible el informe ejecutivo"
            boja_link = "No aparece el enlace de BOJA"
            boja_published = "No aparece el nro. de BOJA"
            boja_year = ""

            ## Compruebo si ha habido publicación de BOJA
            boja_extraction = str(td[2].text).lower()
                    
            ## Extraigo el patron
            # El formato normal es nº, fecha
            boja_normal_pattern = re.compile(r'\d{1,3},?\s{0,1}\d{1,2}[-,\/]\d{1,2}[-,\/]\d{1,4}')
            # El formato abreviado es nº/fecha
            boja_weird_pattern = re.compile(r'\d{1,3}\/\d{1,4}')

                
            ## Compruebo el formato que han elegido para indicar el BOJA
            if (boja_normal_pattern.findall(boja_extraction)):
                # nº, fecha
                # Normalizo la separacion de dias, meses y años
                boja_normal_pattern = boja_normal_pattern.findall(boja_extraction)[0].replace('-','/')
                # Normalizo la separación del número de BOJA y la fecha
                boja_separator = re.compile(r'\d{1,3} ')
                if boja_separator.findall(boja_normal_pattern):
                    boja_published = "Nro. " + boja_normal_pattern.replace(' ',', ')
                else:
                    boja_published = "Nro. " + boja_normal_pattern
            else:
                # nº/año
                if (boja_weird_pattern.findall(boja_extraction)):
                    boja_published = "Nro. " + boja_weird_pattern.findall(boja_extraction)[0]

            # Normalizo la fecha de dos dígitos a cuatro dígitos
            boja_year_pattern = re.compile(r'\d{1,2}$')
            if boja_year_pattern.findall(boja_published):
                boja_year = boja_year_pattern.findall(boja_published)
                if int(boja_year[0]) >= 0 and int(boja_year[0]) <= 80:
                    boja_year = "20" + boja_year[0]
                else:
                    boja_year = "19" + boja_year[0]
                boja_published = re.sub("/\d{1,2}$", "/" + boja_year, boja_published)
                    

            # Doto de los valores correctos a los informes
            for i in range(0, len(a_item)):
                report_tmp = a_item[i].lower()
                if report_tmp.find("complete") != -1:
                    complete_report = a_item[i]
                if report_tmp.find("resume") != -1:
                    resume_report = a_item[i]
                if report_tmp.find("boja") != -1:
                    boja_link = a_item[i]


            ## Corrijo un fallo del gestor de contenidos
            # Si tengo número de BOJA pero no tengo el acceso a la url...
            if boja_link == "No aparece el enlace de BOJA" and boja_published != "No aparece el nro. de BOJA":
                boja_link = "Debe consultarse directamente en BOJA"
            
            # Nombre de la titulo de actuacion
            title_name = DataCuration(td[2].contents)

            # Elimino si hay información de BOJA en el titulo
            boja_info_pattern = re.compile(r'\(BOJA n.m. \d{1,3},?\s{0,1}\d{1,2}[-,/]\d{1,2}[-,/]\d{1,4}\)')
            if (boja_info_pattern.findall(title_name)):
                title_name = re.sub("\(BOJA n.m. \d{1,3},?\s{0,1}\d{1,2}[-,/]\d{1,2}[-,/]\d{1,4}\)", "", title_name)


            # Calculo el tiempo de duracion de la auditoria aproximadamente
            time_auditing_pattern = re.compile(r'\d{4}$')
            boja_year = time_auditing_pattern.findall(boja_published)
            if time_auditing_pattern.findall(boja_published):
                time_auditing_int = int(boja_year[0]) - int(code_year[0]) + 1
                time_auditing = "Cerca de " + str(time_auditing_int) + " año(s)"
            else: 
                time_auditing = "No se puede indicar"
            
                
            # Añado los campos a su lista correspondiente
            department_name_list.append(department_name)
            code_name_list.append(code_name)
            title_name_list.append(title_name)
            boja_published_list.append(boja_published)
            complete_report_list.append(complete_report)
            resume_report_list.append(resume_report)
            boja_link_list.append(boja_link)
            time_auditing_list.append(time_auditing)
            year_of_audit_list.append(int(code_year[0]))

    # Genero un DataFrame con los elementos de la web       
    rows_current = pd.DataFrame({ 'Department' : department_name_list, 'Code' : code_name_list, 'Title' : title_name_list, 'BOJA_Published' : boja_published_list, 'Time Auditing' : time_auditing_list, 'Complete' : complete_report_list, 'Resume' : resume_report_list, 'BOJA_Link' : boja_link_list, 'Year_of_Audit' : year_of_audit_list })
        
    return (rows_current)

## Genero una barra de progreso
def ProgressBar(i,max,postText):
    n_bar = 10
    j = i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()


## Genero el listado de todas las paginas que contengan informes de cada departamento
def Iterator(url, number):
    loop_number = int(number)
    urls = []

    # Genero las urls
    for url_number in list(range(loop_number)):
        urls.append(url + str(url_number+1))
            
    return (urls)

## Genero el CSV por cada departamento
def GeneratingCSVbyDepartment(url, department):
    # Obtengo la delimitacion
    web_delimeter = LookForDelimeter(url)
    # Obtengo las URL fuentes
    url_sources = Iterator(url, web_delimeter)
    # Genero el dataset
    data_web = pd.DataFrame()
    for i in range(0, len(url_sources)):
        data_web = data_web.append(WebProcessing(url_sources[i]), ignore_index = True)
        ProgressBar(i, len(url_sources)-1, "Extrayendo información del departamento de " + department)
        time.sleep(0.05) 
    # Ordeno el DataFrame por año de comienzo de la auditoría
    data_web.sort_values(by=['Year_of_Audit'], ascending=False, inplace=True)
    data_web.reset_index()
    # Grabo los datos del DataSet en CSV
    filename = 'CCA_' + department.replace(' ', '_') + '_Reports_Details_Dataset.csv'
    data_web.to_csv(filename, index_label="Index", encoding='cp1252')
    print ("\r" + (" " * 132) + "\rGenerado el DataSet en CSV del departamento de " + department)

    return (data_web)

# Creo el DF para el DataSet para todos los departamentos
data_web_global = pd.DataFrame()
data_web_jda = pd.DataFrame()
data_web_ccll = pd.DataFrame()
data_web_ooee = pd.DataFrame()
data_web_co = pd.DataFrame()

## Genero el DataSet en formato CSV de cada departamento
data_web_jda = GeneratingCSVbyDepartment('https://www.ccuentas.es/junta-de-andalucia/', 'Junta de Andalucía')
data_web_ccll = GeneratingCSVbyDepartment('https://www.ccuentas.es/corporaciones-locales/', 'Corporaciones Locales')
data_web_ooee =  GeneratingCSVbyDepartment('https://www.ccuentas.es/organismos-y-empresas-publicas/', 'Organismos y Empresas Publicas')
data_web_co = GeneratingCSVbyDepartment('https://www.ccuentas.es/coordinacion/', 'Coordinación')

## Genero el DataSet en formato CSV global
data_web_global = data_web_global.append(data_web_jda, ignore_index=False, verify_integrity=False, sort=None)
data_web_global = data_web_global.append(data_web_ccll, ignore_index=False, verify_integrity=False, sort=None)
data_web_global = data_web_global.append(data_web_ooee, ignore_index=False, verify_integrity=False, sort=None)
data_web_global = data_web_global.append(data_web_co, ignore_index=False, verify_integrity=False, sort=None)

# Ordeno el DataFrame por año de comienzo de la auditoría
data_web_global.sort_values(by=['Year_of_Audit'], ascending=False, inplace=True)
data_web_global.reset_index()

## Genero el DataSet en formato CSV para todos los departamentos
data_web_global.to_csv('CCA_All_Departments_Reports_Details_Dataset.csv', index_label="Index", encoding='cp1252')
print ("Generado el DataSet en CSV de todos los informes")

## Genero una Excel con una hoja por departamento
with pd.ExcelWriter('CCA_All_Departments_Reports_Details_Dataset.xlsx') as writer:  
    data_web_jda.to_excel(writer, sheet_name='Junta de Andalucia')
    data_web_ccll.to_excel(writer, sheet_name='Corporaciones Locales')
    data_web_ooee.to_excel(writer, sheet_name='Organismos y  Empresas')
    data_web_co.to_excel(writer, sheet_name='Coordinación')
    data_web_global.to_excel(writer, sheet_name='Todos')
print ("\rGenerado el DataSet en Excel de todos los informes")
