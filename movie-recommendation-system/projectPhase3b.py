import random
import matplotlib.pyplot as plt

def createUserList():
    userList = []
    with open("ml-100k/u.user", "r", encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 5:
                user_id, age, gender, occ, zipcode = parts
                user = {
                    "age": int(age),
                    "gender": gender,
                    "occupation": occ,
                    "zip": zipcode
                }
                userList.append(user)
    return userList


def createMovieList():
    movieList = []
    with open("ml-100k/u.item", "r", encoding='latin-1') as f:
       for i in f:
           genreList = []
           L = i.split("|")
           for a in range(5, len(L)):
               genreList.append(int(L[a].strip()))
           dictionary = {"title": L[1],
                         "release date": L[2],
                         "video release date": L[3],
                         "IMDB url": L[4],
                         "genre": genreList}
           movieList.append(dictionary)
    return movieList


def readRatings():
    ratingData = []
    with open("ml-100k/u.data", "r", encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                user = int(parts[0])
                movie = int(parts[1])
                rating = int(parts[2])
                ratingData.append((user, movie, rating))
    return ratingData
        
def createRatingsDataStructure(numUsers, numMovies, ratingTuples):
    rLu = [{} for i in range(numUsers)]
    rLm = [{} for i in range(numMovies)]
    for (user, movie, rating) in ratingTuples:
        userIndex = user - 1
        movieIndex = movie - 1
        rLu[userIndex][movie] = rating
        rLm[movieIndex][user] = rating
    return [rLu, rLm]

def createGenreList():
    genres = []
    with open("ml-100k/u.genre", "r", encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                genre_name = parts[0]
                genres.append(genre_name)
    return genres
 
def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):
    ageMin = ageRange[0]
    ageMax = ageRange[1]
    rMin = ratingRange[0]
    rMax =  ratingRange[1]
    genreCount = 19
    target = []
    for userIndex in range(len(userList)):
        userData = userList[userIndex]
        userGender = userData.get("gender")
        userAge = userData.get("age")
        Match = (userGender == gender) or (gender == "A")
        age = ageMin <= userAge < ageMax
        if Match and age:
            target.append(userIndex)
    totalRating = 0
    for userIndex in target:
        totalRating += len(rLu[userIndex])
    if totalRating == 0:
        return [None] * genreCount
    totalRatingPerCount = [0] * genreCount
    Total = 0
    for userIndex in target:
        userRating = rLu[userIndex]
        for movieID, rating in userRating.items():
            Total += 1
            if rMin <= rating <= rMax:
                movieIndex = movieID - 1
                movieData = movieList[movieIndex]
                movieGenre = movieData.get("genre")
                for a in range(genreCount):
                    totalRatingPerCount[a] += movieGenre[a]
    Fraction = []
    for total in totalRatingPerCount:
        Fraction.append((total/Total))
    return Fraction

import random
import math


def randomPrediction(u, m):
    return random.randint(1, 5)



def meanUserRatingPrediction(u, m, rLu):
    if u < 1 or u > len(rLu):
        return None
    user_ratings = rLu[u - 1]
    if len(user_ratings) == 0:
        return None
    total = 0
    count = 0
    for key in user_ratings:
        total += user_ratings[key]
        count += 1
    return total / count



def meanMovieRatingPrediction(u, m, rLm):
    if m < 1 or m > len(rLm):
        return None
    movie_ratings = rLm[m - 1]
    if len(movie_ratings) == 0:
        return None
    total = 0
    count = 0
    for key in movie_ratings:
        total += movie_ratings[key]
        count += 1
    return total / count



def demRatingPrediction(u, m, userList, rLu):
    if u < 1 or u > len(userList):
        return None

    target = userList[u - 1]
    target_gender = target.get("gender")
    target_age = target.get("age")

    if target_age is None:
        return None

    low = target_age - 5
    high = target_age + 5

    collected = []
    uid = 1

    for user in userList:
        if not (uid != u):
            uid += 1
            continue

        gender = user.get("gender")
        age = user.get("age")

        if gender == target_gender:
            if age is not None:
                if low <= age <= high:
                    ratings_for_user = rLu[uid - 1]
                    if m in ratings_for_user:
                        collected.append(ratings_for_user[m])

        uid += 1

    if len(collected) == 0:
        return None

    total = 0
    for r in collected:
        total += r
    return total / len(collected)



def genreRatingPrediction(u, m, movieList, rLu):
    if u < 1 or u > len(rLu):
        return None
    if m < 1 or m > len(movieList):
        return None

    target_genres = movieList[m - 1].get("genre", [])
    if len(target_genres) == 0:
        return None

    same_genre_ids = []

    midx = 1
    for movie in movieList:
        if not (midx != m):
            midx += 1
            continue

        genres = movie.get("genre", [])
        found_shared = False

        gi = 0
        limit = len(target_genres)
        if len(genres) < limit:
            limit = len(genres)

        while gi < limit:
            if target_genres[gi] == 1 and genres[gi] == 1:
                found_shared = True
                break
            gi += 1

        if found_shared:
            same_genre_ids.append(midx)

        midx += 1

    if len(same_genre_ids) == 0:
        return None

    user_ratings = rLu[u - 1]
    collected = []

    for movie_id in same_genre_ids:
        if movie_id in user_ratings:
            collected.append(user_ratings[movie_id])

    if len(collected) == 0:
        return None

    total = 0
    for r in collected:
        total += r
    return total / len(collected)



def partitionRatings(rawRatings, testPercent, seed=None):
    if seed is not None:
        random.seed(seed)

    total = len(rawRatings)
    k = int(round(total * testPercent / 100.0))

    indices = []
    i = 0
    while i < total:
        indices.append(i)
        i += 1

    random.shuffle(indices)

    test_set = set()
    j = 0
    while j < k:
        test_set.add(indices[j])
        j += 1

    train = []
    test = []

    idx = 0
    for tup in rawRatings:
        if idx in test_set:
            test.append(tup)
        else:
            train.append(tup)
        idx += 1

    return train, test



def rmse(actualRatings, predictedRatings):
    valid = []

    idx = 0
    while idx < len(actualRatings):
        a = actualRatings[idx]
        p = predictedRatings[idx]
        if p is not None:
            valid.append((a, p))
        idx += 1

    if len(valid) == 0:
        raise ValueError("No valid predictions")

    total = 0
    for (a, p) in valid:
        diff = a - p
        total += diff * diff

    return math.sqrt(total / len(valid))

import math


def sort_key_helper(item):

    return (-item[1], item[0])

def calculate_mean_rating(ratings_dict):
    total = 0.0
    count = 0
    
    for rating in ratings_dict.values():
        total = total + rating
        count = count + 1
    
    if count == 0:
        return 0.0
    
    return total / count




import math

def similarity(u, v, rLu):
    if u == v:
        return 1.0
    
    u_idx = u - 1
    v_idx = v - 1
    
    u_ratings = rLu[u_idx]
    v_ratings = rLu[v_idx]
    
    common_movies = []
    for movie_id in u_ratings.keys():
        if movie_id in v_ratings:
            common_movies.append(movie_id)
    
    if len(common_movies) == 0:
        return 0.0
    
    u_sum = 0.0
    u_count = 0
    for rating in u_ratings.values():
        u_sum += rating
        u_count += 1
    u_mean = u_sum / u_count
    
    v_sum = 0.0
    v_count = 0
    for rating in v_ratings.values():
        v_sum += rating
        v_count += 1
    v_mean = v_sum / v_count
    
    numerator = 0.0
    u_sum_sq = 0.0
    v_sum_sq = 0.0
    
    for m in common_movies:
        u_diff = u_ratings[m] - u_mean
        v_diff = v_ratings[m] - v_mean
        
        numerator += u_diff * v_diff
        u_sum_sq += u_diff * u_diff
        v_sum_sq += v_diff * v_diff
    
    if u_sum_sq == 0.0 or v_sum_sq == 0.0:
        return 0.0
    
    denominator = math.sqrt(u_sum_sq) * math.sqrt(v_sum_sq)
    
    if denominator == 0.0:
        return 0.0
    
    return numerator / denominator


def kNearestNeighbors(u, rLu, k):
    similarities = []
    num_users = len(rLu)
    
    for other_user in range(1, num_users + 1):
        if other_user != u:
            sim = similarity(u, other_user, rLu)
            similarities.append((other_user, sim))
    
    similarities.sort(key=lambda x: (-x[1], x[0]))
    
    return similarities[:int(k)]


def CFRatingPrediction(u, m, rLu, friends):
    u_idx = u - 1
    u_ratings = rLu[u_idx]
    
    if len(u_ratings) == 0:
        return None
    
    u_sum = 0.0
    u_count = 0
    for rating in u_ratings.values():
        u_sum += rating
        u_count += 1
    u_mean = u_sum / u_count
    
    numerator = 0.0
    denominator = 0.0
    
    for friend_id, sim_value in friends:
        friend_idx = friend_id - 1
        friend_ratings = rLu[friend_idx]
        
        if m in friend_ratings:
            f_sum = 0.0
            f_count = 0
            for rating in friend_ratings.values():
                f_sum += rating
                f_count += 1
            f_mean = f_sum / f_count
            
            numerator += (friend_ratings[m] - f_mean) * sim_value
            denominator += abs(sim_value)
    
    if denominator == 0.0:
        return u_mean
    
    return u_mean + (numerator / denominator)

ratings = readRatings()

NumUsers = 943
NumMovies = 1682

rLu, rLm = createRatingsDataStructure(NumUsers, NumMovies, ratings)

def run_one_trial_all_algos(userList, movieList, rawRatings, test_percent=20):
    trainSet, testSet = partitionRatings(rawRatings, test_percent)

    numUsers = len(userList)
    numMovies = len(movieList)
    trainingRLu, trainingRLm = createRatingsDataStructure(numUsers, numMovies, trainSet)

    actual = []
    pred_random = []
    pred_mean_user = []
    pred_mean_movie = []
    pred_dem = []
    pred_genre = []

    neighbors_full = [None] * (numUsers + 1)
    for u in range(1, numUsers + 1):
        nb = kNearestNeighbors(u, trainingRLu, numUsers - 1)
        neighbors_full[u] = nb

    cf_k10 = []
    cf_k100 = []
    cf_k500 = []
    cf_all = []

    for (u, m, r) in testSet:
        actual.append(r)

        pred_random.append(randomPrediction(u, m))
        pred_mean_user.append(meanUserRatingPrediction(u, m, trainingRLu))
        pred_mean_movie.append(meanMovieRatingPrediction(u, m, trainingRLm))
        pred_dem.append(demRatingPrediction(u, m, userList, trainingRLu))
        pred_genre.append(genreRatingPrediction(u, m, movieList, trainingRLu))

        nb = neighbors_full[u]

        top10 = nb[:10] if len(nb) >= 10 else nb[:]
        cf_k10.append(CFRatingPrediction(u, m, trainingRLu, top10))

        top100 = nb[:100] if len(nb) >= 100 else nb[:]
        cf_k100.append(CFRatingPrediction(u, m, trainingRLu, top100))

        top500 = nb[:500] if len(nb) >= 500 else nb[:]
        cf_k500.append(CFRatingPrediction(u, m, trainingRLu, top500))

        cf_all.append(CFRatingPrediction(u, m, trainingRLu, nb))

    return (
        rmse(actual, pred_random),
        rmse(actual, pred_mean_user),
        rmse(actual, pred_mean_movie),
        rmse(actual, pred_dem),
        rmse(actual, pred_genre),
        rmse(actual, cf_k10),
        rmse(actual, cf_k100),
        rmse(actual, cf_k500),
        rmse(actual, cf_all)
    )


def main():
    userList = createUserList()
    movieList = createMovieList()
    rawRatings = readRatings()

    alg_results = [[] for _ in range(9)]

    trials = 10
    for _ in range(trials):
        random.seed()
        rmses = run_one_trial_all_algos(userList, movieList, rawRatings, test_percent=20)
        for i, val in enumerate(rmses):
            alg_results[i].append(val)

    labels = [
        "Random",
        "MeanUser",
        "MeanMovie",
        "Demographic",
        "Genre",
        "CF k=10",
        "CF k=100",
        "CF k=500",
        "CF all"
    ]

    plt.figure(figsize=(12, 6))
    plt.boxplot(alg_results, patch_artist=True)
    plt.xticks(range(1, len(labels) + 1), labels, rotation=30)
    plt.title("Phase 3: RMSE Comparison (10 trials, 80/20 split)")
    plt.ylabel("RMSE (lower is better)")
    plt.tight_layout()

    plt.show()

    return {
        labels[i]: alg_results[i] for i in range(len(labels))
    }


if __name__ == "__main__":
    main()


