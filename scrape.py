# imports
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request as request
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


# getting all the list of Categories
li_path = "//h3[@class='heading__h3' and text()='Diet and Health']/../../section[1]//ul//li"
sections = len(driver.find_elements_by_xpath(li_path))

print(sections)
#
for s in range(sections-1):

    print('*****************************clicked on ' + driver.find_element_by_xpath(li_path+'['+str(s+1)+']//a').text+'**********************************')
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
            if len(driver.find_elements_by_xpath(recipe_name_xpath)) > 0:
                recipe_name = driver.find_element_by_xpath(recipe_name_xpath)
                print('################'+recipe_name.text+'####################')

                # get the image
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                icon = soup.find('a', {'class': 'video-play'})

                folder = 'C:/Users/ehass/Documents/Dev/Web Scraping/Images/'
                request.urlretrieve(icon.img['src'], folder + (icon.img['alt']).replace('"', '').replace('Photo of ', '') + '.jpeg')

                ingredients_xpath = "//li[@class ='checkList__line']//label//span"
                ingredients = len(driver.find_elements_by_xpath(ingredients_xpath))
                print("Ingredients are - ")
                for j in range(ingredients):
                    ingredient_name = driver.find_elements_by_xpath(ingredients_xpath)[j].text
                    print(ingredient_name)
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
                    print(ingredient_name)

                driver.execute_script("window.history.go(-1)")
                driver.implicitly_wait(5)


    driver.execute_script("window.history.go(-1)")
    driver.implicitly_wait(5)
