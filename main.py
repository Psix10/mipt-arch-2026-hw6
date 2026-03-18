from converters.usd_converter import UsdConverter
from converters.rates_provider_api import ApiRatesProvider
from service import read_amount, read_currency





def main():
    provider = ApiRatesProvider()
    currency = read_currency()
    amount = read_amount()

    converter = UsdConverter(provider)
    result = converter.convert(amount, currency)

    print(f"{amount} USD to {currency}: {result:.2f}")


if __name__ == "__main__":
    main()
