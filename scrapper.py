import time
from selenium import webdriver
import urllib.request
import os
import json

def retrieve_links(search_string):
    links = []
    driver = webdriver.Chrome('chromedriver')
    driver.get('https://www.myntra.com/')
    time.sleep(5)
    driver.find_element_by_class_name('desktop-searchBar').send_keys(search_string)
    driver.find_element_by_class_name('desktop-submit').click()
    while(True):
        time.sleep(5)
        for product_base in driver.find_elements_by_class_name('product-base'):
            links.append(product_base.find_element_by_xpath('./a').get_attribute("href"))
        try:
            driver.find_element_by_class_name('pagination-next').click()
        except:
            driver.close()
            driver.quit()
            return links
def get_product_meta_data(link,base):
    driver = webdriver.Chrome('chromedriver') 
    driver.get(link)
    metadata = dict()
    metadata['link'] = link
    while True:
        try:
            metadata['title'] = driver.find_element_by_class_name('pdp-title').get_attribute("innerHTML")
            break
        except:
            pass
    metadata['name'] = driver.find_element_by_class_name('pdp-name').get_attribute("innerHTML")
    metadata['price'] = driver.find_element_by_class_name('pdp-price').find_element_by_xpath('./strong').get_attribute("innerHTML")
    metadata['specifications'] = dict()
    try:
        driver.find_element_by_class_name('index-showMoreText').click()
    except:
        pass
    for index_row in driver.find_element_by_class_name('index-tableContainer').find_elements_by_class_name('index-row'):
        metadata['specifications'][index_row.find_element_by_class_name('index-rowKey').get_attribute("innerHTML")] = index_row.find_element_by_class_name('index-rowValue').get_attribute("innerHTML")
    metadata['productId'] = driver.find_element_by_class_name('supplier-styleId').get_attribute("innerHTML")
    try:
        os.mkdir("data")
    except:
        pass
    try:
        os.mkdir(os.path.join("data",base))
    except:
        pass
    try:
        os.mkdir(os.path.join("data",base,metadata['productId']))
        os.mkdir(os.path.join("data",base,metadata['productId'],'images'))
    except:
        driver.close()
        driver.quit()
    itr = 1
    for image_tags in driver.find_elements_by_class_name('image-grid-image'):
        image_path = os.path.join("data",base,metadata['productId'],'images',str(itr)+".jpg")
        urllib.request.urlretrieve(image_tags.get_attribute('style').split("url(\"")[1].split("\")")[0],image_path)
        itr +=1
    with open(os.path.join("data",base,metadata['productId'],'metadata.json'), 'w') as fp:
        json.dump(metadata, fp)
    driver.close()
    driver.quit()

if __name__ == "__main__":
    file_ = open("clothings.txt","r")
    search_strings = file_.readlines()
    file_.close()
    for string in search_strings:
        search_string = string.split("\n")[0]
        links = list(set(retrieve_links(search_string)))
        for link in links:
            get_product_meta_data(link,search_string)
        print(len(links),":Number of objects of ",search_string," category added")