from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Wood Defect Detection"
PROJECT_NAME_FULL: str = "Supporting data for Deep Learning and Machine Vision based approaches for automated wood defect detection and quality control"

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Manufacturing()]
CATEGORY: Category = Category.Manufacturing()

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.SemanticSegmentation(),
    CVTask.ObjectDetection(),
]
ANNOTATION_TYPES: List[AnnotationType] = [
    AnnotationType.InstanceSegmentation(),
    AnnotationType.ObjectDetection(),
]

RELEASE_DATE: Optional[str] = "2021-04-15"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://zenodo.org/record/4694695#.YkWqTX9Bzmg"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 845345
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/wood-defect-detection"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "Bouding_Boxes.zip": "https://zenodo.org/record/4694695/files/Bouding_Boxes.zip?download=1",
    "Images1.zip": "https://zenodo.org/record/4694695/files/Images1.zip?download=1",
    "Images2.zip": "https://zenodo.org/record/4694695/files/Images2.zip?download=1",
    "Images3.zip": "https://zenodo.org/record/4694695/files/Images3.zip?download=1",
    "Images4.zip": "https://zenodo.org/record/4694695/files/Images4.zip?download=1",
    "Images5.zip": "https://zenodo.org/record/4694695/files/Images5.zip?download=1",
    "Images6.zip": "https://zenodo.org/record/4694695/files/Images6.zip?download=1",
    "Images7.zip": "https://zenodo.org/record/4694695/files/Images7.zip?download=1",
    "Images8.zip": "https://zenodo.org/record/4694695/files/Images8.zip?download=1",
    "Images9.zip": "https://zenodo.org/record/4694695/files/Images9.zip?download=1",
    "Images10.zip": "https://zenodo.org/record/4694695/files/Images10.zip?download=1",
    "Semantic Map Specification.txt": "https://zenodo.org/record/4694695/files/Semantic%20Map%20Specification.txt?download=1",
    "Semantic Maps.zip": "https://zenodo.org/record/4694695/files/Semantic%20Maps.zip?download=1",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = None
CITATION_URL: Optional[str] = "https://zenodo.org/record/4694695/export/hx"
AUTHORS: Optional[List[str]] = None

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = "VSB TUO, Czech Republic"
ORGANIZATION_URL: Optional[Union[str, List[str]]] = "https://www.vsb.cz/en"

SLYTAGSPLIT: Optional[Dict[str, List[str]]] = None
TAGS: List[str] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["project_name_full"] = PROJECT_NAME_FULL or PROJECT_NAME
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    return settings
