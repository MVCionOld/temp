from decimal import Decimal

from bs4 import BeautifulSoup


def parse_valutes(content, cur_from, cur_to, default_valute="RUR"):
    soup = BeautifulSoup(content, "xml")

    def get_valute(currency):
        nonlocal soup, default_valute
        if currency != default_valute:
            value = soup \
                .find(name="CharCode", text=currency) \
                .find_next_sibling("Value") \
                .string \
                .replace(",", ".")
            nominal = soup \
                .find(name="CharCode", text=currency) \
                .find_next_sibling(name="Nominal") \
                .string
            return value, nominal
        else:
            return "1.0", "1"

    cur_from_val, cur_from_nominal = get_valute(cur_from)
    cur_to_val, cur_to_nominal = get_valute(cur_to)

    return {
        cur_from: {
            "value": Decimal(cur_from_val),
            "nominal": Decimal(cur_from_nominal)
        },
        cur_to: {
            "value": Decimal(cur_to_val),
            "nominal": Decimal(cur_to_nominal)
        }
    }


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(
        "http://www.cbr.ru/scripts/XML_daily.asp",
        {"date_req": date}
    )
    cur_info = parse_valutes(response.content, cur_from, cur_to)

    result = (amount * cur_info[cur_from]["value"] *
              cur_info[cur_to]["nominal"]) / \
             (cur_info[cur_to]["value"] * cur_info[cur_from]["nominal"])

    return result.quantize(Decimal('1.0000'))

