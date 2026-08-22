# Movie Recommendation System

A movie rating prediction and recommendation system built with Python using the MovieLens 100K dataset. The project progresses from exploratory data analysis to rating prediction and user-based collaborative filtering.

## Project Overview

This project explores movie ratings and develops multiple approaches for predicting how a user may rate a movie. The approaches range from simple baseline methods to collaborative filtering based on similarities between users.

The project is divided into three phases:

### Phase 1 — Exploratory Data Analysis

Phase 1 analyzes movie-rating patterns across demographic groups.

The analysis includes:

- Comparing high ratings (4–5) by gender
- Comparing low ratings (1–2) by gender
- Comparing high ratings by age group
- Comparing low ratings by age group
- Analyzing genre rating fractions
- Creating visualizations with Matplotlib

### Phase 2 — Rating Prediction

Phase 2 compares several methods for predicting movie ratings:

- Random prediction
- User-average prediction
- Movie-average prediction
- Demographic-based prediction
- Genre-based prediction

The methods are evaluated using:

- 80/20 training and testing splits
- 10 experimental trials
- Root Mean Squared Error (RMSE)

The results are visualized using box plots to compare prediction performance.

### Phase 3 — Collaborative Filtering

Phase 3 introduces user-based collaborative filtering.

The system:

1. Identifies movies that users have both rated.
2. Calculates similarity between users using their shared ratings.
3. Finds the nearest neighbors for each user.
4. Uses similar users to predict ratings.
5. Compares different numbers of neighbors.

The collaborative filtering approaches evaluated include:

- CF with 10 neighbors
- CF with 100 neighbors
- CF with 500 neighbors
- CF using all available neighbors

These approaches are compared against the baseline prediction methods using RMSE.

## Dataset

This project uses the **MovieLens 100K dataset**, which contains movie ratings along with user demographic information and movie genre information.

The project uses:

- `u.user` — user demographic information
- `u.item` — movie information and genre indicators
- `u.data` — user movie ratings
- `u.genre` — genre information

## Technologies

- Python
- NumPy
- Matplotlib
- Data Structures
- Exploratory Data Analysis
- Machine Learning
- Collaborative Filtering
- RMSE

## Project Structure

```text
movie-recommendation-system/
│
├── projectPhase1a.py
├── projectPhase1b.py
├── projectPhase2a.py
├── projectPhase2b.py
├── projectPhase3a.py
└── projectPhase3b.py

Phase 1 Files

projectPhase1a.py contains the data-processing and demographic/genre analysis functions.

projectPhase1b.py uses those functions to generate visual comparisons of rating patterns.

Phase 2 Files

projectPhase2a.py contains the rating prediction algorithms and RMSE evaluation functions.

projectPhase2b.py runs the prediction experiments and compares the different approaches.

Phase 3 Files

projectPhase3a.py contains the collaborative filtering functions, including user similarity, nearest-neighbor selection, and collaborative-filtering rating prediction.

projectPhase3b.py evaluates the baseline and collaborative filtering approaches across multiple trials.

Evaluation:
Model performance is evaluated using Root Mean Squared Error (RMSE).
A lower RMSE indicates that the predicted ratings are closer to the actual ratings.

The project compares the performance of nine approaches:
Random
User Average
Movie Average
Demographic Average
Genre Average
Collaborative Filtering — k=10
Collaborative Filtering — k=100
Collaborative Filtering — k=500
Collaborative Filtering — All Neighbors

What I Learned:

Through this project, I gained experience with:
Working with structured datasets
Building data structures for user and movie ratings
Exploratory data analysis
Data visualization
Rating prediction
Train/test evaluation
RMSE
User similarity
K-nearest neighbors
Collaborative filtering
Comparing multiple prediction approaches

## Results

The models were evaluated using Root Mean Squared Error (RMSE), where lower values indicate better prediction performance.

### Phase 2

The baseline methods produced RMSE values of approximately:

| Method | Approx. RMSE |
|---|---:|
| Random | 1.89 |
| User Average | 1.05 |
| Movie Average | 1.03 |
| Demographic Average | 1.07 |
| Genre Average | 1.04 |

Among the baseline methods, Movie Average produced the lowest RMSE.

### Phase 3

Collaborative filtering was then compared with the baseline methods using different numbers of nearest neighbors.

| Method | Approx. RMSE |
|---|---:|
| Random | 1.88 |
| Mean User | 1.04 |
| Mean Movie | 1.02 |
| Demographic | 1.06 |
| Genre | 1.03 |
| CF k=10 | 1.09 |
| CF k=100 | 1.07 |
| CF k=500 | 0.95 |
| CF all | 0.95 |

The best-performing approaches were collaborative filtering with 500 neighbors and collaborative filtering using all available neighbors. These approaches achieved an RMSE of approximately 0.95, outperforming the baseline methods tested in this project.
