# https://zenodo.org/record/4694695#.YkWqTX9Bzmg

import os
import shutil
import time
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dotenv import load_dotenv
from supervisely.imaging.color import hex2rgb
from supervisely.io.fs import dir_exists, file_exists, get_file_ext, get_file_name

import src.settings as s
from dataset_tools.convert import unpack_if_archive

# https://zenodo.org/record/4694695#.YkWqTX9Bzmg


# # if sly.is_development():
# load_dotenv("local.env")
# load_dotenv(os.path.expanduser("~/supervisely.env"))

# api = sly.Api.from_env()
# team_id = sly.env.team_id()
# workspace_id = sly.env.workspace_id()


# project_name = "wood defect detection"
# dataset_path = "/home/alex/DATASETS/TODO/wood defect detection"
batch_size = 30

# images_folder = "Images"
# masks_folder = "Semantic Maps"
# bboxes_folder = "Bouding_Boxes/Bouding Boxes"
# semantic_map_name = "Semantic Map Specification.txt"
# segm_suffix = "_segm"
# bbox_suffix = "_anno.txt"
# ds_name = "ds"


# if sly.is_development():
# load_dotenv("local.env")
# load_dotenv(os.path.expanduser("~/supervisely.env"))

# api = sly.Api.from_env()
# team_id = sly.env.team_id()
# workspace_id = sly.env.workspace_id()


# project_name = "wood defect detection"
# dataset_path = "/home/alex/DATASETS/TODO/wood defect detection"


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    teamfiles_dir = "/4import/original_format/wood_defect_detection"
    storage_dir = sly.app.get_data_dir()
    batch_size = 100

    images_folder = "Images"
    masks_folder = "Semantic Maps/Semantic Maps"
    bboxes_folder = "Bouding_Boxes/Bouding Boxes"
    semantic_map_name = "Semantic Map Specification.txt"
    segm_suffix = "_segm"
    bbox_suffix = "_anno.txt"
    ds_name = "ds"
    team_id = sly.env.team_id()

    def download_dataset(teamfiles_dir: str):
        if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
            parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
            file_name_with_ext = os.path.basename(parsed_url.path)
            file_name_with_ext = unquote(file_name_with_ext)

            sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)
            api.file.download(team_id, teamfiles_path, local_path)

            dataset_path = unpack_if_archive(local_path)
            if dataset_path != local_path:
                os.remove(local_path)

        if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
            for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
                local_path = os.path.join(storage_dir, file_name_with_ext)
                teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

                if not os.path.exists(get_file_name(local_path)):
                    api.file.download(team_id, teamfiles_path, local_path)

                    sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                    unpacked = unpack_if_archive(local_path)

                    if unpacked != local_path:
                        os.remove(local_path)
                else:
                    sly.logger.info(
                        f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                    )

            dataset_path = storage_dir
        return dataset_path

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            if col != 0:
                unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        mask_name = get_file_name(image_path) + segm_suffix + get_file_ext(image_path)
        mask_path = os.path.join(masks_path, mask_name)
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)
            unique_colors = get_unique_colors(mask_np)
            for color in unique_colors:
                mask = np.all(mask_np == color, axis=2)
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    bitmap = sly.Bitmap(data=obj_mask)
                    if bitmap.area > 50:
                        obj_class = color_to_obj_class[color]
                        label = sly.Label(bitmap, obj_class)
                        labels.append(label)

        bbox_name = get_file_name(image_path) + bbox_suffix
        bbox_path = os.path.join(bboxes_path, bbox_name)
        if file_exists(bbox_path):
            with open(bbox_path) as f:
                content = f.read().split("\n")

                for curr_data in content:
                    if len(curr_data) != 0:
                        curr_data = curr_data.split("\t")
                        curr_data_name = curr_data[0]
                        if name_to_obj_class.get(curr_data_name) is None:
                            curr_data_name = error_name_to_real[curr_data_name]

                        curr_obj_class = name_to_obj_class.get(curr_data_name)
                        try:
                            left = int(
                                float(curr_data[1]) * img_wight
                            )  # skip 'can not convert str to float' error
                            top = int(float(curr_data[2]) * img_height)
                            right = int(float(curr_data[3]) * img_wight)
                            bottom = int(float(curr_data[4]) * img_height)
                            rectangle = sly.Rectangle(
                                top=top, left=left, bottom=bottom, right=right
                            )
                            label = sly.Label(rectangle, curr_obj_class)
                            labels.append(label)
                        except:
                            pass
                        finally:
                            continue

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    # dataset_path = download_dataset(teamfiles_dir)
    dataset_path = storage_dir
    semantic_map_path = os.path.join(dataset_path, semantic_map_name)
    name_to_obj_class = {}
    color_to_obj_class = {}
    error_name_to_real = {
        "Dead_Knot": "Death_know",
        "Live_Knot": "Live_knot",
        "Blue_Stain": "Blue_stain",
    }

    with open(semantic_map_path) as f:
        content = f.read().split("\n")
        content.append(" ")

        for idx in range(0, len(content), 4):
            class_name = content[idx + 1].split("=")[1].strip()
            color_hex = content[idx + 2].split("=")[1]
            color_rgb = hex2rgb("#" + color_hex)
            curr_obj_class = sly.ObjClass(class_name, sly.AnyGeometry, color_rgb)
            color_to_obj_class[tuple(color_rgb)] = curr_obj_class
            name_to_obj_class[class_name] = curr_obj_class

    obj_classes = list(color_to_obj_class.values())

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=obj_classes)
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    all_data = os.listdir(dataset_path)

    for curr_data in all_data:
        images_path = os.path.join(dataset_path, curr_data)
        if dir_exists(images_path) and curr_data[:6] == images_folder:
            masks_path = os.path.join(dataset_path, masks_folder)
            bboxes_path = os.path.join(dataset_path, bboxes_folder)
            images_names = os.listdir(images_path)

            progress = sly.Progress("Add {} in dataset".format(curr_data), len(images_names))

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(images_path, image_name) for image_name in img_names_batch
                ]
                img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]
                anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))
    return project
