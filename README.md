# pil-numpy-homography-sample
Sample code for homography 

## Environment
Python 2.7  

## Dependencies
- Numpy
- PIL  
*This code doesn't depend on OpenCV but only Numpy and PIL, so it can be used on Google App Engine :)*

## Set up commands

```
pip install numpy==1.6.1
pip install Pillow==4.3.0
```
*This code might be compatible with upper versions of Numpy/Pillow, but it's not tested.*

## Performances

| base image size | color scale | execution time<br>(avg - 10times) |
|:------------|:------------|:--------|
| 768x1024 | RGB | 14.5ms |
| 768x1024 | Gray | 6.28ms |
| 2448x3264 | RGB | 150ms |
| 2448x3264 | Gray | 60.2ms |

(on Macbook Air)

## Sample code to use homography.py

```
#!/usr/bin/python
# -*- coding: utf-8 -*-

import path.to.homography as homography
import base64
from io import BytesIO

def some_method_to_process_uploaded_img(base64_img, corner_list, dest_list):
    base_img = Image.open(BytesIO(base64.b64decode(base64_img)))
    # execute homography transformation
    transformed_img = homography.transform(
        img=base_img,
        crop_corner_list=corner_list,
        destination_corner_list=dest_list
    )

    # or, extend to the size of base_img == (destination_corner_list=None)
    # transformed_img = homography.transform(
    #     img=base_img,
    #     crop_corner_list=corner_list
    # )

    # If base64 encoded data is needed:
    in_memory_file = BytesIO()
    transformed_img.save(in_memory_file, format="PNG")
    in_memory_file.seek(0)
    img_bytes = in_memory_file.read()
    transformed_base64_image = base64.b64encode(img_bytes).decode('ascii')
```

## Sample test commands

```
# execute sample image transformation with ./img/sample.png
test.sh

# transform with gray scale option(-L)
python ./main.py -i ./img/sample.png -c "78, 114, 18, 258, 390, 230, 342, 18" -L

# transform to an intended shape
python ./main.py -i ./img/sample.png -c "78, 114, 18, 258, 390, 230, 342, 18" -d "0, 50, 30, 250, 260, 140, 250, 10"

# save the result as a file
python ./main.py -i ./img/sample.png -c "78, 114, 18, 258, 390, 230, 342, 18" -o ./path/to/destination

```

## Ref
[PIL/pillowとNumpyで射影変換(ホモグラフィ変換)をしてみた / GAE環境でも実行可能](https://qiita.com/naosk8/items/cde89dd93044e0abb054)
