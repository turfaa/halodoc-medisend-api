import requests

from client.schema import Product, PaginatedResponse, Cookies


class MedisendClientError(Exception):
    """Raised when there is an error from the Medisend API.

    Attributes:
        status_code -- HTTP status code.
        code -- error code.
        message -- explanation of the error.
    """

    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(f"{status_code} {code}: {message}")

    def __str__(self):
        return f"{self.status_code}-{self.code}: {self.message}"


class Client:
    base_url: str
    cookies: Cookies

    def __init__(self, cookies: Cookies, base_url: str = "https://medisend.api.halodoc.com/api/v1"):
        self.base_url = base_url
        self.cookies = cookies

    def get_products(self, page_no: int, per_page: int, name: str = None) -> PaginatedResponse[Product]:
        """
        Get products
        :param page_no: The page number is 1-based.
        :param per_page: The number of items per page.
        :param name: Filter by name.
        :return: PaginatedResponse[Product]
        """

        params = {
            "page_no": page_no,
            "per_page": per_page,
        }

        if name:
            params["name"] = name

        response = self._get("/products", params=params)
        return PaginatedResponse.from_dict(response, Product)

    def update_product(self, product: Product) -> Product:
        """
        Update a product.
        :param product: Product to update.
        :return: None
        """
        response = self._put(f"/products/{product.id}", product.to_dict())
        return Product.from_dict(response)

    def _get(self, path: str, params: dict = None) -> dict:
        response = requests.get(self.base_url + path, params=params, cookies=self.cookies.to_dict())
        if response.status_code != 200:
            error = response.json()
            raise MedisendClientError(response.status_code, error["code"], error["message"])

        return response.json()

    def _put(self, path: str, data: dict) -> dict:
        response = requests.put(self.base_url + path, json=data, cookies=self.cookies.to_dict())
        if response.status_code != 200:
            error = response.json()
            raise MedisendClientError(response.status_code, error["code"], error["message"])

        return response.json()