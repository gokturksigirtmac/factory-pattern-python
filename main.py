from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class ProductPrice:
    """Abstract Factory Interface"""
    @abstractmethod
    def get_product_price(self, url):
        pass

class TrendyolProductPrice(ProductPrice):
    def get_product_price(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_info_container = soup.find('div', class_='product-price-container')
        price_element = product_info_container.find_all('span', class_='prc-dsc') 

        if price_element:
            print(price_element[0].text)
            return
        else:
            return 'Fiyat bilgisi bulunamadı.'

class TeknosaProductPrice(ProductPrice):
    def get_product_price(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_info_container = soup.find('div', class_='pdp-prices')
        price_element = product_info_container.find_all('span', class_='prc') 

        if price_element:
            print(price_element[0].text)
            return
        else:
            return 'Fiyat bilgisi bulunamadı.'

class ProductPriceFactory(ABC):
    @abstractmethod
    def create_product_price(self) -> ProductPrice:
        pass

class ConcreteProductPriceFactory(ProductPriceFactory):
    def create_product_price(self, type: str) -> ProductPrice:
        match type:
            case "trendyol":
                return TrendyolProductPrice()
            case "teknosa":
                return TeknosaProductPrice()
            case _:
                raise ValueError("Bir şeyler ters gitti")

if __name__ == "__main__":
    factory = ConcreteProductPriceFactory()
    url = input("Ürün linki girin \n")
    company = url.split('.')[1]
    price = factory.create_product_price(company).get_product_price(url)