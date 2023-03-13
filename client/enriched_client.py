from typing import List

from .client import Client
from .schema import Product


class EnrichedClient(Client):
    """
    EnrichedClient is a Client with additional features.
    """

    def get_unavailable_products(self, per_page: int = 20) -> List[Product]:
        """
        Get all unavailable products.
        This method calls get_products() multiple times until all products are fetched.

        Definition of unavailable product:
        - Product is not active, or
        - Product has no inventory

        :param per_page: The number of items per page.
        :return:
        """
        products: List[Product] = []
        page_no = 1

        while True:
            print(f"Fetching page {page_no}...")
            response = self.get_products(page_no, per_page)
            print(f"Found {len(response.result)} products.")

            products.extend(response.result)
            if not response.next_page:
                break

            page_no += 1

        return [product for product in products
                if (not product.merchant_product.active) or (product.inventory.available_quantity == 0)
                ]
