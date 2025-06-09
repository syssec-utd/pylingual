def get_price_repository(self):
    """ Price repository """
    from .repositories import PriceRepository
    if not self.price_repo:
        self.price_repo = PriceRepository(self.session)
    return self.price_repo