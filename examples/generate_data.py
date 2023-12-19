import cv2
import numpy as np
import os
import pandas as pd
import shutil
from io import StringIO



def reset_fake_data():
    DIR = os.path.join(os.path.dirname(__file__), 'fake_data')
    if os.path.isdir(DIR):
        shutil.rmtree(DIR)
    os.mkdir(DIR)

    ANIMALS_DIR = os.path.join(DIR, "animals")
    ANIMALS_LABELED_DIR = os.path.join(DIR, "labeled_animals")
    os.mkdir(ANIMALS_DIR)
    os.mkdir(ANIMALS_LABELED_DIR)
    os.mkdir(os.path.join(ANIMALS_LABELED_DIR, 'cat'))
    os.mkdir(os.path.join(ANIMALS_LABELED_DIR, 'dog'))

    labels = pd.DataFrame({
    'id': ['1', '2', '3', '4', 'random5text', '6', 
                    '7', '8', '9', '10', '11', '12'],
    'label': ['cat', 'cat', 'dog', 'dog', 'cat', 'dog', 
              'dog', 'dog', 'cat', 'cat', 'dog', 'dog']
    })

    labels.to_excel(os.path.join(ANIMALS_DIR, 'labels.xlsx'), index=False)

    dog_array = np.array([
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    ], dtype=np.uint8)*255

    cat_array = np.array([
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    ], dtype=np.uint8)*255

    for i in range(len(labels.to_numpy())):
        if labels.iloc[i]['label'] == 'dog':
            img = dog_array
        else:
            img = cat_array
        ext = 'jpeg' if labels.iloc[i]['id'] == 'random5text' else 'png'
        img = np.stack([img, img, img], axis=-1, dtype=np.uint8)
        cv2.imwrite(os.path.join(ANIMALS_DIR, 
                                 f'{labels.iloc[i]["id"]}.{ext}'), img)
        cv2.imwrite(os.path.join(ANIMALS_LABELED_DIR, labels.iloc[i]['label'],
                                 f'{labels.iloc[i]["id"]}.{ext}'), img)


    SLIDES_DIR = os.path.join(DIR, 'slides')
    os.mkdir(SLIDES_DIR)

    patients = pd.read_csv(StringIO("""slide_id,patient_id,label
s6,p4,neg
s7,p5,pos
s8,p6,neg
s9,p6,neg
s10,p7,neg
s11,p7,neg
s1,p1,pos
s2,p1,pos
s3,p2,neg
s4,p3,pos
s5,p4,neg
    """))

    patients.to_csv(os.path.join(SLIDES_DIR, 'patients.csv'), index=False)

    for i in range(len(patients.to_numpy())):
        filepath = os.path.join(SLIDES_DIR, f'{patients.iloc[i]["patient_id"]}'
                                    f'_{patients.iloc[i]["slide_id"]}.tif')
        with open(filepath, 'w') as f:
            f.write('')

reset_fake_data()