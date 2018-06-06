import datetime
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin,BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedShuffleSplit,cross_validate,cross_val_score

# custom transformer
class DenseTransformer(BaseEstimator,TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

def modeler(estimator):
    """
    Function creates pipeline to convert text
    to multidimensional array and fit to an 
    estimator of choice
    
    Parameters
    ---------
    
    estimator: scikit-learn object
        A scikit-learn object that corresponds to
        an estimator
    
    Returns
    -------
    
    scikit-learn pipeline
        Returns a new scikit-pipeline object
        with the new estimator appended to the
        end.
    """
    # make a pipeline for any estimator
    sklearn_pipe = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english',ngram_range=(1,1))),
        ('to_dense', DenseTransformer()),
        ('est',estimator)
                       ])
    return sklearn_pipe

def model_selection(estimator,X, y,num=5,size=.05,state=42):
    """
    Function to test scikit-learn evaluators on text
    dataset for classification.  
    
    Parameters
    ----------
    
    estimator : scikit-learn estimator
        A scikit-learn estimator; can use hyperparameters
        or just use with default settings
        
    X: pandas.Series, array, or list
        The features used for classification
        
    y: pandas.Series, array, or list
        The label used for testing
        
    num: integer
        Specifies the number of cross validation folds
    
    size: float
        Determines the test size left out to evaluate
        the model
    
    state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`. 
        
    
    """
    # set random state
    estimator.random_state = state
    
    # create pipeline
    model = modeler(estimator)
    
    # cross validation set up
    cv = StratifiedShuffleSplit(n_splits=num, test_size=size, random_state=state)
    
    # get the estimator name
    es_name = estimator.__class__.__name__
    
    # test if this is bayesian method which can't be multiprocessed
    if es_name in ['MultinomialNB','BernoulliNB','GaussianNB']:
        core_use = 1
    else:
        core_use = -1
    
    # set start time
    start = np.datetime64(datetime.datetime.now())
    
    # get scores
    scores = cross_val_score(model, X, y, cv=cv,n_jobs=core_use)
    
    # get the duration
    dur = np.timedelta64(np.datetime64(datetime.datetime.now())-start, 'ms')/num
    
    # get standard deviation
    var = np.std(scores)
    
    return es_name,np.float64(np.mean(scores)),var,dur