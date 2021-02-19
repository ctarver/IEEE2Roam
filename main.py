from selenium import webdriver
import pyperclip
import re
driver = webdriver.Firefox(executable_path=r'C:\Users\tarve\Desktop\geckodriver-v0.29.0-win64\geckodriver.exe')
driver.get('https://ieeexplore.ieee.org/document/9345121')

authors = driver.find_elements_by_class_name("authors-info")
all_authors_str = ""
for author in authors:
    this_author_text = author.text
    if this_author_text is not '':
        all_authors_str = all_authors_str + '[[' + this_author_text[:-1] + ']], '
all_authors_str = all_authors_str[:-2]
pyperclip.copy(all_authors_str)

# Need to pause here so that we can change the mathjax to not render.
# Find a mathjax and right click on it..
mathjax = driver.find_elements_by_class_name('display-formula')



article = driver.find_element_by_id('article')
article_text = article.text
article_text = article_text.replace("View Source", "")
article_text = article_text.replace("View All", "")
# Make equations use $$
article_text = article_text.replace("\\begin{align*}", "$$")
article_text = article_text.replace("\\end{align*}", "$$")
article_text = article_text.replace("\\begin{equation*}", "$$")
article_text = article_text.replace("\\end{equation*}", "$$")
article_text = article_text.replace("\\begin{align}", "$$")
article_text = article_text.replace("\\end{align}", "$$")
article_text = article_text.replace("\\begin{equation}", "$$")
article_text = article_text.replace("\\end{equation}", "$$")
article_text = article_text.replace("\\tag{*}", "")
# I don't know how to do regex good. Just do it twice
article_text = re.sub('.tag{.}', '', article_text).strip()
article_text = re.sub('.tag{..}', '', article_text).strip()

# Get the references...
# Open the reference header references-header

references = driver.find_elements_by_class_name('reference-container')
# Need to add all strings
all_refs = ''
for reference in references:
    this_text = reference.text
    if this_text is not '':
        all_refs = all_refs + this_text

