from typing import List

data_schema = {
  "access_points": {
    "category": {
      "products": [
        {
          "model": "",
          "title": "",
          "specs": [],
          "thumbnails": [],
          "product_url": "",
          "datasheet_url": "",
        }
      ]
    }
  }
}

class Schema:
  @staticmethod
  def create_product(model: str, title: str, specs: List[str], thumbnails: List[str], product_url: str, datasheet_url: str):
    return {
      "model": model,
      "title": title,
      "specs": specs,
      "thumbnails": thumbnails,
      "product_url": product_url,
      "datasheet_url": datasheet_url,
    }
