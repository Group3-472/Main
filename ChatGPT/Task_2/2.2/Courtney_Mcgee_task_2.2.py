import numpy as np

class LinearRegression:
    """
    Linear Regression model using gradient descent.

    Attributes:
    -----------
    lr : float
        Learning rate for gradient descent (default: 0.001).
    n_iters : int
        Number of iterations for gradient descent (default: 1000).
    weights : numpy array
        Coefficients/weights for the features, initialized during training.
    bias : float
        Bias term (intercept), initialized during training.
    """

    def __init__(self, lr=0.001, n_iters=1000) -> None:
        """
        Initializes the LinearRegression model with a learning rate and the number
        of iterations for gradient descent.

        Parameters:
        -----------
        lr : float, optional
            Learning rate for gradient descent (default is 0.001).
        n_iters : int, optional
            Number of iterations for gradient descent (default is 1000).
        """
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """
        Trains the LinearRegression model on the provided data using gradient descent.

        Parameters:
        -----------
        X : numpy array of shape (n_samples, n_features)
            Training data consisting of n_samples (number of data points) and n_features (number of features).
        y : numpy array of shape (n_samples,)
            Target values corresponding to each training data sample.
        
        Returns:
        --------
        None
        """
        # Get the number of samples and features from the input data
        n_samples, n_features = X.shape
        
        # Initialize weights as zeros and bias as 0
        self.weights = np.zeros(n_features)
        self.bias = 0

        # Perform gradient descent for the given number of iterations
        for _ in range(self.n_iters):
            # Predicted values using current weights and bias
            y_pred = np.dot(X, self.weights) + self.bias
            
            # Calculate gradients (derivatives) for weights and bias
            dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            db = (1/n_samples) * np.sum(y_pred - y)

            # Update weights and bias using the gradients and learning rate
            self.weights  = self.weights - self.lr * dw
            self.bias = self.bias - self.lr * db
    
    def predict(self, X):
        """
        Predicts target values for new input data using the trained model.

        Parameters:
        -----------
        X : numpy array of shape (n_samples, n_features)
            Input data for which to make predictions.
        
        Returns:
        --------
        y_pred : numpy array of shape (n_samples,)
            Predicted target values for the input data.
        """
        return np.dot(X, self.weights) + self.bias
