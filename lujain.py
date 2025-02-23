import pandas as pd
import xml.etree.ElementTree as ET

def update_prices(excel_file, xml_file, output_excel, output_xml):

    df = pd.read_excel(excel_file, sheet_name='Sheet1')

    conversion_factor = 1.28

    df['price($)'] = df['price(£)'] * conversion_factor


    df.to_excel(output_excel, index=False)


    tree = ET.parse(xml_file)
    root = tree.getroot()
    namespace = {'ns': 'http://www.demandware.com/xml/impex/pricebook/2006-10-31'}


    for price_table in root.findall('.//ns:price-table', namespace):
        product_id = price_table.get('product-id')

        row = df.loc[df['SKU Code'] == product_id]

        if not row.empty:
            amount = price_table.find('ns:amount', namespace)
            amount.text = str(round(row['price($)'].values[0], 2))


    tree.write(output_xml)


update_prices('taskexcel_1.xlsx', 'task.xml', 'taskexcel_2.xlsx', 'update.xml')
