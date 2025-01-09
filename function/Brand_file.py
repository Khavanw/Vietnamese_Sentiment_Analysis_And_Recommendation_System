class Brand:
    def __init__(self,brand_id=None, brand_name=None):
        self._brand_id=brand_id
        self._brand_name=brand_name
    @property
    def getBrandId(self):
        return self._brand_id
    @property
    def getBrandName(self):
        return self._brand_name
