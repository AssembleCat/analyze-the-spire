import pandas as pd

from type import sts_static


def event_choices_set(data_path):
    df = pd.read_parquet(data_path, columns=['event_choices'])
    event_names = set()

    for event_list in df["event_choices"]:
        for event in event_list:
            event_names.add(event["event_name"])

    return sorted(event_names)


def card_set(data_path):
    df = pd.read_parquet(data_path, columns=['master_deck'])
    card_names = set()

    for card_list in df['master_deck']:
        for card in card_list:
            card_names.add(card)

    return sorted(card_names)


if __name__ == '__main__':
    card_set = card_set('../preprocessed/sample.parquet')

    print(len(card_set))

    include, exclude = [], []

    for card in sts_static.ALL_CARDS:
        if card in card_set:
            include.append(card)
        else:
            exclude.append(card)
    print(f'include: {include}')
    print(f'exclude: {exclude}')
