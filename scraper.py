# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Import Necessary Packages

# %%
# Import necessary modules in ascending order by line length
# Just b/c
import os
import time
import math
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %% [markdown]
# ## Test New Scrapers

# %%
# Create a DataFrame of the sentences to be translated
source = pd.read_excel('Source [TEST].xlsx', header = None)
source.columns = ['origin', 'language', 'extra']
# Get the project name
project = source.language[1]
# Get the language
language = source.language[0]
# Drop the language column
source = source.drop(columns = 'language')
# Drop the extra column
source = source.drop(columns = 'extra')
# Drop nulls
source = source.dropna(axis = 0)


# %%
# Set the Driver up
# Instantiate an Options object
option = webdriver.ChromeOptions()
#Remove navigator.webdriver flag
option.add_argument('--disable-blink-features=AutomationControlled')
# Change the resolution of the browser
option.add_argument("window-size=810,1080")
# Adjusting the user agent
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

# %% [markdown]
# ### QQ Scraper

# %%
# Define the URL to be opened
url = 'https://fanyi.qq.com/'
#Open Browser
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
# Open the specfied URL
driver.get(url)
# Sleep to avoid errors
time.sleep(random.uniform(2.0, 4.0))
# Open the "Select Language" dropdown menu
buttonSource = driver.find_element_by_xpath('//*[@id="language-button-group-target"]/div[1]').click()
# Sleep to avoid errors
time.sleep(random.uniform(2.0, 4.0))
# Click the English button
button = driver.find_element_by_xpath('//*[@id="language-button-group-target"]/div[2]/ul/li[2]/span').click()
# Sleep to avoid errors
time.sleep(random.uniform(2.0, 4.0))
# Find the text field
textFieldSource = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/textarea')
# Sleep to avoid errors
time.sleep(random.uniform(2.0, 4.0))
# Type the text into the text field
batch = 1
sentencesCleanBatches = {}
sentencesClean = []
for row in source['origin']:
    textFieldSource.send_keys(row)
    textFieldSource.send_keys(Keys.RETURN)
    try:
        char_usage = driver.find_element_by_xpath('//*[@id="J-container"]/div[2]/div[1]/div/div[2]/div[2]/div/div[4]/div[2]/span').text
        char_usage1 = char_usage[0:4]
        char_usage2 = char_usage1.strip()
        char_count = int(char_usage2)
    except Exception:
        char_count = 0
        pass
    if char_count >= 4500:
        # Pause to avoid errors
        time.sleep(5)
        # Store the translated text as a string
        translatedText = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]')
        translatedTextList = translatedText.find_element_by_xpath('./*')
        translatedText_content = translatedText.get_attribute('innerHTML').strip()
        translatedText_content = translatedText_content.replace(" &nbsp;", "")
        translatedText_content = translatedText_content.replace("&nbsp;", "")
        # Sleep to avoid errors
        time.sleep(2)
        # Clean the output text and print
        sentencesCleanBatches[batch] = translatedText_content.split("\n")
        batch += 1
        # Clear the input field
        textFieldSource.clear()
# Pause to avoid errors
time.sleep(5)
# Store the translated text as a string
translatedText = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]')
translatedTextList = translatedText.find_element_by_xpath('./*')
translatedText_content = translatedText.get_attribute('innerHTML').strip()
translatedText_content = translatedText_content.replace(" &nbsp;", "")
translatedText_content = translatedText_content.replace("&nbsp;", "")
# Sleep to avoid errors
time.sleep(2)
# Clean the output for the last batch
sentencesCleanBatches[batch] = translatedText_content.split("\n")
# Concatenate all the batches into once list
for i in range(1, batch + 1):
    sentencesClean = sentencesClean + sentencesCleanBatches[i]
# Sleep to avoid errors
time.sleep(2)
# Close the browser window
driver.quit()
# Return the sentences
return sentencesClean

# %% [markdown]
# ## Scrape Machine Translation Services

