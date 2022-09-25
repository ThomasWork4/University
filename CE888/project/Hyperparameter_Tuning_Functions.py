from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression

random_grid = {'bootstrap': [True, False],
 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}


Model = RandomForestRegressor()
ModelTwo = LinearRegression()
def Optimize_RF(XTtrain, Ytrain, Weights="None", Model=Model, random_grid=random_grid):
        if Weights == "None":
                Optimizer = RandomizedSearchCV(estimator = Model, param_distributions = random_grid, n_iter = 100, cv = 10, verbose=2, n_jobs = -1)
                Optimizer.fit(XTtrain, Ytrain.flatten())
                return Optimizer.best_params_
        if Weights != "None":
                Optimizer = RandomizedSearchCV(estimator = Model, param_distributions = random_grid, n_iter = 100, cv = 10, verbose=2, n_jobs = -1)
                Optimizer.fit(XTtrain, Ytrain.flatten(), sample_weight=Weights)
                return Optimizer.best_params_
        
param_grid = {'fit_intercept': [True, False],
 'positive': [True, False]}

def Optimize_LR(XTtrain, Ytrain, Weights="None",ModelTwo=ModelTwo, param_grid=param_grid):
        if Weights == "None":
                Optimizer = GridSearchCV(estimator=ModelTwo, param_grid= param_grid, cv=10, verbose=2, n_jobs= -1)
                Optimizer.fit(XTtrain, Ytrain.flatten())
                return Optimizer.best_params_
        if Weights != "None":
                Optimizer = GridSearchCV(estimator=ModelTwo, param_grid= param_grid, cv=10, verbose=2, n_jobs= -1)
                Optimizer.fit(XTtrain, Ytrain.flatten(), sample_weight=Weights)
                return Optimizer.best_params_
