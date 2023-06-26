**Supporting data for Deep Learning and Machine Vision based approaches for automated wood defect detection and quality control.** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the manufacturing industry.

The dataset consists of 20276 images with 86803 labeled objects belonging to 20 different classes including *Live_knot*, *Live_knot_bbox*, *Death_know*, and other: *Death_know_bbox*, *resin*, *resin_bbox*, *knot_with_crack_bbox*, *knot_with_crack*, *Crack_bbox*, *Crack*, *Marrow*, *Marrow_bbox*, *Quartzity_bbox*, *Quartzity*, *Knot_missing_bbox*, *Knot_missing*, *Blue_stain*, *Blue_stain_bbox*, *overgrown_bbox*, and *overgrown*.

Imagess in the Wood Defect Detection dataset has pixel-level instance segmentation and bounding box annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation task (only one mask for every class). There are 1991 (10% of the total) unlabeled images (i.e. without annotations). There are 10 splits in the dataset: *Images4* (2000 images), *Images8* (2000 images), *Images1* (2000 images), *Images5* (2000 images), *Images10* (2276 images), *Images9* (2000 images), *Images7* (2000 images), *Images2* (2000 images), *Images6* (2000 images), and *Images3* (2000 images). The dataset was released in 2021 by the [VSB TUO, Czech Republic](https://www.vsb.cz/en).

Here are the visualized examples for each of the 20 classes:

[Dataset classes](https://github.com/dataset-ninja/wood-defect-detection/raw/main/visualizations/classes_preview.webm)
