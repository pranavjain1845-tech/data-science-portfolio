#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:09:08 2025

@author: pranavjain
"""
import matplotlib.pyplot as plt
import numpy as np
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

def graphData(title, group1, group2, action1, comedy1, drama1, horror1, romance1, action2, comedy2, drama2, horror2, romance2):
    genres = ("Action", "Comedy", "Drama", "Horror", "Romance")
    genreGroups = {
        group1: (action1, comedy1, drama1, horror1, romance1),
        group2: (action2, comedy2, drama2, horror2, romance2)
        }
    
    x = np.arange(len(genres))
    width = 0.25
    multiplier = 0
    
    fig, ax = plt.subplots(layout = "constrained")
    
    x_centered = x - width / 2
    
    for trait, measurement in genreGroups.items():
        offset = width * multiplier
        rects = ax.bar(x_centered + offset, measurement, width, label = trait)
        
        labels = [f'{m:.2f}' for m in measurement]
        
        ax.bar_label(rects, padding = 5, labels = labels, fontsize = 8, fontweight = "bold")
        
        multiplier += 1
        
    ax.set_ylabel("Fraction of Subpopulation's Total Ratings")
    ax.set_title(title)
    ax.set_xticks(x, genres)
    ax.legend(loc = "upper left", ncols = 5)
    ax.set_ylim(0, 0.45)
        
    plt.show()
        
def main():
    userList = createUserList()
    movieList = createMovieList()
    ratingTuples = readRatings()
    [rLu, rLm] = createRatingsDataStructure(len(userList), len(movieList), ratingTuples)
    
    #Plot No.1 - High Ratings by Gender
    graph1M = demGenreRatingFractions(userList, movieList, rLu, "M", [0, 100], [4,5])
    graph1F = demGenreRatingFractions(userList, movieList, rLu, "F", [0, 100], [4,5])
    
    graphData("Fraction of High Ratings (4 or 5) by Gender", "Men", "Women", graph1M[1],
               graph1M[5], graph1M[8], graph1M[11], graph1M[14], graph1F[1], graph1F[5],
               graph1F[8], graph1F[11], graph1F[14])
    
    #Plot No.2 - Low Ratings by Gender
    graph2M = demGenreRatingFractions(userList, movieList, rLu, "M", [0,100], [1,2])
    graph2F = demGenreRatingFractions(userList, movieList, rLu, "F", [0,100], [1,2])
    
    graphData("Fraction of Low Ratings (1 or 2) by Gender", "Men", "Women", graph2M[1],
                graph2M[5], graph2M[8], graph2M[11], graph2M[14], graph2F[1], graph2F[5],
                graph2F[8], graph2F[11], graph2F[14])
    
    #Plot No.3 - High Ratings by Age Group
    graph3Y = demGenreRatingFractions(userList, movieList, rLu, "A", [20,30], [4,5])
    graph3O = demGenreRatingFractions(userList, movieList, rLu, "A", [50,60], [4,5])
    
    graphData("Fraction of High Ratings (4 or 5) by Age Group", "Younger Adults (20-29)",
              "Older Adults (50-59)", graph3Y[1], graph3Y[5], graph3Y[8], graph3Y[11],
              graph3Y[14], graph3O[1], graph3O[5], graph3O[8], graph3O[11], graph3O[14])
    
    #Plot No.4 - Low Ratings by Age Group
    graph4Y = demGenreRatingFractions(userList, movieList, rLu, "A", [20,30], [1,2])
    graph4O = demGenreRatingFractions(userList, movieList, rLu, "A", [50,60], [1,2])
    
    graphData("Fraction of Low Ratings (1 or 2) by Age group", "Younger Adults(20-29)",
              "Older Adults (50-59)", graph4Y[1], graph4Y[5], graph4Y[8], graph4Y[11],
              graph4Y[14], graph4O[1], graph4O[5], graph4O[8], graph4O[11], graph4O[14])
    
    
              
              
