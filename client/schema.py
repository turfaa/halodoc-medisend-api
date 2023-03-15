import json
from dataclasses import dataclass, asdict
from typing import List, Optional, TypeVar, Generic, Any

T = TypeVar('T')


@dataclass
class PaginatedResponse(Generic[T]):
    next_page: bool
    result: List[T]
    total_count: int

    @classmethod
    def from_dict(cls, data: dict, item_type: type) -> 'PaginatedResponse':
        result: List[T]

        if hasattr(item_type, 'from_dict'):
            result = [item_type.from_dict(item_data) for item_data in data['result']]
        else:
            result = [item_type(**item_data) for item_data in data['result']]

        return cls(data['next_page'], result, data['total_count'])

    def to_dict(self) -> dict:
        result = [item.to_dict() for item in self.result]
        return {'next_page': self.next_page, 'result': result, 'total_count': self.total_count}

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.to_dict, sort_keys=True, indent=4)


@dataclass
class Image:
    type: str
    extension: str
    url: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, image_dict: dict) -> "Image":
        return cls(**image_dict)


@dataclass
class Inventory:
    id: int
    merchant_location_id: str
    product_id: str
    available_quantity: int
    reserved_quantity: Optional[int]
    status: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, inventory_dict: dict) -> "Inventory":
        return cls(**inventory_dict)


@dataclass
class MerchantProduct:
    id: int
    external_id: str
    product_id: str
    currency: str
    sku_id: str
    active: bool
    cost_price: float
    merchant_id: str
    merchant_location_id: str
    recommended_merchant_price: Optional[float]
    product: Optional[Any]
    uom_price_conversion_attribute: Optional[Any]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, merchant_product_dict: dict) -> "MerchantProduct":
        return cls(**merchant_product_dict)


@dataclass
class Product:
    id: int
    created_at: int
    external_id: str
    product_id: Optional[str]
    entity_id: Optional[str]
    name: str
    meta_description: str
    meta_keywords: str
    type: str
    base_price: float
    currency: str
    thumbnail_url: str
    image_url: str
    status: str
    display: bool
    recommended_merchant_price: Optional[str]
    uom: str
    visual_cues: List[str]
    images: List[Image]
    inventory: Inventory
    merchant_product: MerchantProduct
    max_allowable_price: float
    min_allowable_price: float

    def to_dict(self) -> dict:
        product_dict = asdict(self)
        product_dict["images"] = [image.to_dict() for image in self.images]
        product_dict["inventory"] = self.inventory.to_dict()
        product_dict["merchant_product"] = self.merchant_product.to_dict()
        return product_dict

    @classmethod
    def from_dict(cls, product_dict: dict) -> "Product":
        images = [Image.from_dict(image_dict) for image_dict in product_dict["images"]]
        inventory = Inventory.from_dict(product_dict["inventory"])
        merchant_product = MerchantProduct.from_dict(product_dict["merchant_product"])
        product_dict["images"] = images
        product_dict["inventory"] = inventory
        product_dict["merchant_product"] = merchant_product
        return cls(**product_dict)


@dataclass
class Cookies:
    user_id: str  # Cookie name: afUserId
    session_id: str  # Cookie name: medisend-session-prod

    def to_dict(self) -> dict:
        return {'afUserId': self.user_id, 'medisend-session-prod': self.session_id}

    @classmethod
    def from_dict(cls, cookies_dict: dict) -> "Cookies":
        return cls(cookies_dict['afUserId'], cookies_dict['medisend-session-prod'])
