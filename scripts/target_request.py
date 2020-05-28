import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import RequestException
import csv



def download(url, headers, num_retries=3):
    page = requests.get(url,headers=headers)
    #print(page.status_code)

    if page.status_code == 200:
        content_list = []
        content = page.content
        result = BeautifulSoup(content, 'lxml')
        total_page_num = result.find('div',attrs={'class':'RefineMenu-pageInfo'}).find('span',attrs={'class':'total-page-number'}).text
        #print(total_page_num)
        try:

            #generate URLs for multi-pages
            for i in range(0,int(total_page_num)):
                url_split = re.findall("(.*page=)", url)
                new_url = url_split[0]
                new_url = new_url + str(i)
                print("new url:", new_url)
                new_page = requests.get(url,headers=headers)
                if new_page.status_code == 200:
                    #print(type(new_page.content))
                    #download page contents page by page
                    content_list.append(new_page.content)
                    # return new_page.content
                else:
                    print("new url status code:", new_page.status_code)
                    return None
            #print(len(content_list))
            return content_list
        except RequestException as e:
            print(e.response)

        #verify if the response of request's exception contains status_code
        if hasattr(e.response,'status_code'):
            code = e.response.status_code
            print("error code: %s" % code)

        #try 3 times and return the results if success
        html = ""
        if num_retries > 0 and 500 <= code < 600:
            html = download(url, headers, num_retries-1)
        else:
            code = None
            return html


    else:
        print(page.status_code)
        return None

#new file and add title
def add_file_title(filepath, title):
    with open (filepath, 'w', newline = '', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        write.writerow(title)
    f.close()
#crawler all the products details and save to csv file
def find_products(url, filepath, headers):
    r = download(url,headers)
    count = 0
    #print("length r is ", len(r))
    with open (filepath, 'a+', newline = '', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        #crawler the products details page by page
        #get each product code, name and price
        for i in range(0, int(len(r))):
            page = BeautifulSoup(r[i], 'lxml')
            all_items = page.find_all('li',attrs={'class':'product ga-ec-impression'})
            #print(len(all_items)) 
            for data in all_items:
                count += 1
                row = []
                product_code = data.get('data-product-code')
                #print(product_code)
                product_name = data.find('div',attrs={'class':'detail'}).find('a').text
                #print(product_name)
                product_price = data.find('div',attrs={'class':'price-info'}).find('span',attrs={'class':'price-regular'}).text
                product_price = re.sub(r'[\n\s\r]+', '', product_price)
                #print(product_price)
                row.append(product_code)
                row.append(product_name)
                row.append(product_price)
                write.writerow(row)
        print("totol %d computers saved" % count)
    f.close()
     

def main():
    headers = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"   
    }

    url = "https://www.target.com.au/c/men/accessories/W133029?N=27op&Nrpp=30&viewAs=grid&category=W133029&page=0"
    filepath = "D:\\www\\SeleniumWWS\\Data\\target_product.csv"
    #title = ('product_code', 'product_name', 'product_price')
    #add_file_title(filepath, title)
    find_products(url, filepath, headers=headers)

if __name__ == "__main__":
    main()

