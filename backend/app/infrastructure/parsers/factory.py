from .nordnet_parser import NordnerCsvParser

def get_provider_parser(provider: str):
    if provider == "nordnet":
        return NordnerCsvParser()
    else:
        raise ValueError("unsupported provider")    