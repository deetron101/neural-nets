import numpy as np
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

feature_set = np.array([[0,1,0],[0,0,1],[1,0,0],[1,1,0],[1,1,1]])
labels = np.array([[1,0,0,1,1]])
labels = labels.reshape(5,1)

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_der(x):
    return sigmoid(x)*(1-sigmoid(x))

def train():

    np.random.seed(42)
    global weights, bias, all_weights 
    weights = np.random.rand(3,1)
    bias = np.random.rand(1)
    lr = 0.05

    all_weights = [weights.flatten()]

    for epoch in range(500):
        inputs = feature_set

        # feedforward step1
        XW = np.dot(feature_set, weights) + bias

        #feedforward step2
        z = sigmoid(XW)

        # backpropagation step 1
        error = z - labels

        # backpropagation step 2
        dcost_dpred = error
        dpred_dz = sigmoid_der(z)

        z_delta = dcost_dpred * dpred_dz

        inputs = feature_set.T
        weights -= lr * np.dot(inputs, z_delta)

        for num in z_delta:
            bias -= lr * num
        
        #all_weights = np.insert(all_weights, 0, [weights.flatten()], axis=0)
        all_weights = np.append(all_weights, [weights.flatten()], axis=0)

def scale(X, x_min, x_max):
    nom = (X-X.min(axis=0))*(x_max-x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom==0] = 1
    return x_min + nom/denom 

def test():
    single_point = np.array([1,1,1])
    result = sigmoid(np.dot(single_point, weights) + bias)
    print(result)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/train")
def do_train():
    global all_weights
    train()
    all_weights = scale(all_weights, 0, 1)
    all_weights = np.round(all_weights, 2)
    #all_weights = np.transpose(all_weights)
    lists = all_weights.tolist()
    json_str = json.dumps(lists)
    return json_str