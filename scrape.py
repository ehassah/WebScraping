# imports
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# website urls
videos_url = "https://www.allrecipes.com/"

# Chrome session
# driver = webdriver.Chrome(executable_path=r"C:/Users/ehass/Documents/Dev/Web Scraping/chromedriver.exe")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension('AdBlock_v3.41.0.crx')
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(1600, 1200)
# time.sleep(10)



driver.get(videos_url)
driver.implicitly_wait(10)
# navigate to link
browse_xpath = "//li[@class='browse-recipes']/a[@id='navmenu_recipes']"

BrowseButton = driver.find_element_by_xpath(browse_xpath)
BrowseButton.click()

# click on All categories
BrowseCategories = driver.find_element_by_xpath("//a[text()='All Categories']")
BrowseCategories.click()

driver.implicitly_wait(3)

# section
li_path = "//h3[@class='heading__h3' and text()='Diet and Health']/../../section[1]//ul//li//a"
sections = driver.find_elements_by_xpath(li_path)
for section in sections:
    section.click()
    driver.implicitly_wait(3)
    recipe_card_xpath = "//article[@class='fixed-recipe-card']"
    recipe_cards = len(driver.find_elements_by_xpath(recipe_card_xpath))

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
                print(recipe_name.text)

                ingredients_xpath = "//li[@class ='checkList__line']//label//span"
                ingredients = len(driver.find_elements_by_xpath(ingredients_xpath))
                print("Ingredients are - ")
                for j in range(ingredients):
                    ingredient_name = driver.find_elements_by_xpath(ingredients_xpath)[j].text
                    print(ingredient_name)
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
driver.quit()