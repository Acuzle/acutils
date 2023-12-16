# acutils

**Python library providing a robust pipeline for data processing tasks.**

The acutils library is designed to facilitate data processing tasks, particularly for individuals dealing with custom data preprocessing before building machine learning algorithms. It has been utilized in various domains, including pathology image processing, custom segmentation, and frame extractions from videos.

HERE ARE THE [DOCUMENTATION FILES](./doc).



## Key features

1. You only need to **code** **one** **function** for a custom treatment, nothing else.
1. Easy **random** distribution/split of the data into **datasets**.
1. Remember and **reproduce** your **distribution**/**split** by saving it to **JSON** files.
1. Made for **multiprocessing** and facilitate GPU usage for computation.
1. Works with **any** kind of **data** files.
1. If some **files** are **related** (for example: two medical images from the same patient), you can **define** **groups** to ensure that those are in the same dataset (to **avoid** **biases**).



## Brief example

```py
import acutils as au

# Define the handler and linked it to a source directory
handler = au.handler.DataHandler('./data', allowed_cpus=2)

# Load filenames and labels
handler.load_data_fromdatapath()
handler.load_labels_fromsheet('./labels.xlsx', idcol="id", labelcol="label")

# Even load relations between files through groups (optional for split)
handler.load_groups_fromsheet(os.path.join(DIR, './labels.xlsx'), 
                               idcol="id", groupcol="patient")

# Randomly split into datasets (dict<filename,label>) and balance them
tdata, vdata = handler.split(train_percentage=0.70) # use groups if defined
bal_tdata, bal_vdata = handler.balance_datasets(tdata, vdata)

#TODO
def your_custom_treatment(self, src, dstdir, arg1):
    au.file.tmnt_copyfile_to_dir(src, dstdir) # example

# Process the data using your custom function and save the datasets:
handler.make_datasets('./train_bal', './val_bal', bal_tdata, bal_vdata, 
                      func=your_custom_treatment, # custom function
                      arg1="very useful argument") # its arguments
```



## Installation

- It should work using any OS, but for now, we only tested using Ubuntu 22.04.
- It works using any Python version >= 3.8 (maybe lowers too, but not tested yet).


### From pip

```bash
pip install acutils
```


### From this repository (still pip though :)

```bash
pip install --upgrade build
```

```bash
python3 -m build
```

```bash
pip install dist/acutils-0.1-py3-none-any.whl
```


### Additional requirements

- `Pillow`, `scikit-image`, `pooch` and `openslide-python`: **pathology** module.
- `opencv-python`: **image**, **pathology** and **video** modules.

```bash
pip install opencv-python Pillow scikit-image pooch openslide-python
```

Finally, the **pathology** module requires you to install [Openslide](https://openslide.org/), `openslide-python` is just a mapping of it. Maybe reinstall openslide-python after installing Openslide, but it should not be necesarry.


### GPU computation

For now, this is only used in **pathology** modules (because the process take a while).

- `cupy`: numpy but using GPU.
- `cucim`: includes cucim.skimage that is skimage (older version) using GPU.

```bash
pip install cupy cucim
```

Make you CUDA install usable from cupy:
```bash
export LD_LIBRARY_PATH=/path/to/cudnn/lib:$LD_LIBRARY_PATH
```

Choose at least one device (if multiple, we take the first):
```bash
export CUDA_VISIBLE_DEVICES=0
```



## Modules

Use the relevant modules from acutils based on your data processing needs:

- **handler**: High-level classes to handle data processing.
- **file**: About directories and files.
- **gpu**: GPU computation (for now, only used in pathology module).
- **image**: Computer Vision tasks on images.
- **multiprocess**: Multiprocessing and process management.
- **pathology**: Pathology data processing for segmentation and tiling.
- **sheet**: Handling pandas DataFrames.
- **video**: Video data processing.

Refer to the [documentation files](./doc) and code [examples](./examples) for detailed usage instructions.



## TBD

- [ ] Provide more code examples.
- [ ] Define a test pipeline to check if all features work.
- [ ] Ensure that acutils works on multiple OS and Python versions.



## License

Proprietary but will very very soon be switched to MIT or Apache 2.0.



## Contributing

This library is maintained by [Acuzle](https://acuzle.com/)'s development team, lead by [@ThomasPDM](https://github.com/ThomasPDM).

We welcome and appreciate contributions from the community to enhance acutils. If you have ideas, bug fixes, or new features that can benefit others, we encourage you to contribute to the project. Just fork the project, create a new branch, do whatever you want and create a pull request.