import os
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
meal='lunch'
meal_no={'breakfast':1,'lunch':2,'dinner':3}
print(meal_no[meal])
information =meal+".csv"
df=pd.DataFrame(columns=["Recipe ID",'Title','Meal','Q_Merge_Label','Ingredients','Calories','Protein','Carbs','Fat','Link','Price','V_0'])
from numpy.random import randint
def get_ingredients(page):
    ingredients = page.soup.findAll(
        'li',
        {'class': "checkList__line"}
    )

    return


def calc_calories(element):
    try:
        tstring = element.get_text()
        print(tstring)
        calories = int(filter(str.isdigit, tstring))
        return calories
    except AttributeError:  # if dom_element not found or no matched
        return 0


def normalize_string(string):
    return re.sub(
        r'\s+', ' ',
        string.replace(
            '\xa0', ' ').replace(  # &nbsp;
            '\n', ' ').replace(
            '\t', ' ').strip()
    )
def scrapping():
    path = 'C:\\Users\\cdr03\\PycharmProjects\\allrecipesScraper\\'+meal # This is your folder name which stores all your html
    id=0
    #be careful that you might need to put a full path such as C:\Users\Niche\Desktop\htmlfolder
    for filename in os.listdir(path): #Read files from your path
        fullpath = os.path.join(path, filename)
        #If we have html tag, then read it
        if fullpath.endswith('.html'):
            list_ingredients = []
            soup = BeautifulSoup(open(fullpath), 'html.parser')
            title=soup.find('h1').get_text()

            url = filename.replace(" ", "-")
            url = "http://allrecipes.com/Recipe/{}/".format(url.split("/")[-1].split(".")[0])
            url = re.sub('---Allrecipes/$', '', url)
            print(url)
            calories=re.findall(r'\d+', soup.find("span", itemprop='calories').get_text())
            fat=soup.find("span", itemprop='proteinContent').get_text()
            carbs=soup.find("span", itemprop='carbohydrateContent').get_text()
            protein=soup.find("span", itemprop='fatContent').get_text()
            for el in soup.find_all('li',
                {'class': "checkList__line"}):
                if el.get_text(strip=True) not in (
                'Add all ingredients to list',
                '',
                'ADVERTISEMENT'):
                    list_ingredients.append(el.get_text(strip=True))
            print(list_ingredients)
            df.loc[id]=[id+1,title,meal_no[meal],10*meal_no[meal]+id+1,list_ingredients,calories[0],fat,carbs,protein,url,randint(5, 15),0]
            id+=1
    df.to_csv(information, sep=';')


if __name__ == '__main__':
    scrapping()