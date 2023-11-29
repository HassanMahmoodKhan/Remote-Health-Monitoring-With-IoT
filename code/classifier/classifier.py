import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time
import boto3
import csv


def read_csv(file_path):
    '''
    Method that reads the dataset from a csv file and converts it into a pandas dataframe.
    Additionally, it prints information about the dataframe.
    @param file_path: The string file path to the csv file
    returns a pandas dataframe
    '''
    # Load the dataset from a csv file
    df = pd.read_csv(file_path)
    print("Print dataframe information")
    print(df.head(5))
    print(df.info())
    return df

def preprocess(df):
    '''
    Takes a pandas dataframe, performs data preprocessing, feature standardization and one-hot encoding.
    Additionally, it performs label encoding on the label column for binary classification.
    @param df: A pandas dataframe that contains the model dataset
    returns Feature dataframe and label series
    '''

    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Labels

    # Perform one-hot encoding on the labels
    encoder = OneHotEncoder(sparse_output=False)

    # Extract the categorical feature
    categorical_feature = X[['fall_detected']]

    # Fit and transform the categorical feature
    onehot_encoded = encoder.fit_transform(categorical_feature)

    # Create a DataFrame with the one-hot encoded features
    onehot_df = pd.DataFrame(onehot_encoded, columns=encoder.get_feature_names_out(['fall_detected']))

    # Concatenate the one-hot encoded DataFrame with the original DataFrame
    X = pd.concat([X, onehot_df], axis=1)

    # Dropping the original categorical feature column
    X = X.drop(['fall_detected'], axis=1)

    # Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # LabelEncoder to convert string label to numerical values
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    return X, y

def train(X_train, y_train, model_path):
    '''
    Method that performs model training on the training dataset it is fed.
    Saves the model after training is complete for reuseability.
    @param X_train: The training feature set.
    @param y_train: The training label series.
    returns None
    '''
    # Create a logistic regression model
    model = LogisticRegression()

    # Train the model on the training data
    start_time = time.perf_counter()
    model.fit(X_train, y_train)
    end_time = time.perf_counter()

    print("Training complete!")
    print(f"Training time: {(end_time-start_time):.3f} sec")

    print("Saving model!")
    # Save the trained model to a file
    joblib.dump(model, model_path)

def predict(X_test, y_test, model_path):
    '''
    Method that performs inference on the testing set i.e., unseen data.
    Loads the trained model from file and computes accuracy for the predictions.
    @param X_test: The testing feature set.
    @param y_test: The testing label series. 
    '''
    # Load the saved model from a file
    loaded_model = joblib.load(model_path)

    # Make predictions on the test set
    y_pred = loaded_model.predict(X_test)

    # Calculate evaluation metrics
    eval_metrics = classification_report(y_test, y_pred)
    print(eval_metrics)

    cm = confusion_matrix(y_test, y_pred)

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Incident', 'No Incident'], yticklabels=['Incident', 'No Incident'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

def data_upload(data_file_path):
    """
    Method that uploads the data file to the Amazon S3 bucket instance using the personal keys.
    @param data_file_path: The path to the data file
    """
    # Set your AWS credentials
    AWS_ACCESS_KEY_ID = "sample_access_key"
    AWS_SECRET_ACCESS_KEY = "sample_secret_key"
    AWS_REGION = "sample_region"
    BUCKET_NAME = "sample_name"
    LOCAL_FILE_PATH = data_file_path   # Update with your local CSV file path
    S3_FILE_KEY = "IOT_test_data.csv"  # Update with the desired S3 object key

    # Upload the CSV file to S3
    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    s3.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_FILE_KEY)

    print(f"CSV file '{LOCAL_FILE_PATH}' uploaded to S3 bucket '{BUCKET_NAME}' with key '{S3_FILE_KEY}'.")

    # Download the CSV file from S3
    s3.download_file(BUCKET_NAME, S3_FILE_KEY, "downloaded_file.csv")

    # Read the downloaded CSV file
    with open("downloaded_file.csv", mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        i = 0
        for row in csv_reader:
            if i <=5:
                print(row)
            else:
                break
            i+=1

if __name__ == '__main__':

    data_file_path = 'test_data_2.csv' # Specify path to data csv file
    model_path = 'logistic_regression.joblib' # Specify path to weights file

    data = read_csv(data_file_path)
    X, y = preprocess(data)

    # Split the dataset into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # train(X_train, y_train, model_path) # Uncomment if you wish to retrain model
    predict(X_test, y_test, model_path)

    # data_upload(data_file_path)
