# Image Downloader

A small app with GUI that downloads images from a webpage.

The script fetches a page, extracts all `<img>` elements, then downloads the images into a local folder organized by domain.

## Requirements

* Python 3
* Tkinter
* `requests`
* `beautifulsoup4`

Install dependencies:

```
pip install requests beautifulsoup4
```

## Usage

```
python img_downloader.py https://example.com
```

## What it does

1. Connects to the provided URL
2. Parses the HTML page
3. Extracts image URLs from `<img>` tags
4. Downloads each image using streamed requests

Images are saved in:

```
image_downloader/<domain>/
```

Example:

```
image_downloader/
    example.com/
        image1.jpg
        image2.png
```

## Notes

* Uses a persistent HTTP session for efficiency.
* Handles relative image URLs from the target site.
* Skips images without a valid `src` attribute.

