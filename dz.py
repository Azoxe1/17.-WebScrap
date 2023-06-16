import requests
import fake_headers
import bs4

headers = fake_headers.Headers(browser="YandexBrowser", os="win")
headers_dict = headers.generate()

response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_dict)
html = response.text

soup = bs4.BeautifulSoup(html, "lxml")
div = soup.find('main', class_='vacancy-serp-content')
articles = div.find_all(class_='serp-item')

def find_info(a):
    info = []
    counter = 0
    for lists in a:
        name = lists.find('a', class_ = 'serp-item__title')
        name_text = name.text
        
        if " " in name_text:                                                            #Оставил пустым, ибо если делать как в ДЗ - результатов нет  =)
            z = lists.find('span', class_ = "bloko-header-section-3")
            if z is None:
                continue
            else:
                if "USD" in str(z.text):
                    salary = z.text                                             #Тут возникает баг с выводом корректного формата. Некоторые говорят Селениум решает эту беду. Так ли?
                else:
                    continue
            url = lists.find('a', class_ = 'serp-item__title')
            link = f"{url['href']}"
            
            g = lists.find('a', class_ = "bloko-link bloko-link_kind-tertiary")
            company = g.text
            
            # u = lists.find('div', dataqa= "vacancy-serp__vacancy-address")             - dataqa Неизвестно как записать данную переменную, дабы код работал и искал город
            # city = u.text
            
            counter +=1
            info.append({
                "Number" : counter,
                "URL": link,
                "Salary" : salary,
                "Company_name": company,
                # "City": city
                })
            continue
        else:
            continue
    return info
if __name__ == "__main__":
    print(find_info(articles))
    
