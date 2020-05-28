from selenium import webdriver
import os
import time
import json
    '''
    #save login cookie
    dictCookies = driver.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    with open('D:\\www\\SeleniumPython\\cookie_target.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')

    #open URL using saved cookie
    with open('D:\\www\\SeleniumPython\\cookie_target.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    for cookie in listCookies:
        cookie_dict = {
                    'domain': cookie.get('domain'),
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": '',
                    'path': '/',
                    'httpOnly': cookie.get('httpOnly'),
                    #'sameSite':cookie.get('sameSite'),
                    'Secure': cookie.get('Secure')
                }
        driver.add_cookie(cookie_dict)

    driver.refresh()  
    time.sleep(20)

    '''