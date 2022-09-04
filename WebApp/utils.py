import numpy as np
import pandas as pd
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
import tensorflow as tf
import joblib



trainDf = pd.read_csv("../ML/train.csv")
cols2Drop = ["id", "locality", "activation_date"]

trainDf.drop(cols2Drop, axis=1, inplace=True)

trainDf_amenities = trainDf.pop("amenities")


catCols = trainDf.dtypes[trainDf.dtypes == 'object'].index
numCols = trainDf.dtypes[trainDf.dtypes != 'object'].index

amenitesCols = json.loads(trainDf_amenities.values[0]).keys()

for col in amenitesCols:
    trainDf[col] = trainDf_amenities.apply(lambda x: int(bool(json.loads(x).get(col))))

pca = PCA(n_components=1)
pca.fit(trainDf[amenitesCols])

trainDf["reducedAmenities"] = pca.transform(trainDf[amenitesCols]).reshape(-1, )

trainDf = trainDf[trainDf["property_size"]<5000]
trainDf = trainDf[trainDf["property_age"]<60]
trainDf = trainDf[trainDf["bathroom"]<7] 
trainDf = trainDf[trainDf["cup_board"]<25] 
trainDf = trainDf[trainDf["balconies"]<10] 

trainDf = trainDf[trainDf['property_age'] >0]

newCols = ["latitudeXlongitude",
           "totalSpace",
          "property_size/bathroom", "property_size/balconies", "property_size/cup_board",
          "total_floor/bathroom", "total_floor/balconies", "total_floor/cup_board",
          ]

# Features with lat and long
trainDf["latitudeXlongitude"] = trainDf.latitude * trainDf.longitude


# Total totalSpace in house
trainDf['totalSpace'] = trainDf.total_floor * trainDf.property_size


# Ratio of [bathroom, balconies, cup_board] with property_size
trainDf["property_size/bathroom"] = trainDf.property_size / trainDf.bathroom
trainDf["property_size/balconies"] = trainDf.property_size / trainDf.balconies
trainDf["property_size/cup_board"] = trainDf.property_size / trainDf.cup_board

# Ratio of [bathroom, balconies, cup_board] with total_floor
trainDf["total_floor/bathroom"] = trainDf.total_floor / trainDf.bathroom
trainDf["total_floor/balconies"] = trainDf.total_floor / trainDf.balconies
trainDf["total_floor/cup_board"] = trainDf.total_floor / trainDf.cup_board

cat2num = {}

for col in catCols:
    cat2num[f"{col}"] = {k: v+1 for v, k in enumerate(trainDf[col].unique())}

for col in catCols:
    trainDf[col].replace(cat2num[col], inplace=True)

trainDf.replace([np.inf, -np.inf], np.nan, inplace=True)
trainDf.fillna(0, inplace=True)

cols2Scale = newCols + ['latitude', 'longitude', 'property_size', 'property_age', 'cup_board', 'floor','total_floor']

scaler = RobustScaler()

scaler.fit(trainDf[cols2Scale])
trainDf[cols2Scale] = scaler.transform(trainDf[cols2Scale])



def preProcessDf(df):
    cols2Drop = ["id", "locality", "activation_date"]
    row_id = df["id"]
    df.drop(cols2Drop, axis=1, inplace=True)
    Df_amenities = df.pop("amenities")

    amenitesCols = json.loads(Df_amenities.values[0]).keys()

    for col in amenitesCols:
        df[col] = Df_amenities.apply(lambda x: int(bool(json.loads(x).get(col))))

    df["reducedAmenities"] = pca.transform(df[amenitesCols]).reshape(-1, )

    # Features with lat and long
    df["latitudeXlongitude"] = df.latitude * df.longitude

    # Total totalSpace in house
    df['totalSpace'] = df.total_floor * df.property_size

    # Ratio of [bathroom, balconies, cup_board] with property_size
    df["property_size/bathroom"] = df.property_size / df.bathroom
    df["property_size/balconies"] = df.property_size / df.balconies
    df["property_size/cup_board"] = df.property_size / df.cup_board

    # Ratio of [bathroom, balconies, cup_board] with total_floor
    df["total_floor/bathroom"] = df.total_floor / df.bathroom
    df["total_floor/balconies"] = df.total_floor / df.balconies
    df["total_floor/cup_board"] = df.total_floor / df.cup_board



    for col in catCols:
        df[col].replace(cat2num[col], inplace=True)

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    cols2Scale = newCols + ['latitude', 'longitude', 'property_size', 'property_age', 'cup_board', 'floor','total_floor']


    df[cols2Scale] = scaler.transform(df[cols2Scale])

    return df, row_id


def loadData(path):
    df = pd.read_csv(path)
    return df

def predict(df):
    preds = []

    BinModelPaths = ["../ML/models/regB.sav", "../ML/models/regET.sav", "../ML/models/regRF.sav", ]

    for i in range(1, 6):
        model = tf.keras.models.load_model(f"../ML/models/BestModel_{i}.h5")
        pred = model.predict(df).reshape(-1, )
        preds.append(pred)

    for i, path in enumerate(BinModelPaths):
        if i!=3:
            model = joblib.load(path)
        else:
            model = joblib.load(path)
            
        pred = model.predict(df)
        preds.append(pred)

    preds = np.stack(preds).T
    preds = preds.mean(axis=-1)
    return preds



from os import walk
import cv2
import pandas as pd
import numpy as np
from PIL import Image

from app import *

# Helper Constant and Function to Delete the Old Xray
ALLOWED_EXTENSIONS = set(['csv'])

def file_saver(filename):
    file = os.path.splitext(filename)
    if file[1] != '.csv':
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return str(file[0] + '.csv')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def erase_dir():
    f = next(walk('static/uploads/'), (None, None, []))[2]
    for ele in f:
        os.remove('static/uploads/'+ele)