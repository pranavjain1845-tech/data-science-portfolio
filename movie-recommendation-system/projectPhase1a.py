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


    

