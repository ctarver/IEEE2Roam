import re

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
import click
import time

#@click.command()
#@click.argument('papernumber')
def run_all(papernumber):
	driver = webdriver.Firefox(executable_path=r'C:\Users\c.tarver\Documents\geckodriver.exe')
	url =  'https://ieeexplore.ieee.org/document/' + papernumber
	driver.get(url)

	authors = driver.find_elements(By.CLASS_NAME, "authors-info")
	all_authors_str = ""
	for author in authors:
		this_author_text = author.text
		if this_author_text != '':
			if this_author_text[-1] == ';':
				this_author_text = this_author_text[:-1]
			all_authors_str = all_authors_str + '[[' + this_author_text + ']], '
	all_authors_str = all_authors_str[:-2]
	pyperclip.copy(all_authors_str)
	print(f'The authors are: {all_authors_str}')
	input("Authors are in your clipboard now. Please change the mathjax to source render. Press Enter to continue...")

	# Need to pause here so that we can change the mathjax to not render.
	# Find a mathjax and right click on it..

	# mathjax = driver.find_elements_by_class_name('display-formula')

	#article = driver.find_element_by_id('article')
	#article_text = article.text
	#article_text = article_text.replace("View Source", "")
	#article_text = article_text.replace("View All", "")
	# Make equations use $$
	#article_text = article_text.replace("\\begin{align*}", "$$")
	#article_text = article_text.replace("\\end{align*}", "$$")
	#article_text = article_text.replace("\\begin{equation*}", "$$")
	#article_text = article_text.replace("\\end{equation*}", "$$")
	#article_text = article_text.replace("\\begin{align}", "$$")
	#article_text = article_text.replace("\\end{align}", "$$")
	#article_text = article_text.replace("\\begin{equation}", "$$")
	#article_text = article_text.replace("\\end{equation}", "$$")
	#article_text = article_text.replace("\\tag{*}", "")
	# I don't know how to do regex good. Just do it twice
	#article_text = re.sub('.tag{.}', '', article_text).strip()
	#article_text = re.sub('.tag{..}', '', article_text).strip()
	#pyperclip.copy(article_text)

	#input("Article is in your clipboard now. Press Enter to continue...")
	# Get the references...
	# Open the reference header references-header

	SCROLL_PAUSE_TIME = 0.5

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height

	ref_header = driver.find_element(By.ID, 'references-header')
	ref_header.click()

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
	time.sleep(SCROLL_PAUSE_TIME)
	references = driver.find_elements(By.CLASS_NAME, 'reference-container')
	# Need to add all strings
	all_refs = ''
	for reference in references:
		this_text = reference.text
		if this_text != '':
			end_of_ref = this_text.find('\nS')
			this_text = this_text[:end_of_ref+1]

			# Remove 1st \n after number...
			this_text = this_text.replace('\n', ' ')
			this_text = this_text + '\n'

			# No Colons in name.
			this_text = this_text.replace(':', '.')
			this_text = this_text.replace('/', '')

			# Look for title to wrap in [[]] for Roam. Assumes Articles and not books
			index_of_title = this_text.find('"') # Find start of article.
			index_of_title_end = this_text.rfind('"') # Find end of article title
			if index_of_title != -1:
				this_text = this_text[:index_of_title+1] + '[[' + this_text[index_of_title+1:index_of_title_end] + ']]' + this_text[index_of_title_end+1:]
			all_refs = all_refs + this_text

	pyperclip.copy(all_refs)
	input('References are copied. Press enter to exit.')

if __name__ == '__main__':
	run_all('6375940')
