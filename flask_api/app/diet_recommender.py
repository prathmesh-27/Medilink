import pandas as pd
from sklearn.neighbors import NearestNeighbors

class Recommender:
    def __init__(self):
        self.df = pd.read_csv('flask_api\\app\\data\\dataset.csv') 
    
    def get_features(self):
        nutrient_dummies = self.df.Nutrient.str.get_dummies()
        disease_dummies = self.df.Disease.str.get_dummies(sep=' ')
        diet_dummies = self.df.Diet.str.get_dummies(sep=' ')
        feature_df = pd.concat([nutrient_dummies, disease_dummies, diet_dummies], axis=1)
        return feature_df
    
    def k_neighbor(self, inputs):
        feature_df = self.get_features()
        model = NearestNeighbors(n_neighbors=40, algorithm='ball_tree')
        model.fit(feature_df)
        df_results = pd.DataFrame(columns=list(self.df.columns))
        distances, indices = model.kneighbors(inputs)

        for i in list(indices):
            df_results = df_results._append(self.df.loc[i])
        
        df_results = df_results.filter(['Name', 'Nutrient','catagory','Veg_Non', 'Diet', 'Disease', 'description'])
        df_results = df_results.drop_duplicates(subset=['Name'])
        df_results = df_results.reset_index(drop=True)
        
        return df_results
