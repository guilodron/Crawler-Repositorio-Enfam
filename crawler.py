from bs4 import BeautifulSoup
import urllib.parse
import requests
import os
import json

# Creates pdf destination folder
if not os.path.exists('pdfs'):
    os.makedirs('pdfs')

# Gets main page soup and extracts all links
main_page = requests.get('https://www.enfam.jus.br/portal-covid19/repositorio/')
soup = BeautifulSoup(main_page.text, 'html.parser')
classe = soup.find(class_="entry-content")
main_page_links = classe.findAll('a')

# Removes categories with unusable links
del main_page_links[-6:]

# Loads json file if exists to store file info
file_info = []
if not os.path.exists('data.json'):
  open('data.json', 'w', encoding='utf8').close()
else: 
  with open('data.json', 'r+', encoding='utf8') as file_data:
    file_info = json.load(file_data)

# Iterates on links on the main page
for category_link in main_page_links:
  url = category_link.get('href')
  try:
    links_request = requests.get(url)
    soup = BeautifulSoup(links_request.text, 'html.parser')
    classe = soup.find(class_="entry-content")
    links = classe.findAll('a')
    # print('--------------------------------------')
    # print(category_link.text)
    # print('--------------------------------------')
  except: 
    open('log.txt', 'a+').write('erro na url: ' + url + '\n')
    #print('erro na url: ' + url)
  # Iterates on each every link to find pdf
  for link in links:
    url = link.get('href')
    filename = url.split("/")[-1]
    parsed_filename = urllib.parse.unquote(filename)
    parsed_filename = parsed_filename.replace('?', '')
    # print(url)
    # print('--------------------------------------')
    try:
      if not os.path.exists('./pdfs/' + parsed_filename):
          pdf = requests.get(url, verify=True, timeout=4)
          #print(pdf)
          if pdf.headers.get('Content-Type') == 'application/pdf':
              open('./pdfs/' + parsed_filename, 'wb').write(pdf.content)
              file_info.append({
                "filename" : parsed_filename,
                "path": "./pdfs/" + parsed_filename,
                "category": urllib.parse.unquote(category_link.text)
              })
              # print('baixou url: ' + url + '\n')
    except:
      open('log.txt', 'a+').write('erro na url: ' + url + '\n')
      # print('erro na url: ' + url)

# Saves file content back on json file
with open('data.json', 'w+', encoding='utf8') as f:
        json.dump(file_info, f, ensure_ascii=False)