import re


def convert_to_csegp(amount) -> list:
    """
    Takes in a string of the with the amount of money and parses it for a list of integers
    representing the amount of money passed.
    :param amount: str with the amount of money to be converted
    :return: Tuple of ints
    """
    coin_patter_strings = ['cp', 'sp', 'ep', 'gp', 'pp']
    numbers_regex = '[0-9]+'
    matches = []
    for i in coin_patter_strings:
        match = re.search(numbers_regex + i, amount)
        if match is not None:
            matches.append(int(match.group().replace(i, '')))
        else:
            matches.append(0)

    return matches


def convert_from_csegp(amount_list: list) -> str:
    return f'Copper: {amount_list[0]}\nSilver: {amount_list[1]}\nElectrum:' \
           f' {amount_list[2]}\nGold: {amount_list[3]}\nPlatinum: {amount_list[4]}'


def convert_to_copper(amount_list: list) -> int:
    # conversion rates for currency for dnd 5e
    conversion_rate = [1, 10, 50, 100, 1000]
    return sum(x * y for x, y in zip(conversion_rate, amount_list))


def compress_copper(copper_amount: int) -> list:
    """
    compresses the amount of copper into the higher coin types
    Note: copper amount must be positive or we will throw a Value Error
    :param copper_amount: int
    :return: list A list of ints representing the coin types
    """
    conversion_rate = [1, 10, 50, 100, 1000]
    r_conversion_rate = reversed(conversion_rate)
    amount_list = []
    for i in r_conversion_rate:
        coin_amount = copper_amount // i
        amount_list.append(coin_amount)
        copper_amount -= coin_amount * i
    return list(reversed(amount_list))


def add_to_gold(current_gold: str, gold_amount: str) -> list:
    curr_gold = convert_to_csegp(current_gold)
    g_amount = convert_to_csegp(gold_amount)
    return [x + y for x, y in zip(curr_gold, g_amount)]


def subtract_from_gold(current_gold: str, gold_amount: str) -> list:
    curr_gold = convert_to_csegp(current_gold)
    g_amount = convert_to_csegp(gold_amount)
    return [x - y for x, y in zip(curr_gold, g_amount)]


def valid_csegp_string(input_str: str) -> bool:
    return bool(re.match('[0-9]+(cp|sp|gp|pp|ep)+', input_str))
