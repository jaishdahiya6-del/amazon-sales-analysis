import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NetflixRecommender:
    def __init__(self, dataframe):
        self.df = dataframe
        self.tfidf_matrix = None
        self.cosine_sim = None
        self._prepare_data()

    def _prepare_data(self):
        # Combining metadata for better context
        features = self.df['description'] + " " + self.df['listed_in'] + " " + self.df['cast']
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(features.fillna(''))
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend(self, title, top_n=5):
        try:
            idx = self.df[self.df['title'].str.lower() == title.lower()].index[0]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            indices = [i[0] for i in sim_scores[1:top_n+1]]
            return self.df['title'].iloc[indices].tolist()
        except IndexError:
            return ["Title not found in database."]

if __name__ == "__main__":
    # Test block
    data = pd.read_csv('cleaned_netflix_data.csv')
    engine = NetflixRecommender(data)
    print(f"Recommendations for 'Peaky Blinders': {engine.recommend('Peaky Blinders')}")
