# Movie-Recommender
A Movie Recommendation System built using Streamlit and TMDB API. This project suggests movies based on a collaborative filtering approach and utilizes preprocessed PKL files for recommendations.

Features
    -Suggests similar movies based on user input
    -Uses collaborative filtering for recommendations
    -Built with Streamlit for an interactive UI
    -Utilizes TMDB API for fetching movie details
    -Preprocessed PKL files for efficient data handling

Installation

Prerequisites

Ensure you have Python 3.7+ installed.

Steps

Clone the repository:

git clone https://github.com/yourusername/Movie-Recommender.git
cd Movie-Recommender

Install dependencies:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run app.py

File Structure

Movie-Recommender/
│── app.py              # Main Streamlit app
│── test_api.py         # API testing script
│── requirements.txt    # Dependencies
│── similarity.pkl.gz   # Precomputed similarity matrix
│── movie_list.pkl.gz   # Preprocessed movie dataset
│── README.md           # Project documentation

Usage

Enter a movie name in the search bar.

The system will fetch similar movies using collaborative filtering.

Movie details such as posters and descriptions are fetched from TMDB API.

Screenshots

(Add relevant screenshots of the application UI here.)

Technologies Used

Python

Streamlit

TMDB API

Pandas

Numpy

Future Enhancements

Add content-based filtering

Improve UI/UX

Deploy on Streamlit Cloud / Heroku