# %%
# Define start time
startTime = time.time()
# Set the Driver up
# Instantiate an Options object
option = webdriver.ChromeOptions()
#Remove navigator.webdriver flag
option.add_argument('--disable-blink-features=AutomationControlled')
# Change the resolution of the browser
option.add_argument("window-size=810,1080")
# Adjusting the user agent
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
# Define time functions
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%dh %02dm %02ds" % (hour, minutes, seconds)
def convertTTS(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d hours %02d minutes %02d seconds" % (hour, minutes, seconds)
# Define scraping functions
def scrapeSoGou():
    # Define the URL to be opened
    url = 'https://translate.sogou.com/text'
    #Open Browser
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    # Open the specfied URL
    driver.get(url)
    # Sleep to avoid errors
    time.sleep(random.uniform(2.0, 4.0))
    # Open the "Select Language" dropdown menu
    buttonSource = driver.find_element_by_xpath('//*[@id="J-langselect"]/div/span[3]').click()
    # Sleep to avoid errors
    time.sleep(random.uniform(2.0, 4.0))
    # Click the English button
    button = driver.find_element_by_xpath('//*[@id="languageList"]/div[2]/span[2]').click()
    # Sleep to avoid errors
    time.sleep(random.uniform(2.0, 4.0))
    # Find the text field
    textFieldSource = driver.find_element_by_xpath('//*[@id="trans-input"]')
    # Sleep to avoid errors
    time.sleep(random.uniform(2.0, 4.0))
    # Type the dummy text into the text field to trigger the bot detection
    textFieldSource.send_keys('我喜欢吃冰淇淋.')
    # Sleep to allow for manual bot-detectiong passing
    time.sleep(20)
    # Clear the text input field
    bClear = driver.find_element_by_xpath('//*[@id="J-container"]/div[2]/div[1]/div/div[2]/div[2]/div/span').click()
    # Sleep to avoid errors
    time.sleep(random.uniform(2.0, 4.0))
    # Find the text field and clear it
    textFieldSource = driver.find_element_by_xpath('//*[@id="trans-input"]').clear()
    # Find the text field once more
    textFieldSource = driver.find_element_by_xpath('//*[@id="trans-input"]')
    # Type the text into the text field
    batch = 1
    sentencesCleanBatches = {}
    sentencesClean = []
    for row in source['origin']:
        # Find the text field once more
        textFieldSource = driver.find_element_by_xpath('//*[@id="trans-input"]')
        textFieldSource.send_keys(row)
        textFieldSource.send_keys(Keys.RETURN)
        try:
            char_usage = driver.find_element_by_xpath('//*[@id="J-container"]/div[2]/div[1]/div/div[2]/div[2]/div/div[4]/div[2]/span').get_attribute('innerHTML')
            char_usage1 = char_usage[0:4]
            char_usage2 = char_usage1.strip()
            char_count = int(char_usage2)
        except Exception:
            char_count = 0
            pass
        if char_count >= 4500:
            print(char_count)
            # Pause to avoid errors
            time.sleep(5)
            # Store the translated text as a string
            translatedText = driver.find_element_by_xpath('//*[@id="trans-result"]')
            translatedText_content = translatedText.get_attribute('innerHTML').strip()
            translatedText_content = translatedText_content.replace(" &nbsp;", "")
            translatedText_content = translatedText_content.replace("&nbsp;", "")
            # Sleep to avoid errors
            time.sleep(2)
            # Clean the output text and print
            sentencesCleanBatches[batch] = translatedText_content.split("\n")
            batch += 1
            # Clear the input field
            try:
                bClear = driver.find_element_by_xpath('//*[@id="J-container"]/div[2]/div[1]/div/div[2]/div[2]/div/span').click()
            except Exception:
                pass
            textFieldSource = driver.find_element_by_xpath('//*[@id="trans-input"]').clear()
            try:
                textFieldSource2 = driver.find_element_by_xpath('//*[@id="input-placeholder"]').clear()
            except Exception:
                pass
    # Pause to avoid errors
    time.sleep(5)
    # Store the translated text as a string
    translatedText = driver.find_element_by_xpath('//*[@id="trans-result"]')
    translatedText_content = translatedText.get_attribute('innerHTML').strip()
    translatedText_content = translatedText_content.replace(" &nbsp;", "")
    translatedText_content = translatedText_content.replace("&nbsp;", "")
    # Sleep to avoid errors
    time.sleep(2)
    # Clean the output for the last batch
    sentencesCleanBatches[batch] = translatedText_content.split("\n")
    # Concatenate all the batches into once list
    for i in range(1, batch + 1):
        sentencesClean = sentencesClean + sentencesCleanBatches[i]
    # Sleep to avoid errors
    time.sleep(2)
    # Close the browser window
    driver.quit()
    # Retrieve the sentences
    return sentencesClean
def scrapeDeepL(language):
    # Define the URL to be opened
    url = 'https://www.deepl.com/translator'
    # Define the driver for Selenium to use
    driver = webdriver.Chrome('chromedriver.exe')
    # Open the specfied URL
    driver.get(url)
    # Sleep to avoid errors
    time.sleep(2)
    # Open the "Select Language" dropdown menu
    buttonSource = driver.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[2]/div[1]/div[1]/div/button').click()
    # Sleep to avoid errors
    time.sleep(2)
    if language == '中文':
        # Click the Chinese button
        button = driver.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[2]/div[1]/div[1]/div/div/button[12]').click()
    else:
        # Click the Japanese button
        button = driver.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[2]/div[1]/div[1]/div/div/button[11]').click()
    # Sleeep to avoid errors
    time.sleep(2)
    # Find the text field
    textFieldSource = driver.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[2]/div[1]/div[2]/div[1]/textarea')
    # Type the text into the text field
    test = source.loc[0:0].to_string(index = False, columns = None, header = False)
    batch = 1
    sentencesCleanBatches = {}
    sentencesClean = []
    for row in source['origin']:
        textFieldSource.send_keys(row)
        textFieldSource.send_keys(Keys.RETURN)
        try:
            char_usage = driver.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[2]/div[1]/div[2]/div[3]').text
            char_usage1 = char_usage[0:4]
            char_usage2 = char_usage1.strip()
            char_count = int(char_usage2)
        except Exception:
            char_count = 0
            pass
        if char_count >= 4500:
            print(char_count)
            # Pause to avoid errors
            time.sleep(5)
            # Store the translated text as a string
            translatedText = driver.find_element_by_xpath('//*[@id="target-dummydiv"]')
            translatedText_content = translatedText.get_attribute('innerHTML').strip()
            # Sleep to avoid errors
            time.sleep(2)
            # Clean the output text and print
            sentencesCleanBatches[batch] = translatedText_content.split("\n")
            batch += 1
            # Clear the input field
            textFieldSource.clear()
    # Pause to avoid errors
    time.sleep(5)
    # Store the translated text as a string
    translatedText = driver.find_element_by_xpath('//*[@id="target-dummydiv"]')
    translatedText_content = translatedText.get_attribute('innerHTML').strip()
    # Sleep to avoid errors
    time.sleep(2)
    # Clean the output for the last batch
    sentencesCleanBatches[batch] = translatedText_content.split("\n")
    # Concatenate all the batches into once list
    for i in range(1, batch + 1):
        sentencesClean = sentencesClean + sentencesCleanBatches[i]
    # Sleep to avoid errors
    time.sleep(2)
    # Close the browser window
    driver.quit()
    return sentencesClean
def scrapePapago(language):
    # Define the URL to be opened
    url = 'https://papago.naver.com/'
    # Define the driver for Selenium to use
    driver = webdriver.Chrome('chromedriver.exe')
    # Open the specfied URL
    driver.get(url)
    # Sleep to avoid errors
    time.sleep(2)
    # Find the Text Field and type the sentences
    textFieldSource = driver.find_element_by_xpath('//*[@id="txtSource"]')
    test = source.loc[0:0].to_string(index = False, columns = None, header = False)
    batch = 1
    sentencesCleanBatches = {}
    sentencesClean = []
    for row in source['origin']:
        textFieldSource.send_keys(row)
        textFieldSource.send_keys(Keys.RETURN)
        try:
            char_usage = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/section/div/div[1]/div[1]/div/p[1]').text
            char_usage1 = char_usage[0:4]
            char_usage2 = char_usage1.strip()
            char_count = int(char_usage2)
        except Exception:
            char_count = 0
            pass
        if char_count >= 4500:
            print(char_count)
            # Pause to avoid errors
            time.sleep(5)
            # Push the Translate button
            translate_button = driver.find_element_by_xpath('//*[@id="btnTranslate"]').click()
            # Pause to avoid errors
            time.sleep(5)
            # Store the translated text as a string
            translatedText = driver.find_element_by_xpath('//*[@id="txtTarget"]')
            translatedText_content = translatedText.text
            # Clean the output text and print
            sentencesCleanBatches[batch] = translatedText_content.split("\n")
            batch += 1
            # Clear the input field
            textFieldSource.clear()
    # Pause to avoid errors
    time.sleep(5)
    # Push the Translate button
    translate_button = driver.find_element_by_xpath('//*[@id="btnTranslate"]').click()
    # Pause to avoid errors
    time.sleep(5)
    # Store the translated text as a string
    translatedText = driver.find_element_by_xpath('//*[@id="txtTarget"]')
    translatedText_content = translatedText.text
    # Clean the output text and print
    sentencesCleanBatches[batch] = translatedText_content.split("\n")
    # Concatenate all the batches into once list
    for i in range(1, batch + 1):
        sentencesClean = sentencesClean + sentencesCleanBatches[i]
    # Close the browser window
    driver.quit()
    # Return necessary objects
    return sentencesClean
def scrapeGoogleTranslate():
    # Define the URL to be opened
    url = 'https://translate.google.com/'
    # Define the driver for Selenium to use
    driver = webdriver.Chrome('chromedriver.exe')
    # Open the specfied URL
    driver.get(url)
    # Sleep to avoid errors
    time.sleep(2)
    # Text Input Field
    textFieldSource = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea')
    test = source.loc[0:0].to_string(index = False, columns = None, header = False)
    batch = 1
    sentencesCleanBatches = {}
    sentencesClean = []
    for row in source['origin']:
        textFieldSource.send_keys(row)
        textFieldSource.send_keys(Keys.RETURN)
        try:
            char_usage = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/div[5]/div[2]/span/span').text
            char_count = int(char_usage)
        except Exception:
            char_count = 0
            pass
        if char_count >= 4500:
            print(char_count)
            # Pause to avoid errors
            time.sleep(5)
            # Store the translated text as a string
            translatedText = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]')
            translatedText_content = translatedText.text
            # Clean the output text and print
            sentencesCleanBatches[batch] = translatedText_content.split("\n")
            batch += 1
            # Clear the input field
            textFieldSource.clear()
    # Pause to avoid errors
    time.sleep(5)
    # Store the translated text as a string
    translatedText = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]')
    translatedText_content = translatedText.text
    # Clean the output text and print
    sentencesCleanBatches[batch] = translatedText_content.split("\n")
    # Concatenate all the batches into once list
    for i in range(1, batch + 1):
        sentencesClean = sentencesClean + sentencesCleanBatches[i]
    # Close the driver
    driver.quit()
    return sentencesClean
