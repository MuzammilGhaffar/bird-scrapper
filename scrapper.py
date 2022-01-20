import requests
from tkinter import *
from bs4 import BeautifulSoup
from googlesearch import search
import re
import html

def get_text(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser').extract()
    text = ''
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    for para in soup.select('p'):
        raw_text = re.sub(CLEANR, '', html.unescape(para.getText()))
        if(len(raw_text) >= 200):
            text += raw_text + ' '
    text = text.replace(".", " ")
    return " ".join(re.sub("[^A-Za-z0-9]+", "", text).split())

def save_to_file(content, filename):
    filename = filename.replace(' ', '-').lower() + '.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def search_func(input):
    query = input.get()
    if(not len(query)):
        return
    visited_url = []
    content = ''
    for j in search(query, num=15, stop=15):
        main_url = j.split('/')[2].strip()
        if main_url in visited_url:
            continue
        content += main_url + '\n'
        content += get_text(j)
        content += '\n\n'
        visited_url.append(main_url)
    save_to_file(content, query)
    input.delete(0, END)




window = Tk()
window.resizable(0, 0)
window.geometry("380x150")
window.title("Scrape Birds Data!")

input = Entry(window, width=30)
button = Button(window, text="Generate info", padx = 15, pady =3, command = lambda: search_func(input))

input.place(anchor = CENTER, relx = .5, rely = .3)
button.place(anchor = CENTER, relx = .5, rely = .6)

window.mainloop()