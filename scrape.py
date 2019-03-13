# imports
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request as request
import csv
# website urls
url = "https://www.allrecipes.com/"

# Chrome session
# driver = webdriver.Chrome(executable_path=r"C:/Users/ehass/Documents/Dev/Web Scraping/chromedriver.exe")

# adding the extension to block ads (AdBlock)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension('AdBlock_v3.41.0.crx')
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(1600, 1200)

# Open the url
driver.get(url)
driver.implicitly_wait(10)

# navigate to Browse button and click on All Categories link
browse_xpath = "//li[@class='browse-recipes']/a[@id='navmenu_recipes']"

BrowseButton = driver.find_element_by_xpath(browse_xpath)
BrowseButton.click()

# click on All categories
BrowseCategories = driver.find_element_by_xpath("//a[text()='All Categories']")
BrowseCategories.click()

driver.implicitly_wait(3)
data=[]
#creating csv file
f = csv.writer(open('data.csv', 'w'))
f.writerow(['ID', 'Name', 'SubmitedBy', 'Ingredients', 'Direction', 'Type', 'Servings', 'Calories', 'PrepTime', 'CookTime', 'ReadyIn', 'ImageName'])


# getting all the list of Categories
li_path = "//h3[@class='heading__h3' and text()='Diet and Health']/../../section[1]//ul//li"
sections = len(driver.find_elements_by_xpath(li_path))

print(sections)
#
recipe_name = ""
submittedBy= ""
ingredientsArray = ""
directionArray = ""
typeOfMeal = ""
serving = ""
calories = ""
prepTime = ""
cookTime = ""
readyTime = ""
ImageName = ""
for s in range(sections-1):

    print('*****************************clicked on ' + driver.find_element_by_xpath(li_path+'['+str(s+1)+']//a').text+'**********************************')
    typeOfMeal = driver.find_element_by_xpath(li_path+'['+str(s+1)+']//a').text
    driver.find_element_by_xpath(li_path+'['+str(s+1)+']//a').click()

    driver.implicitly_wait(3)
    recipe_card_xpath = "//article[@class='fixed-recipe-card']"
    recipe_cards = len(driver.find_elements_by_xpath(recipe_card_xpath))

    print('Recipe card length '+str(recipe_cards))
