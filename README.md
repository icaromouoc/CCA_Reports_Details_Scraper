# CCA_Reports_Details_Scraper
## Español

Extrae los informes de fiscalización publicados y definitivos de la página web de (https://www.ccuentas.es/) de la Cámara de Cuentas de Andalucía.

Para ejecutar el script es necesario instalar la siguientes bibliotecas:
```
pip install pandas
pip install requests
pip install lxml
pip install beautifulsoup4
pip install time
pip install openpyxl
```

El script se debe ejecutar de la siguiente manera:
```
python CCA_Reports_Details_Scraper.py
```

Actualmente extrae los siguientes detalles de los informes de fiscalización:
- Departamento de fiscalización.
- Código de la fiscalización.
- Título de la fiscalización.
- Número y fecha de publicación en BOJA.
- Tiempo necesario para realizar la auditoría, aproximadamente.
- URL de acceso al informe completo.
- URL de acceso al informe resumido.
- URL de acceso al BOJA donde está publicado el informe de fiscalización.
- Año cuando empezó la auditoría.
 
Todos los datos son almacenados en:
- Un fichero CSV por departamento.
- Un fichero CSV con todos los informes.
- Un fichero Excel con todos los informes.

## English

Extract the published and final audit reports from the website of Andalusian Official Audit Office (https://www.ccuentas.es/) 

To run is necessary install the following libraries:
```
pip install pandas
pip install requests
pip install lxml
pip install beautifulsoup4
pip install time
pip install openpyxl
```

To run the script:
```
python CCA_Reports_Details_Scraper.py
```

It currently extracts the following details from the audit reports:
- Audit department.
- Audit code.
- Title of the report.
- Number and date of publication in BOJA.
- Time necessary to carry out the audit, approximately.
- URL to access the full report.
- URL to access the summary report.
- Access URL to the BOJA where the audit report is published.
- Year when the audit started.

All data is stored in:
- One CSV file per department.
- A CSV file with all the reports.
- An Excel file with all the reports.
