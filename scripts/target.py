#######get all the products of men accessories from Target.com
#coding=utf-8
from selenium import webdriver
import os
import time
import json
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import xlrd
import xlwt
from xlutils.copy import copy
driver = webdriver.Chrome()
action = ActionChains(driver)


def wait_element(by_,element_):
    element = WebDriverWait(driver,timeout=10).until(
        ec.presence_of_element_located(
            (by_,element_)
        )
    )
    return element

def wait_elements(by_,element_):
    element = WebDriverWait(driver,timeout=10).until(
        ec.presence_of_all_elements_located(
            (by_,element_)
        )
    )
    return element

def write_excel_xls(path, sheet_name, value):
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    sheet.write(0,0,'Product')
    sheet.write(0,1,'Price')
    sheet.col(0).width = 20000
    for i in range(0,len(value)):
        sheet.write(1,i,value[i])
    workbook.save(path)  # 保存工作簿

def write_excel_xls_append(path, sheet_name, value):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    if rows_old == 0:
        write_excel_xls(path, sheet_name, value)
    else:
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        new_worksheet.col(0).width = 20000
        for i in range(0,len(value)):
            new_worksheet.write(rows_old,i, value[i])
        new_workbook.save(path)  # 保存工作簿

def main():
    #driver.maximize_window()
    driver.get('https://www.target.com.au/')
    time.sleep(3)
    file1 = 'D:\\www\\SeleniumWWS\\product.xls'

    #find category Men and keep mouse hovering
    #List_Men = driver.find_element_by_css_selector('li.MenuItem.MenuItem--2> a > span')
    List_Men = wait_element(By.CSS_SELECTOR,'li.MenuItem.MenuItem--2> a > span')
    action.move_to_element(List_Men).perform()
    time.sleep(2)
    #click WebPage men/accessories
    men_accessories = wait_element(By.CSS_SELECTOR,'a[href="/c/men/accessories/W133029"]')
    men_accessories.click()
    time.sleep(2)
    #get products of accessories
    count = 0
    items = []
    data = []
    page_num = 0
    is_loop = True

    if ec.title_contains('Mens Accessories'):
        total_page = wait_element(By.CSS_SELECTOR,'div.prod-refine.prod-refine-top span.total-page-number').text
        #print(total_page)
        current_page = wait_element(By.CSS_SELECTOR,'div.prod-refine.prod-refine-top span.current-page-number').text
        #print(current_page)
        
        page_num = int(current_page)
        while is_loop:
            is_loop = False
            #print('total_page_number is: %s, curent_page_number is: %d ' % (total_page,page_num))
            product_list = wait_elements(By.CSS_SELECTOR,'div.product-listing>ul>li>div.detail')
            for i in product_list:
                #print('this is %d item' % (count+1))
                product = i.find_element_by_css_selector('div.summary>h3>a').text
                #price = i.find_element_by_css_selector('div.price-info>span>span').text
                price = i.find_element_by_css_selector('div.price-info>span').text
                lists = [product,price]
                #print(lists)
                items.append(lists)
                count += 1
            time.sleep(3)
            if page_num < int(total_page):
                
                is_loop = True
            else:
                is_loop = False
                continue
            #print(is_loop)
            next_page = wait_element(By.CSS_SELECTOR,'div.prod-refine.prod-refine-top>div>div>a.RefineMenu-arrow.refine-arrow.next')
            #next_page = driver.find_element_by_css_selector('div.prod-refine.prod-refine-top>div>div>a.RefineMenu-arrow.refine-arrow.next')
            next_page.click()
            time.sleep(3)
            page_num += 1
        
        print(count,items)
    else:
        print('page failed to open')    
    time.sleep(5)
    driver.close()     
            
    for i in range(0,len(items)):
        data = items[i]
        #print(data)
        write_excel_xls_append(file1,'MenAccessories', data)
        time.sleep(1)
    time.sleep(2)
  

if __name__ == "__main__":
    main()