# clicking on each recipes and getting data
    for i in range(recipe_cards-1):

        # check if the button is displayed
        if len(driver.find_elements_by_xpath(recipe_card_xpath + "[" + str(i + 1) + "]" + "//h3[@class='fixed-recipe-card__h3']")) > 0:
            button = driver.find_element_by_xpath(
                recipe_card_xpath + "[" + str(i + 1) + "]" + "//h3[@class='fixed-recipe-card__h3']")
            actions = ActionChains(driver)
            actions.move_to_element(button)
            # actions.click(button)
            actions.perform()
            driver.implicitly_wait(2)
            button.click()
            print("Button clicked")
            driver.implicitly_wait(5)

            recipe_name_xpath = "//h1[@id='recipe-main-content']"
            alt_recipe_name_xpath = "//div[@class='intro article-info']/h1"
            # recipe_name = driver.find_element_by_xpath(recipe_name_xpath)
            # alt_recipe_name = driver.find_element_by_xpath(alt_recipe_name_xpath)
            ingredientsArray = ""
            directionArray = ""
            if len(driver.find_elements_by_xpath(recipe_name_xpath)) > 0:
                recipe_name = driver.find_element_by_xpath(recipe_name_xpath)
                print('################'+recipe_name.text+'####################')

                # get the image
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                icon = soup.find('a', {'class': 'video-play'})

                folder = 'C:/Users/ehass/Documents/Dev/Web Scraping/Images/'
                request.urlretrieve(icon.img['src'], folder + (icon.img['alt']).replace('"', '').replace('Photo of ', '') + '.jpeg')

                if len(driver.find_elements_by_xpath("//div[@class='hero-photo__wrap']//img")) > 1:
                    ImageName = driver.find_element_by_xpath("//div[@class='hero-photo__wrap']//img[2]").get_attribute("alt")
                else:
                    ImageName = driver.find_element_by_xpath("//div[@class='hero-photo__wrap']//img").get_attribute("alt")

                # getting servings
                if len(driver.find_elements_by_xpath("//div[@class='submitter']//span[@class='submitter__name']")) > 0:
                    submittedBy = driver.find_element_by_xpath("//div[@class='submitter']//span[@class='submitter__name']").text
                    print("Submitted by : " + str(submittedBy))

                # getting servings
                if len(driver.find_elements_by_xpath("//span[@class ='servings-count']")) > 0:
                    serving = driver.find_element_by_xpath("//span[@class ='servings-count']/span[1]").text
                    print("Servings : "+ str(serving)+" servings")

                # getting calories
                if len(driver.find_elements_by_xpath("//span[@class ='calorie-count']")) > 0:
                    calories = driver.find_element_by_xpath("//span[@class ='calorie-count']/span[1]").text
                    print("Calories : " + str(calories) + " cals")


                # getting the ingredients
                ingredients_xpath = "//li[@class ='checkList__line']//label//span"
                ingredients = len(driver.find_elements_by_xpath(ingredients_xpath))
                print("Ingredients are - ")

                for j in range(ingredients):
                    ingredient_name = driver.find_elements_by_xpath(ingredients_xpath)[j].text
                    ingredientsArray = ingredientsArray +"$$$"+ ingredient_name
                print(ingredientsArray)

                # getting prep time
                if len(driver.find_elements_by_xpath("//time[@itemprop='prepTime']/span")) > 0:
                    prepTime = driver.find_element_by_xpath("//time[@itemprop='prepTime']/span").text
                    print("Prep time is : "+ str(prepTime))

                # getting cook time
                if len(driver.find_elements_by_xpath("//time[@itemprop='cookTime']/span")) > 0:
                    cookTime = driver.find_element_by_xpath("//time[@itemprop='cookTime']/span").text
                    print("Cook time is : "+ str(cookTime))

                # getting ready in time
                if len(driver.find_elements_by_xpath("//time[@itemprop='totalTime']/span")) > 0:
                    readyTime = driver.find_element_by_xpath("//time[@itemprop='totalTime']/span").text
                    print("Ready in time is : "+ str(readyTime))

                # getting the directions
                direction_xpath = "//div[@class='directions--section__steps ng-scope']//ol//li[@class='step']"

                directions = len(driver.find_elements_by_xpath(direction_xpath))
                for d in range(directions-1):
                    direction = driver.find_element_by_xpath(direction_xpath + '[' + str(d + 1) + ']').text
                    directionArray = directionArray + "$$$" + direction
                print(directionArray)

                driver.execute_script("window.history.go(-1)")
                driver.implicitly_wait(5)

                # go back to initial page
            elif len(driver.find_elements_by_xpath(alt_recipe_name_xpath)) > 0:
                alt_recipe_name = driver.find_element_by_xpath(alt_recipe_name_xpath)
                print(alt_recipe_name.text)
                ingredients_xpath = "//ul[@class='ingredients-section']//li//span[@class='ingredients-item-name']"
                ingredients = len(driver.find_elements_by_xpath(ingredients_xpath))
                print("Ingredients are - ")

                for j in range(ingredients):
                    ingredient_name = driver.find_elements_by_xpath(ingredients_xpath)[j].text.strip()
                    ingredientsArray = ingredientsArray + "$$$" + ingredient_name
                print(ingredientsArray)


                tempData = [i, recipe_name, submittedBy, ingredientsArray, directionArray, typeOfMeal, serving, calories, prepTime, cookTime, readyTime, ImageName]
                data.append(tempData)
                driver.execute_script("window.history.go(-1)")
                driver.implicitly_wait(5)

    with open('data.csv', 'wb') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)
    driver.execute_script("window.history.go(-1)")
    driver.implicitly_wait(5)


