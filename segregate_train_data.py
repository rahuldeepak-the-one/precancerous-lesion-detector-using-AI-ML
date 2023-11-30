import os
import random
import pandas as pd
import shutil
# df = pd.read_csv("ISIC2018_Task3_Test_GroundTruth.csv")
df = pd.read_csv("labels.csv")
#print(df.to_markdown())

base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "Images_set")
image_files = os.listdir(image_dir)
num_images = int(len(image_files) * 20 / 100)

selected_images = random.sample(image_files, num_images)
# unlabeled_path = os.path.join(image_dir, "unlabeled")
os.makedirs("unlabelled_images", exist_ok=True)
# os.makedirs("unlabelled_images", exist_ok=True)

image_ids=[]
for file in image_files:
    if not os.path.isfile(os.path.join(image_dir, file)):
        continue
    
    if file in selected_images:
        image_id=file[:-4]
        image_ids.append(image_id)
    else:
        image_path = os.path.join(image_dir, file)
        shutil.move(image_path, "unlabelled_images")
        
image_classes=[]
for image_id in image_ids:
    row = df.loc[df["image_id"] == image_id]
    image_class = row["dx"].iloc[0]

    image_class_path = os.path.join(image_dir, image_class)

    if image_class not in image_classes:
        if os.path.exists(image_class_path):
            os.chmod(image_class_path, 0o777)
            os.remove(image_class_path)
        os.mkdir(image_class_path)
        image_classes.append(image_class)
    
    img = image_id + '.jpg'
    img_path = os.path.join(image_dir, img)
    os.rename(img_path, os.path.join(image_class_path, img))
print(image_files)

# print(image_files)
