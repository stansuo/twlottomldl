import multiprocessing
from itertools import product

def merge_names(a, b):
    return '{} & {}'.format(a, b)


if __name__ == '__main__':
    obs_names = ["Neihu", "Songshan", "Dazhi", "Wenshan","Xizhi", "Shihding", "Shenkeng"]
    obs_years = ["2016", "2017", "2018", "2019", "2020"]
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.starmap(merge_names, product(obs_names, obs_years))
        print(results)

