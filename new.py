{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "3d463b5a-75d2-438a-9ddb-846ec4dd559d",
   "metadata": {},
   "source": [
    "# ML INTERN at PRODIGY INFOTECH\n",
    "# Author: Viraj N. Bhutada\n",
    "\n",
    "# Task - 03 : Implement a support vector machine (SVM) to classify images of cats and dogs from the Kaggle dataset. \n",
    "\n",
    "In this project, I am implementing a Support Vector Machine (SVM) to categorize images of cats and dogs from the Kaggle dataset. By harnessing the SVM's proficiency in handling complex image data, the model discerns intricate patterns and features within the images. Through meticulous training and evaluation, the SVM accurately distinguishes between cats and dogs, showcasing its robustness in image classification tasks. This project serves as a testament to the SVM's effectiveness in real-world applications, making it a valuable tool for diverse image recognition challenges.\n",
    "\n",
    "Dataset: https://www.kaggle.com/c/dogs-vs-cats/data\n",
    "\n",
    "SVMs offer significant advantages in image classification due to their robust handling of high-dimensional data, such as images. Unlike neural networks and other algorithms, SVMs demonstrate a reduced tendency to overfit, enhancing their reliability in diverse datasets.\n",
    "\n",
    "In the realm of machine learning, model training relies on input data and corresponding expected output data. The process involves several essential phases:\n",
    "\n",
    "* **Import Necessary Libraries:** Begin by importing the essential libraries required for the task.\n",
    "\n",
    "* **Load Images and Convert to Dataframe:** Load images from the dataset and transform them into a structured dataframe format for processing.\n",
    "\n",
    "* **Separate Input Features and Targets:** Divide the data into input features and their corresponding target labels to prepare for model training.\n",
    "\n",
    "* **Split Train and Test Data:** Split the dataset into training and testing subsets, allocating a portion for training the model and another for evaluating its performance.\n",
    "\n",
    "* **Build and Train the Model:** Construct the Support Vector Machine (SVM) model and train it using the training data.\n",
    "\n",
    "* **Model Evaluation:** Assess the model's performance by evaluating its predictions against the test data, employing metrics like accuracy, precision, and recall.\n",
    "\n",
    "* **Prediction:** Utilize the trained model to make predictions on new, unseen data, enabling real-world applications of the image classification system.\n",
    "\n",
    "These phases collectively form the foundation for creating an effective image classification model using Support Vector Machines in machine learning."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "b78dd65d",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:12:42.332510Z",
     "iopub.status.busy": "2023-08-20T03:12:42.332140Z",
     "iopub.status.idle": "2023-08-20T03:12:53.148317Z",
     "shell.execute_reply": "2023-08-20T03:12:53.147076Z",
     "shell.execute_reply.started": "2023-08-20T03:12:42.332475Z"
    }
   },
   "outputs": [],
   "source": [
    "# extract dataset\n",
    "from zipfile import ZipFile\n",
    "\n",
    "dataset_train = \"train.zip\"\n",
    "    \n",
    "with ZipFile(dataset_train, 'r') as zip:\n",
    "    zip.extractall()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "c82c808c",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:12:53.150275Z",
     "iopub.status.busy": "2023-08-20T03:12:53.150012Z",
     "iopub.status.idle": "2023-08-20T03:12:54.262650Z",
     "shell.execute_reply": "2023-08-20T03:12:54.261537Z",
     "shell.execute_reply.started": "2023-08-20T03:12:53.150252Z"
    }
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/opt/conda/lib/python3.10/site-packages/scipy/__init__.py:146: UserWarning: A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy (detected version 1.23.5\n",
      "  warnings.warn(f\"A NumPy version >={np_minversion} and <{np_maxversion}\"\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "from sklearn.svm import SVC\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "import matplotlib.pyplot as plt\n",
    "from tqdm import tqdm\n",
    "import joblib\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "import cv2\n",
    "import seaborn as sns\n",
    "import time\n",
    "from sklearn.decomposition import PCA\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.model_selection import train_test_split"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "a05d4ec3",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:12:54.265648Z",
     "iopub.status.busy": "2023-08-20T03:12:54.264707Z",
     "iopub.status.idle": "2023-08-20T03:12:54.272046Z",
     "shell.execute_reply": "2023-08-20T03:12:54.270860Z",
     "shell.execute_reply.started": "2023-08-20T03:12:54.265621Z"
    }
   },
   "outputs": [],
   "source": [
    "folder_path = f\"Dataset/\"\n",
    "os.makedirs(folder_path, exist_ok=True)\n",
    "\n",
    "# define path\n",
    "confusion_image_path = os.path.join(folder_path, 'confusion matrix.png')\n",
    "classification_file_path = os.path.join(folder_path, 'classification_report.txt')\n",
    "model_file_path = os.path.join(folder_path, \"svm_model.pkl\")\n",
    "\n",
    "# Path dataset\n",
    "dataset_dir = \"Dataset/\"\n",
    "train_dir = os.path.join(dataset_dir, \"train\")\n",
    "test_dir = os.path.join(dataset_dir, \"test1\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "8335a27a",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:12:54.274789Z",
     "iopub.status.busy": "2023-08-20T03:12:54.274491Z",
     "iopub.status.idle": "2023-08-20T03:13:37.706207Z",
     "shell.execute_reply": "2023-08-20T03:13:37.704830Z",
     "shell.execute_reply.started": "2023-08-20T03:12:54.274764Z"
    }
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Processing Train Images: 100%|██████████| 25000/25000 [00:43<00:00, 575.99it/s]\n"
     ]
    }
   ],
   "source": [
    "# load data, preprocessing data, and labeling\n",
    "# dog = 1, cat = 0\n",
    "train_images = os.listdir(train_dir)\n",
    "features = []\n",
    "labels = []\n",
    "image_size = (50, 50)\n",
    "\n",
    "# Proses train images\n",
    "for image in tqdm(train_images, desc=\"Processing Train Images\"):\n",
    "    if image[0:3] == 'cat' :\n",
    "        label = 0\n",
    "    else :\n",
    "        label = 1\n",
    "    image_read = cv2.imread(train_dir+\"/\"+image)\n",
    "    image_resized = cv2.resize(image_read, image_size)\n",
    "    image_normalized = image_resized / 255.0\n",
    "    image_flatten = image_normalized.flatten()\n",
    "    features.append(image_flatten)\n",
    "    labels.append(label)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "054b7066",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:13:37.708409Z",
     "iopub.status.busy": "2023-08-20T03:13:37.707687Z",
     "iopub.status.idle": "2023-08-20T03:13:37.713697Z",
     "shell.execute_reply": "2023-08-20T03:13:37.712263Z",
     "shell.execute_reply.started": "2023-08-20T03:13:37.708378Z"
    }
   },
   "outputs": [],
   "source": [
    "del train_images"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "a646d9a0",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:13:37.715013Z",
     "iopub.status.busy": "2023-08-20T03:13:37.714768Z",
     "iopub.status.idle": "2023-08-20T03:13:38.099819Z",
     "shell.execute_reply": "2023-08-20T03:13:38.099179Z",
     "shell.execute_reply.started": "2023-08-20T03:13:37.714989Z"
    }
   },
   "outputs": [],
   "source": [
    "features = np.asarray(features)\n",
    "labels = np.asarray(labels)\n",
    "\n",
    "# train test split\n",
    "X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, shuffle=True, random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "44762227",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:13:38.101147Z",
     "iopub.status.busy": "2023-08-20T03:13:38.100790Z",
     "iopub.status.idle": "2023-08-20T03:13:38.106441Z",
     "shell.execute_reply": "2023-08-20T03:13:38.105829Z",
     "shell.execute_reply.started": "2023-08-20T03:13:38.101126Z"
    }
   },
   "outputs": [],
   "source": [
    "del features\n",
    "del labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "fd8f10c8",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:13:38.107720Z",
     "iopub.status.busy": "2023-08-20T03:13:38.107355Z",
     "iopub.status.idle": "2023-08-20T03:13:38.120180Z",
     "shell.execute_reply": "2023-08-20T03:13:38.119086Z",
     "shell.execute_reply.started": "2023-08-20T03:13:38.107700Z"
    }
   },
   "outputs": [],
   "source": [
    "# PCA, SVM, & Pipeline\n",
    "n_components = 0.8\n",
    "pca = PCA(n_components=n_components)\n",
    "svm = SVC()\n",
    "pca = PCA(n_components=n_components, random_state=42)\n",
    "pipeline = Pipeline([\n",
    "    ('pca', pca),\n",
    "    ('svm', svm)\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "d8d3d9ff",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:13:38.121825Z",
     "iopub.status.busy": "2023-08-20T03:13:38.121564Z",
     "iopub.status.idle": "2023-08-20T03:13:38.135062Z",
     "shell.execute_reply": "2023-08-20T03:13:38.134296Z",
     "shell.execute_reply.started": "2023-08-20T03:13:38.121805Z"
    }
   },
   "outputs": [],
   "source": [
    "param_grid = {\n",
    "    'pca__n_components': [2, 1, 0.9, 0.8],\n",
    "    'svm__kernel': ['linear', 'rbf', 'poly', 'sigmoid'],\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "3f6fadca",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T03:13:38.138198Z",
     "iopub.status.busy": "2023-08-20T03:13:38.137408Z",
     "iopub.status.idle": "2023-08-20T05:35:44.898617Z",
     "shell.execute_reply": "2023-08-20T05:35:44.895939Z",
     "shell.execute_reply.started": "2023-08-20T03:13:38.138174Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fitting 3 folds for each of 16 candidates, totalling 48 fits\n",
      "[CV 1/3] END pca__n_components=2, svm__kernel=linear;, score=0.527 total time=  16.8s\n",
      "[CV 2/3] END pca__n_components=2, svm__kernel=linear;, score=0.533 total time=  15.6s\n",
      "[CV 3/3] END pca__n_components=2, svm__kernel=linear;, score=0.530 total time=  16.2s\n",
      "[CV 1/3] END pca__n_components=2, svm__kernel=rbf;, score=0.566 total time=  12.9s\n",
      "[CV 2/3] END pca__n_components=2, svm__kernel=rbf;, score=0.573 total time=  12.8s\n",
      "[CV 3/3] END pca__n_components=2, svm__kernel=rbf;, score=0.565 total time=  12.6s\n",
      "[CV 1/3] END pca__n_components=2, svm__kernel=poly;, score=0.496 total time=  11.2s\n",
      "[CV 2/3] END pca__n_components=2, svm__kernel=poly;, score=0.512 total time=  11.3s\n",
      "[CV 3/3] END pca__n_components=2, svm__kernel=poly;, score=0.496 total time=  11.2s\n",
      "[CV 1/3] END pca__n_components=2, svm__kernel=sigmoid;, score=0.501 total time=  13.1s\n",
      "[CV 2/3] END pca__n_components=2, svm__kernel=sigmoid;, score=0.509 total time=  12.0s\n",
      "[CV 3/3] END pca__n_components=2, svm__kernel=sigmoid;, score=0.498 total time=  14.0s\n",
      "[CV 1/3] END pca__n_components=1, svm__kernel=linear;, score=0.519 total time=  12.1s\n",
      "[CV 2/3] END pca__n_components=1, svm__kernel=linear;, score=0.518 total time=  11.3s\n",
      "[CV 3/3] END pca__n_components=1, svm__kernel=linear;, score=0.514 total time=  11.8s\n",
      "[CV 1/3] END pca__n_components=1, svm__kernel=rbf;, score=0.531 total time=  12.8s\n",
      "[CV 2/3] END pca__n_components=1, svm__kernel=rbf;, score=0.530 total time=  12.6s\n",
      "[CV 3/3] END pca__n_components=1, svm__kernel=rbf;, score=0.532 total time=  13.3s\n",
      "[CV 1/3] END pca__n_components=1, svm__kernel=poly;, score=0.499 total time=  10.7s\n",
      "[CV 2/3] END pca__n_components=1, svm__kernel=poly;, score=0.503 total time=  10.1s\n",
      "[CV 3/3] END pca__n_components=1, svm__kernel=poly;, score=0.499 total time=  10.7s\n",
      "[CV 1/3] END pca__n_components=1, svm__kernel=sigmoid;, score=0.506 total time=  11.3s\n",
      "[CV 2/3] END pca__n_components=1, svm__kernel=sigmoid;, score=0.507 total time=  11.1s\n",
      "[CV 3/3] END pca__n_components=1, svm__kernel=sigmoid;, score=0.506 total time=  11.2s\n",
      "[CV 1/3] END pca__n_components=0.9, svm__kernel=linear;, score=0.608 total time=14.6min\n",
      "[CV 2/3] END pca__n_components=0.9, svm__kernel=linear;, score=0.606 total time=14.6min\n",
      "[CV 3/3] END pca__n_components=0.9, svm__kernel=linear;, score=0.605 total time=17.6min\n",
      "[CV 1/3] END pca__n_components=0.9, svm__kernel=rbf;, score=0.674 total time= 4.4min\n",
      "[CV 2/3] END pca__n_components=0.9, svm__kernel=rbf;, score=0.680 total time= 4.4min\n",
      "[CV 3/3] END pca__n_components=0.9, svm__kernel=rbf;, score=0.673 total time= 4.3min\n",
      "[CV 1/3] END pca__n_components=0.9, svm__kernel=poly;, score=0.606 total time= 4.4min\n",
      "[CV 2/3] END pca__n_components=0.9, svm__kernel=poly;, score=0.610 total time= 4.6min\n",
      "[CV 3/3] END pca__n_components=0.9, svm__kernel=poly;, score=0.605 total time= 4.5min\n",
      "[CV 1/3] END pca__n_components=0.9, svm__kernel=sigmoid;, score=0.521 total time= 3.8min\n",
      "[CV 2/3] END pca__n_components=0.9, svm__kernel=sigmoid;, score=0.516 total time= 3.8min\n",
      "[CV 3/3] END pca__n_components=0.9, svm__kernel=sigmoid;, score=0.521 total time= 3.9min\n",
      "[CV 1/3] END pca__n_components=0.8, svm__kernel=linear;, score=0.587 total time= 5.5min\n",
      "[CV 2/3] END pca__n_components=0.8, svm__kernel=linear;, score=0.587 total time= 5.3min\n",
      "[CV 3/3] END pca__n_components=0.8, svm__kernel=linear;, score=0.589 total time= 5.2min\n",
      "[CV 1/3] END pca__n_components=0.8, svm__kernel=rbf;, score=0.663 total time= 3.5min\n",
      "[CV 2/3] END pca__n_components=0.8, svm__kernel=rbf;, score=0.668 total time= 3.5min\n",
      "[CV 3/3] END pca__n_components=0.8, svm__kernel=rbf;, score=0.659 total time= 3.4min\n",
      "[CV 1/3] END pca__n_components=0.8, svm__kernel=poly;, score=0.597 total time= 3.4min\n",
      "[CV 2/3] END pca__n_components=0.8, svm__kernel=poly;, score=0.606 total time= 3.4min\n",
      "[CV 3/3] END pca__n_components=0.8, svm__kernel=poly;, score=0.592 total time= 3.4min\n",
      "[CV 1/3] END pca__n_components=0.8, svm__kernel=sigmoid;, score=0.517 total time= 3.4min\n",
      "[CV 2/3] END pca__n_components=0.8, svm__kernel=sigmoid;, score=0.516 total time= 3.4min\n",
      "[CV 3/3] END pca__n_components=0.8, svm__kernel=sigmoid;, score=0.520 total time= 3.3min\n"
     ]
    }
   ],
   "source": [
    "# Hitung waktu training\n",
    "start_time = time.time()\n",
    "\n",
    "grid_search = GridSearchCV(pipeline, param_grid, cv=3, verbose=4)\n",
    "grid_search.fit(X_train, y_train)\n",
    "\n",
    "# Hitung waktu training\n",
    "end_time = time.time()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "738e3df2",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T05:35:44.902750Z",
     "iopub.status.busy": "2023-08-20T05:35:44.902002Z",
     "iopub.status.idle": "2023-08-20T05:35:44.909483Z",
     "shell.execute_reply": "2023-08-20T05:35:44.908111Z",
     "shell.execute_reply.started": "2023-08-20T05:35:44.902677Z"
    }
   },
   "outputs": [],
   "source": [
    "del X_train\n",
    "del y_train"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "75a48001",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T05:35:44.911881Z",
     "iopub.status.busy": "2023-08-20T05:35:44.911457Z",
     "iopub.status.idle": "2023-08-20T05:35:44.934019Z",
     "shell.execute_reply": "2023-08-20T05:35:44.933144Z",
     "shell.execute_reply.started": "2023-08-20T05:35:44.911834Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Best Parameters:  {'pca__n_components': 0.9, 'svm__kernel': 'rbf'}\n",
      "Best Score:  0.6756998783724181\n"
     ]
    }
   ],
   "source": [
    "# Mendapatkan model terbaik dan parameter terbaik\n",
    "best_pipeline = grid_search.best_estimator_\n",
    "best_params = grid_search.best_params_\n",
    "best_score = grid_search.best_score_\n",
    "\n",
    "print(\"Best Parameters: \", best_params)\n",
    "print(\"Best Score: \", best_score)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "468935fc",
   "metadata": {},
   "source": [
    "The grid search identified the best SVM model configuration: using 90% of principal components and the Radial Basis Function (RBF) kernel. This setup yielded an accuracy score of approximately 67.57%, demonstrating the effectiveness of these parameters in accurately classifying cats and dogs images."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "c595d007",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T05:35:44.935898Z",
     "iopub.status.busy": "2023-08-20T05:35:44.935546Z",
     "iopub.status.idle": "2023-08-20T05:36:10.189333Z",
     "shell.execute_reply": "2023-08-20T05:36:10.187937Z",
     "shell.execute_reply.started": "2023-08-20T05:35:44.935876Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.6762\n"
     ]
    }
   ],
   "source": [
    "# Evaluation on test dataset\n",
    "accuracy = best_pipeline.score(X_test, y_test)\n",
    "print(\"Accuracy:\", accuracy)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "782958de",
   "metadata": {},
   "source": [
    "The model attained an accuracy score of approximately 67.62%, indicating its ability to correctly classify images of cats and dogs from the Kaggle dataset. This accuracy score reflects the proportion of correctly predicted classifications out of the total dataset, showcasing the model's overall performance."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "06ca62aa",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T05:36:10.271224Z",
     "iopub.status.busy": "2023-08-20T05:36:10.270011Z",
     "iopub.status.idle": "2023-08-20T05:36:35.388213Z",
     "shell.execute_reply": "2023-08-20T05:36:35.386304Z",
     "shell.execute_reply.started": "2023-08-20T05:36:10.271169Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Classification Report:\n",
      "               precision    recall  f1-score   support\n",
      "\n",
      "         Cat       0.68      0.69      0.68      2529\n",
      "         Dog       0.68      0.66      0.67      2471\n",
      "\n",
      "    accuracy                           0.68      5000\n",
      "   macro avg       0.68      0.68      0.68      5000\n",
      "weighted avg       0.68      0.68      0.68      5000\n",
      "\n"
     ]
    }
   ],
   "source": [
    "y_pred = best_pipeline.predict(X_test)\n",
    "\n",
    "# classification report\n",
    "target_names = ['Cat', 'Dog']\n",
    "classification_rep = classification_report(y_test, y_pred, target_names=target_names)\n",
    "print(\"Classification Report:\\n\", classification_rep)\n",
    "\n",
    "with open(classification_file_path, 'w') as file:\n",
    "    file.write(classification_rep)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d72578b8",
   "metadata": {},
   "source": [
    "In the classification report, the model achieved an overall accuracy of 68% in distinguishing between cats and dogs. With precision and recall scores around 68%, it demonstrates consistent performance in identifying both classes. The F1-score, a balanced measure of precision and recall, also hovers around 68%, indicating a well-rounded classification capability for this SVM model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "fd521141",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T05:36:35.390696Z",
     "iopub.status.busy": "2023-08-20T05:36:35.389881Z",
     "iopub.status.idle": "2023-08-20T05:36:35.731365Z",
     "shell.execute_reply": "2023-08-20T05:36:35.730095Z",
     "shell.execute_reply.started": "2023-08-20T05:36:35.390664Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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s7NdbSqCKRsAAExm1ZNac3JydOTIEdfrjIwMpaWlKTg4WBEREapVq5Zbez8/P4WFhbl2xtjtdo0ePVpTpkxRrVq1FBwcrKlTp6p169auXTfNmzfXgAEDNHbsWC1btkySNG7cOMXExFR4h41EIAEAoNLas2eP+vTp43r944LYUaNGKTExsUJ9LFy4UL6+vho2bJjy8/N1xx13KDExUVWqVHG1WbFihSZNmuTajTN48GDDZ5/8lM3pdDo9escNILD9o1YPAbguZe327D8QwC9BwDX4X/M7luzwSj8fTozySj/XIyokAACYzIcf1zPEolYAAGA5KiQAAJiMAokxAgkAACazapfNjYRAAgCAyXzII4ZYQwIAACxHhQQAAJMxZWOMQAIAgMnII8aYsgEAAJb72YGkpKREaWlpZX4JEAAAXGLz0j+VmceBJC4uTq+++qqkS2GkV69e6tChg8LDw7VlyxZvjw8AgBuej807R2XmcSBZvXq12rZtK0lav369MjIydPDgQcXFxWnWrFleHyAAAKj8PA4k3333ncLCwiRJGzdu1H333acmTZpo9OjR+uKLL7w+QAAAbnQ2m80rR2XmcSAJDQ3VV199pZKSEiUnJ6tv376SpLy8PLefIgYAAJfYbN45KjOPt/0+9NBDGjZsmOrWrSubzaZ+/fpJknbu3KlmzZp5fYAAAKDy8ziQzJkzR61atdKJEyd03333yd/fX5JUpUoVPfHEE14fIAAANzqfyl7e8IKrejDavffeW+bcqFGjfvZgAACojMgjxioUSBYvXlzhDidNmnTVgwEAoDKq7AtSvaFCgWThwoUV6sxmsxFIAACAxyoUSDIyMsweBwAAlRYFEmNX/ej4wsJCHTp0SMXFxd4cDwAAlY6PzeaVozLzOJDk5eVp9OjRqlatmlq2bKnjx49LurR25Nlnn/X6AAEAQOXncSCZOXOm9u/fry1btiggIMB1vm/fvnrrrbe8OjgAACoDm5eOyszjbb9r167VW2+9pa5du7qtGm7RooW++eYbrw4OAIDKgF02xjyukJw7d04hISFlzufm5vKFAwCAq+JxIOnUqZPeffdd1+sfQ8jy5csVFRXlvZEBAFBJ+Ni8c1RmHk/ZxMfHa8CAAfrqq69UXFysF198UV9++aV27NihTz75xIwxAgBwQ2MGwZjHFZJu3brps88+U15enm65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1KZNm9zOb9q0Sd26dbNoVACA65mv1QNA5TR58mTFxsaqY8eOioqK0t/+9jcdP35c48ePt3pogGVycnJ05MgR1+uMjAylpaUpODhYERERFo4MsB7bfmGal156Sc8995xOnz6tVq1aaeHCherZs6fVwwIss2XLFvXp06fM+VGjRikxMfHaDwi4jhBIAACA5VhDAgAALEcgAQAAliOQAAAAyxFIAACA5QgkAADAcgQSAABgOQIJAACwHIEEAABYjkACWGjOnDlq166d6/WDDz6ooUOHXvNxHD16VDabTWlpaZdt06BBAy1atKjCfSYmJqpGjRo/e2w2m01r16792f0AuL4RSICfePDBB2Wz2WSz2eTn56dGjRpp6tSpys3NNf2zX3zxxQo/QrwiIQIAbhT8uB5QjgEDBui1115TUVGRPv30U40ZM0a5ubl6+eWXy7QtKiqSn5+fVz7Xbrd7pR8AuNFQIQHK4e/vr7CwMIWHh2vkyJG6//77XdMGP06z/P3vf1ejRo3k7+8vp9Op7OxsjRs3TiEhIapevbpuv/127d+/363fZ599VqGhobr55ps1evRoXbx40e36T6dsSktLNX/+fN16663y9/dXRESEnnnmGUlSw4YNJUnt27eXzWZT7969Xe977bXX1Lx5cwUEBKhZs2Z66aWX3D5n165dat++vQICAtSxY0ft27fP4+9owYIFat26tYKCghQeHq4JEyYoJyenTLu1a9eqSZMmCggIUL9+/XTixAm36+vXr1dkZKQCAgLUqFEjzZ07V8XFxeV+ZmFhoR599FHVrVtXAQEBatCggeLj4z0eO4DrDxUSoAICAwNVVFTken3kyBGtWrVKb7/9tqpUqSJJuuuuuxQcHKyNGzfKbrdr2bJluuOOO3T48GEFBwdr1apVmj17tv7617+qR48eSkpK0uLFi9WoUaPLfu7MmTO1fPlyLVy4UN27d9fp06d18OBBSZdCRefOnbV582a1bNlSVatWlSQtX75cs2fPVkJCgtq3b699+/Zp7NixCgoK0qhRo5Sbm6uYmBjdfvvteuONN5SRkaHHHnvM4+/Ex8dHixcvVoMGDZSRkaEJEyZo+vTpbuEnLy9PzzzzjF5//XVVrVpVEyZM0IgRI/TZZ59Jkt5//3399re/1eLFi9WjRw998803GjdunCRp9uzZZT5z8eLFWrdunVatWqWIiAidOHGiTMABcINyAnAzatQo55AhQ1yvd+7c6axVq5Zz2LBhTqfT6Zw9e7bTz8/PefbsWVebDz/80Fm9enXnxYsX3fq65ZZbnMuWLXM6nU5nVFSUc/z48W7Xu3Tp4mzbtm25n33hwgWnv7+/c/ny5eWOMyMjwynJuW/fPrfz4eHhzjfffNPt3J/+9CdnVFSU0+l0OpctW+YMDg525ubmuq6//PLL5fb1v+rXr+9cuHDhZa+vWrXKWatWLdfr1157zSnJmZKS4jqXnp7ulOTcuXOn0+l0Onv06OGcN2+eWz9JSUnOunXrul5Lcq5Zs8bpdDqdEydOdN5+++3O0tLSy44DwI2JCglQjg0bNuimm25ScXGxioqKNGTIEC1ZssR1vX79+qpTp47rdWpqqnJyclSrVi23fvLz8/XNN99IktLT0zV+/Hi361FRUfr444/LHUN6eroKCgp0xx13VHjc586d04kTJzR69GiNHTvWdb64uNi1PiU9PV1t27ZVtWrV3MbhqY8//ljz5s3TV199pQsXLqi4uFgXL15Ubm6ugoKCJEm+vr7q2LGj6z3NmjVTjRo1lJ6ers6dOys1NVW7d+92TUNJUklJiS5evKi8vDy3MUqXprT69eunpk2basCAAYqJiVH//v09HjuA6w+BBChHnz599PLLL8vPz08Oh6PMotUf/+D+qLS0VHXr1tWWLVvK9HW1W18DAwM9fk9paamkS9M2Xbp0cbv249SS0+m8qvH8r2PHjunOO+/U+PHj9ac//UnBwcHatm2bRo8e7Ta1JV3atvtTP54rLS3V3Llzdc8995RpExAQUOZchw4dlJGRoffee0+bN2/WsGHD1LdvX61evfpn3xMAaxFIgHIEBQXp1ltvrXD7Dh06KDMzU76+vmrQoEG5bZo3b66UlBQ98MADrnMpKSmX7bNx48YKDAzUhx9+qDFjxpS5/uOakZKSEte50NBQ1atXT//5z390//33l9tvixYtlJSUpPz8fFfoudI4yrNnzx4VFxfrhRdekI/PpbXxq1atKtOuuLhYe/bsUefOnSVJhw4d0vnz59WsWTNJl763Q4cOefRdV69eXcOHD9fw4cN17733asCAAfr+++8VHBzs0T0AuL4QSAAv6Nu3r6KiojR06FDNnz9fTZs21alTp7Rx40YNHTpUHTt21GOPPaZRo0apY8eO6t69u1asWKEvv/zysotaAwICNGPGDE2fPl1Vq1bVbbfdpnPnzunLL7/U6NGjFRISosDAQCUnJ+tXv/qVAgICZLfbNWfOHE2aNEnVq1fXwIEDVVBQoD179igrK0uTJ0/WyJEjNWvWLI0ePVp//OMfdfToUT3//PMe3e8tt9yi4uJiLVmyRIMGDdJnn32mpUuXlmnn5+eniRMnavHixfLz89Ojjz6qrl27ugLKU089pZiYGIWHh+u+++6Tj4+PPv/8c33xxRf685//XKa/hQsXqm7dumrXrp18fHz0r3/9S2FhYV55ABsAa7HtF/ACm82mjRs3qmfPnnr44YfVpEkTjRgxQkePHlVoaKgkafjw4Xrqqac0Y8YMRUZG6tixY/rd7353xX6ffPJJTZkyRU899ZSaN2+u4cOH6+zZs5Iurc9YvHixli1bJofDoSFDhkiSxowZo1deeUWJiYlq3bq1evXqpcTERNc24Ztuuknr16/XV199pfbt22vWrFmaP3++R/fbrl07LViwQPPnz1erVq20YsWKcrffVqtWTTNmzNDIkSMVFRWlwMBArVy50nU9OjpaGzZs0KZNm9SpUyd17dpVCxYsUP369cv93Jtuuknz589Xx44d1alTJx09elQbN250VWkA3LhsTm9MKAMAAPwM/G8FAACwHIEEAABYjkACAAAsRyABAACWI5AAAADLEUgAAIDlCCQAAMByBBIAAGA5AgkAALAcgQQAAFiOQAIAACz3/wARL/LSzeKOqQAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 640x480 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Confusion matrix\n",
    "cm = confusion_matrix(y_test, y_pred)\n",
    "sns.heatmap(cm, annot=True, fmt=\"d\", cmap=\"Blues\")\n",
    "plt.xlabel('Predicted labels')\n",
    "plt.ylabel('True labels')\n",
    "plt.savefig(confusion_image_path)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fc14e280",
   "metadata": {},
   "source": [
    "In summary, the SVM model accurately classified Kaggle dataset images of cats and dogs. The confusion matrix visualized its performance, revealing precise predictions for both classes. This underscores the SVM's effectiveness in image classification, emphasizing the need for robust evaluation tools. This success paves the way for future improvements and applications in real-world scenarios requiring precise image recognition."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "40fb89d1",
   "metadata": {},
   "source": [
    "* Conclusion, the successful optimization of the Support Vector Machine (SVM) model highlights the importance of parameter tuning and feature selection in enhancing image classification accuracy. By leveraging 90% of principal components and the RBF kernel, the model achieved a commendable accuracy of approximately 67.57%. This accomplishment not only underscores the effectiveness of SVMs in image classification tasks but also emphasizes the significance of fine-tuning for maximizing predictive capabilities. This knowledge paves the way for improved algorithms and applications in the realm of computer vision."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}