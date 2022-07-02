import sys
import requests
import time
import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque



class Tree:
    #инициализация класса работы с иерархиями
    def __init__(self, parent, url, degree):
        #установить указатель на предка
        self.parent = parent
        #установить значение текущего узла
        self.url = url
        #установить степень узла
        self.degree = degree

    def setSubURLs(self):
        
                if self.degree == max_degree:
            return
                  urls = getSubURLs(self.url)
        #проверка условия нахождения  целевой ссылки среди найденых на странице составляем ответ 
        if target_url in urls:
            #инициализируем работу со списком 
            answer = []
            #добавляем целевую ссылку в список
            answer.append(target_url)
            #взять текущую вершину и положить в node
            node = self
                while not node.parent is None:
                answer.append(node.url)
                node = node.parent
                answer.append(node.url)
            #по всему перевернутому([::-1]) списку без последнего элемента ([:-1])
            for i in answer[::-1][:-1]:
                #вывод ответа без последней ссылки, sys.stdout.write а не print, потому что print переносит строку
                sys.stdout.write(i + " => ")
            #вывод последней ссылки
            sys.stdout.write(answer[0] + '\n')    
            exit(0)
        for url in urls:
            #создать вершину из ссылки, родителем будет текущая вершина, а степень равна степени текущей вершины + 1
            node = Tree(self, url, self.degree + 1)
            #добавить созданную вершину в очередь
            queue.append(node)

#проверка ссылки на корректность
def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#получение set() ссылок со страницы
def getSubURLs(url):
    urls = set()
    #скачивает контент со ссылки и парсит
    soup = BeautifulSoup(requests.get(url).content, "html.parser")


    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not valid_url(href):
            continue
        #если мы уже такую ссылку уже находили, то мы с ней ничего не делаем
        if href in int_url:
            continue
        #проверяем совпадает доменное имя и доменное имя ссылки
        if domain_name not in href:
            continue
        #добавить ссылку в набор
        urls.add(href)
        int_url.add(href)
    return urls

#проверяем параметры 
if len(sys.argv) != 4:
    print("ошибка установки параметра")
    exit(1)

#проверяем что  это ссылки
if not valid_url(sys.argv[1]):
    print("неверный начальный URL-адрес: " + sys.argv[1])
    exit(2)
if not valid_url(sys.argv[2]):
    print("недопустимый  URL-адрес: " + sys.argv[2])
    exit(2)

#проверяем условия если 2 и 3 ссылки одинаковые вернуть ответь
if sys.argv[1] == sys.argv[2]:
    print(sys.argv[1])
    exit(0)

#задаем макс глубина дерева
max_degree = 5
#проверяем ддоменное имя первой ссылки сссылки
domain_name = urlparse(sys.argv[1]).netloc
#проверяем что доменное имя первой и второй ссылки совпадает
if urlparse(sys.argv[2]).netloc != domain_name:
    print("начальный и целевой URL-адреса имеют разные доменные имена")
    exit(3)

#вычисляем и проверяем rate_limit установленного времени
rate_limit = int(sys.argv[3])
if rate_limit < 1:
        print("Органичение скорости")
        exit(4)
except ValueError:
         print("Ошибка лимита времени")
         exit(4)

#набор ссылок которые мы уже посетили или планируем посетить 
int_url = set()
target_url = sys.argv[2]
tree = Tree(None, sys.argv[1], 0)
queue = deque()
queue.append(tree)
#пока очередь не пустая выполняем следюущее
while queue:
    node = queue.popleft()
    node.setSubURLs()
    time.sleep(60/rate_limit)

#теперь обрабатываем похожим образом но меняем изначальные и target ссылки местами
int_url = set()
target_url = sys.argv[1]
tree = Tree(None, sys.argv[2], 0)
queue = deque()
queue.append(tree)
while queue:
    node = queue.popleft()
    node.setSubURLs()
    time.sleep(60/rate_limit)

print("достигнут конечный элемент списка ссылок")
