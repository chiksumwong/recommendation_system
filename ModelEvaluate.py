
import os
from surprise import Dataset, Reader
from surprise import SVD
from surprise import SVDpp
from surprise import NMF

from surprise.model_selection import cross_validate

try:
    # read data
    file_path = os.path.expanduser('processed/currentModel.csv')
    reader = Reader(line_format='user item rating', sep=',')
    data = Dataset.load_from_file(file_path, reader=reader)

    # chose the algorithms
    algo = SVD()   
    # Run 5-fold cross-validation and print results.
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    algo = SVDpp()
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    algo = NMF()
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

except FileNotFoundError:
    print("Current Model is not exist. Please put the UP file to input folder !")