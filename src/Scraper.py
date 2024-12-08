import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import src.configs as configs
from src.Schema import Schema


class Scraper:
  def __init__(self) -> None:
    self.driver = None
    self.output_data = {}
    self.target_pages = configs.TARGET_URLS

  def start(self):
    self.driver = webdriver.Firefox(configs.DRIVER_OPTIONS)
    self.driver.implicitly_wait(10)

    # Start with Access Points Page
    for target_page in self.target_pages:
      self.driver.get(target_page['url'])
      window_before = self.driver.current_window_handle
      products_elem = self.driver.find_element(By.XPATH, '//div[@class="tp-product-cell tp-filter-product"]')
      categories = products_elem.find_elements(By.XPATH, './/h2[@class="tp-product-cate"]')

      categories_data = {}
      for category in categories:
        category_data = {"products": []}
        products = products_elem.find_elements(By.XPATH, f'.//ul[@class="tp-product-content {'smb' if target_page['name'] == 'switches' else ''}" and @data-id="{category.get_attribute('data-id')}"]//child::li[@class="tp-product-item"]')
        for product in products:
          actions = ActionChains(self.driver)
          # self.driver.execute_script("arguments[0].click();", product.find_element(By.XPATH, './/div[@class="tp-product-model"]'))
          target = product.find_element(By.XPATH, './/div[@class="tp-product-model"]')
          # actions.scroll_to_element(product).perform()
          self.driver.execute_script("arguments[0].scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"nearest\"});", product)
          time.sleep(1)
          actions.move_to_element(target).perform()
          # ActionChains(self.driver).click(product.find_element(By.XPATH, './/div[@class="tp-product-model"]')).perform()
          model = product.find_element(By.XPATH, './/div[@class="tp-product-model"]').text
          time.sleep(1.5)
          title = product.find_element(By.XPATH, './/h2[@class="tp-product-title"]').text
          time.sleep(1.5)
          WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, './/div[@class="tp-product-spec"]/ul//child::li')))
          specs = [x.text for x in product.find_elements(By.XPATH, './/div[@class="tp-product-spec"]/ul//child::li')]
          time.sleep(1.5)
          WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, './/div[@class="tp-product-thumbnail-box"]/img')))
          thumbnails = [x.get_attribute('src') for x in product.find_elements(By.XPATH, './/div[@class="tp-product-thumbnail-box"]/img')]
          time.sleep(1.5)
          product_url = product.find_element(By.XPATH, f'.//a[@aria-label="{model}"]').get_attribute('href')
          time.sleep(2)

          self.driver.switch_to.new_window('tab')
          product_tab = self.driver.current_window_handle
          self.driver.get(product_url)
          support_url = self.driver.find_element(By.XPATH, '''//a[contains(@data-vars-event-category, "Product-Menu_Support")]''').get_attribute('href')

          self.driver.switch_to.new_window('tab')
          self.driver.get(support_url)
          datasheet_url = self.driver.find_element(By.XPATH, '//div[@class="download-list"]/dl[1]/dd/ul/li/a').get_attribute('href')
          self.driver.close()

          self.driver.switch_to.window(product_tab)
          self.driver.close()

          self.driver.switch_to.window(window_before)
          product_data = Schema.create_product(model, title, specs, thumbnails, product_url, datasheet_url)
          category_data['products'] += [product_data]

        categories_data[f'{category.text.replace(' ', '_').lower()}'] = category_data

      self.output_data[f'{target_page['name']}'] = categories_data
      self.output_data[f'{target_page['name']}']['url'] = target_page['url']

    if os.path.exists(configs.OUTPUT_FILE_NAME):
      os.system(f'rm -rf {configs.OUTPUT_FILE_NAME}')

    with open(configs.OUTPUT_FILE_NAME, 'w', encoding='utf8') as json_file:
      data = json.dumps(self.output_data, ensure_ascii=False, indent=2)
      json_file.write(data)

    self.driver.quit()
