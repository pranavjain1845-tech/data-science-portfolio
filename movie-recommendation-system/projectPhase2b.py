import random
import time
import matplotlib.pyplot as plt

from projectPhase2a import (
    createUserList, createMovieList, readRatings, createRatingsDataStructure,
    randomPrediction, meanUserRatingPrediction, meanMovieRatingPrediction,
    demRatingPrediction, genreRatingPrediction, partitionRatings, rmse
)


def main():
    userList = createUserList()
    movieList = createMovieList()
    rawRatings = readRatings()

    numUsers = len(userList)
    numMovies = len(movieList)

    outcomes = {
        "random": [],
        "userAverage": [],
        "movieAverage": [],
        "demographic": [],
        "genre": []
    }

    keys = ["random", "userAverage", "movieAverage", "demographic", "genre"]

    trial = 0
    while trial < 10:

        trainingSet, testSet = partitionRatings(rawRatings, 20)
        RLu, RLm = createRatingsDataStructure(numUsers, numMovies, trainingSet)

        actual = []
        pred_lists = [[], [], [], [], []]

        j = 0
        while j < len(testSet):
            u, m, rating = testSet[j]
            actual.append(rating)

            p1 = randomPrediction(u, m)
            p2 = meanUserRatingPrediction(u, m, RLu)
            p3 = meanMovieRatingPrediction(u, m, RLm)
            p4 = demRatingPrediction(u, m, userList, RLu)
            p5 = genreRatingPrediction(u, m, movieList, RLu)

            pred_lists[0].append(p1)
            pred_lists[1].append(p2)
            pred_lists[2].append(p3)
            pred_lists[3].append(p4)
            pred_lists[4].append(p5)

            j += 1

        i = 0
        while i < len(keys):
            rmse_val = rmse(actual, pred_lists[i])
            outcomes[keys[i]].append(rmse_val)
            i += 1

        trial += 1


    data = [
        outcomes["random"],
        outcomes["userAverage"],
        outcomes["movieAverage"],
        outcomes["demographic"],
        outcomes["genre"]
    ]

    plt.figure(figsize=(10, 6))
    plt.boxplot(data, patch_artist=True)

    plt.xticks(
        [1, 2, 3, 4, 5],
        ["Random", "User\nAverage", "Movie\nAverage", "Demographic\nAverage", "Genre\nAverage"]
    )

    plt.title("RMSE Scores by Algorithm", fontweight="bold")
    plt.ylabel("Root Mean Squared Error (RMSE)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()