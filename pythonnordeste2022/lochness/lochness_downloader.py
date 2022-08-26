
import  requests
import  re
from bs4 import BeautifulSoup
import pandas as pd


def extract_data(content_page):
    soup = BeautifulSoup(content_page, 'html.parser')
    row_to_write = []
    for row in soup.find_all('div', {'class': 'results-table--row'})[1:]:
        position =  row.find('div', {'data-col-title': 'Position'}).text
        bib_number =  row.find('div', {'data-col-title': 'Race No'}).text
        first_name =  row.find('div', {'data-col-title': 'First Name'}).text
        last_name =  row.find('div', {'data-col-title': 'Last Name'}).text
        half_time =  row.find('div', {'data-col-title': 'Half Time'}).text
        gun_time =  row.find('div', {'data-col-title': 'Gun Time'}).text
        chip_time =  row.find('div', {'data-col-title': 'Chip Time'}).text
        club =  row.find('div', {'data-col-title': 'Club'}).text
        category =  row.find('div', {'data-col-title': 'Category'}).text

        row_to_write.append({'position': position.strip(), 'bib': bib_number.strip(), 'firstname': first_name.strip(),
                             'lastname': last_name.strip(), 'halftime': half_time.strip(),
                             'guntime': gun_time.strip(), 'chiptime': chip_time.strip(),
                                'category':   category.strip()})

    return row_to_write


if __name__ == '__main__':
    content_main_page = requests.get('https://lochnessmarathon.com/results/').text
    soup = BeautifulSoup(content_main_page, 'html.parser')
    results = soup.findAll('a', href=True, text=re.compile('Loch Ness Marathon'))
    for result in results:
        if 'results' in str(result['href']):
            all_results = []
            year = (re.search(r'\d+', str(result.text)).group(0))
            url = (result['href'])
            page = 1
            content_marathon = requests.get('https://lochnessmarathon.com/results/1/%s/?epage=%d' % (year, page)).text
            page_results = extract_data(content_marathon)
            while(page_results):
                all_results.extend(page_results)
                page +=1
                content_marathon = requests.get('https://lochnessmarathon.com/results/1/%s/?epage=%d' % (year,page)).text
                page_results = extract_data(content_marathon)
            print('total_results' , len(all_results))
            dataframe = pd.DataFrame.from_dict(all_results)
            dataframe.to_csv('lochness_marathon_%s.csv' % year, index=False)
