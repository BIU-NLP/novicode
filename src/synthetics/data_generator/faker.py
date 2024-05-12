from typing import Optional
from faker import Faker
from faker.providers import BaseProvider, DynamicProvider


class FakerDataGenerator:
    _fake = None

    @classmethod
    def get_faker(cls, seed: Optional[int] = None) -> Faker:
        if not cls._fake:
            if seed:
                Faker.seed(seed)

            cls._fake = Faker()
            cls._fake.add_provider(brand_provider)
            cls._fake.add_provider(DigitsProvider)
            cls._fake.add_provider(TimeProvider)

        return cls._fake


brand_provider = DynamicProvider(
    provider_name="brand",
    elements=[
        "Apple",
        "Amazon",
        "Google",
        "Facebook",
        "Dior",
        "Chanel",
        "Prada",
        "Gucci",
        "Louis Vuitton",
        "Burberry",
        "Hermes",
        "Armani",
        "Ray-Ban",
        "Ralph Lauren",
        "Samsung",
        "Microsoft",
        "Disney",
        "Adidas",
        "Zara",
        "H&M",
        "Nike",
        "Lego",
        "McDonald's",
        "Starbucks",
        "Pepsi",
        "Coca-Cola",
        "Toyota",
        "Mercedes-Benz",
        "BMW",
        "Ford",
        "Honda",
        "Volkswagen",
        "Nissan",
        "Hyundai",
        "Sony",
    ],
)


class DigitsProvider(BaseProvider):
    def digit(self) -> str:
        digits = self.digits(1)
        return digits

    def two_digits(self) -> str:
        digits = self.digits(2)
        return digits

    def digits(self, n: int) -> str:
        fake = FakerDataGenerator.get_faker()
        digits = fake.msisdn()[:n]
        while digits.startswith("0"):
            digits = fake.msisdn()[:n]
        return digits


class TimeProvider(BaseProvider):
    def fake_hour(self) -> str:
        fake = FakerDataGenerator.get_faker()
        hour = int(fake.time("%H"))
        hour = hour % 12 or 12
        hour_str = str(hour)
        return hour_str

    def time_hour(self) -> str:
        fake = FakerDataGenerator.get_faker()
        hours = self.fake_hour()
        time = f"{hours} {fake.am_pm()}"
        return time

    def time_hour_minutes(self) -> str:
        fake = FakerDataGenerator.get_faker()
        hours = self.fake_hour()
        minutes = fake.time("%M")
        time = f"{hours}:{minutes} {fake.am_pm()}"
        return time
    
