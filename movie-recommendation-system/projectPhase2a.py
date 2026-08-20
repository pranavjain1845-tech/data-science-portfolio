def createUserList():
    userList = []
    with open("u.user", "r") as f:
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
    with open("u.item", "r", encoding="latin-1") as f:
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
    with open("u.data", "r") as f:
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
    with open("u.genre", "r") as f:
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


    