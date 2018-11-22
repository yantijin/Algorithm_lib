def data_reader(filename):
    "Read csv file as rows"
    import csv
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            yield row


def split(dataset, ratio):
    "Split dataset into traning set and test set"
    import random
    random.shuffle(dataset)
    length = len(dataset)
    k = int(length * ratio)
    return dataset[:k], dataset[k:]