# Create a DataFrame of the sentences to be translated
source = pd.read_excel('Source.xlsx', header = None)
source.columns = ['origin', 'language', 'extra']
# Get the project name
project = source.language[1]
# Get the language
language = source.language[0]
# Drop the language column
source = source.drop(columns = 'language')
# Drop the extra column
source = source.drop(columns = 'extra')
# Drop nulls
source = source.dropna(axis = 0)
# Determine which scraper to use
if language == '한국어':
    sentencesClean = scrapePapago(language)
    service = 'Papago'
else:
    sentencesCleanSoGou = scrapeSoGou()
    sentencesClean = scrapeDeepL(language)
    service = 'DeepL' 
sentencesCleanGoogle = scrapeGoogleTranslate()
# Create a DataFrame
cols = [language, 'Final', 'Final Count', service, '{} Count'.format(service), 'Final - {}'.format(service), 'Google Translate', 'Google Translate Count', 'Final - Google', 'SoGou', 'SoGou Count', 'Final - SoGou']
df = pd.DataFrame(columns = cols)
df[service] = sentencesClean
df[language] = source['origin']
while("" in sentencesCleanGoogle) : 
    sentencesCleanGoogle.remove("") 
df['Google Translate'] = sentencesCleanGoogle
df['SoGou'] = sentencesCleanSoGou
# Drop nan rows
df.dropna(how = 'all', inplace = True, axis = 0)
# Export DataFrame as an XLSX to Google Drive\Work\Translation folder
df.to_excel('{}\{}.xlsx'.format(language, project), index=False)
os.startfile('{}\{}.xlsx'.format(language, project))


# %%
df.dropna(how = 'all', inplace = True, axis = 0)
# Export DataFrame as an XLSX to Google Drive\Work\Translation folder
df.to_excel('{}\{}.xlsx'.format(language, project), index=False)
os.startfile('{}\{}.xlsx'.format(language, project))


# %%
while(" " in sentencesCleanGoogle) : 
    sentencesCleanGoogle.remove(" ") 
print(len(sentencesCleanGoogle))
df['Google Translate'] = sentencesCleanGoogle


# %%
len(sentencesCleanGoogle)


# %%
len(sentencesCleanSoGou)


# %%
len(sentencesClean)


# %%
sentencesCleanSoGou


# %%
sentencesCleanGoogle

# %% [markdown]
# ## Calculate Differences

# %%
# Import necessary modules
import difflib
# Variables
language = '中文'
project = 'demo0118'


# %%
df1 = pd.read_excel('{}\{}.xlsx'.format(language, project))
df1.columns


# %%
df1


# %%



