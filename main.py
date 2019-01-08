from selenium import webdriver
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MAIN_URL = config['DEFAULT']['MAIN_URL']
STORE_NAME = config['DEFAULT']['STORE_NAME']
SORT_BY = config['DEFAULT']['SORT_BY']
MAX_PAGE_NUM = int(config['DEFAULT']['MAX_PAGE_NUM'])
hlink = []


#FUNCTION TO REPLACE MULTIPLE STRING
def replaceMultiple(mainString, toBeReplaces, newString):
    for elem in toBeReplaces :
        if elem in mainString :
            mainString = mainString.replace(elem, newString)
    return  mainString


driver = webdriver.Firefox()
driver.implicitly_wait(12)

with open('export.csv', 'w') as f:
    f.write("Nama Produk; Kategori; Deskripsi Produk; Harga (Dalam Rupiah); Berat (Dalam Gram); Pemesanan Minimum; Status; Jumlah Stok; Etalase; Preorder; Waktu Proses Preorder; Kondisi; Gambar 1 ; Gambar 2; Gambar 3; Gambar 4; Gambar 5; URL Video Produk 1; URL Video Produk 2; URL Video Produk 3 \n")

for i in range(1, MAX_PAGE_NUM +1):
    url = MAIN_URL + "/" + STORE_NAME + "?" + "page=" + str(i) + "&sortBy=" + SORT_BY

    driver.get(url)

    div_href = driver.find_elements_by_xpath('//div[@class="shop-search-result-view__item col-xs-2-4"]')
    for i in range(int(len(div_href))):
        hlink_list = div_href[i].find_element_by_css_selector('a').get_attribute('href')
        hlink.append(hlink_list)
        

for i in range(int(len(hlink))):
    driver.get(hlink[i])

    prod_img = []

    #PRODUCT NAME
    prod_name_el = driver.find_element_by_xpath('//div[@class="qaNIZv"]')
    prod_name = prod_name_el.text.replace('Star Seller', '')

    #PRODUCT DESCRIPTION
    prod_desc_el = driver.find_element_by_xpath('//div[@class="_2u0jt9"]')
    prod_desc = replaceMultiple(prod_desc_el.text, [';', '\n'], ' ')
    
    #PRODUCT PRICE
    prod_price_el = driver.find_element_by_xpath('//div[@class="_3n5NQx"]')
    prod_price = replaceMultiple(prod_price_el.text,['Rp', '.'], '')
    
    #PRODUCT STOCK
    prod_stock_el = driver.find_element_by_xpath('//div[contains(text(), "tersisa")]')
    prod_stock = replaceMultiple(prod_stock_el.text, ['tersisa', 'buah'], '')
    
    #PRODUCT IMAGE
    div_img = driver.find_elements_by_xpath('//div[@class="_2Fw7Qu animated-lazy-image__image--ready"]')
    for i in range(int(len(div_img))):
        prod_img_list = div_img[i].get_attribute('style')
        prod_img.append(prod_img_list[23:84])
    
    prod_pict = ";".join(prod_img)
    
    with open('export.csv', 'a') as f:
        f.write(prod_name + ";" + "CATEGORY" + ";" + prod_desc + ";" + prod_price + ";" + "WEIGHT" + ";" + "MIN_ORDER" + ";" + "Stock Tersedia" + ";" + prod_stock + ";" + "ETALASE" + ";" + "PREORDER" + ";" + "WAKTU_PROSES_PREORDER" + ";" + "CONDITION" + ";" + prod_pict + "\n")

driver.close()