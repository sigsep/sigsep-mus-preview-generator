# SISEC MUS 2018 Preview Generator

This repository aims to generate 30s excerpts from both the
[MUSDB18](https://sigsep.github.io/musdb.html) music data set and the estimated
sources submitted by participants of [SiSEC MUS 2018](https://sisec.inria.fr/).

Previews are generated from a pre-defined cut-list, such as those created using
[sigsep-mus-cutlist-generator](https://github.com/sigsep/sigsep-mus-cutlist-generator).

## Usage

1. Install python3.6 requirements using `pip install -r requirements.txt`

2. Trim the reference MUSDB18 using
    ```
    python generate_previews.py --musdb /path/to/musdb --previews 30s_previews.csv -o previews_output_dir
    ```
    where `30s_previews.csv` is the cut-list.

3. Trim the user submissions using:
    ```
    python generate_submission_previews.py --estimate_root_dir /path/to/my_estimations --previews 30s_previews.csv -o previews_output_dir
    ```

3.1. Using GNU Parallel to cut multiple submission folders

```
parallel python generate_submission_previews.py --estimate_root_dir /path/to/all_submissions/{/} --previews 30s_previews.csv  -o /path/to/cut_submissions/{/} ::: /path/to/all_submissions/*
```
