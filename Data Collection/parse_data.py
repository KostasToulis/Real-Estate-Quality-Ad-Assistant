import csv
import os
import requests
from urllib.parse import urlparse

def read_txt_file(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines


def create_directory(url):
    parsed_url = urlparse(url)
    directory_name = sanitize_filename(parsed_url.path.replace('/', '_'))
    directory = os.path.join('images', directory_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()


def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded image from {url} to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {url}. Error: {e}")


def write_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Description', 'Location', 'Price', 'Image Directory'])
        writer.writerows(data)


def process_lines(lines):
    data = []
    num_lines = len(lines)
    i = 0
    while i < num_lines:
        url = lines[i].strip()
        if i + 4 < num_lines:
            description = lines[i + 2].strip()
            location = lines[i + 3].strip()
            price = lines[i + 4].strip()
            image_urls = lines[i + 1].strip().split()
            directory = create_directory(url)
            if len(image_urls):
                download_images(image_urls, directory)
            data.append([url, description, location, price, directory])
            i += 5
        else:
            break
    return data


def download_images(image_urls, directory):
    for idx, url in enumerate(image_urls):
        image_name = f"image_{idx + 1}.jpg"
        save_path = os.path.join(directory, image_name)
        download_image(url, save_path)


def txt_to_csv_with_images(txt_file, csv_file):
    lines = read_txt_file(txt_file)
    data = process_lines(lines)
    write_csv(data, csv_file)
    print(f"Converted {txt_file} to {csv_file}")



txt_file = 'data1.txt'
csv_file = 'holdout.csv'
txt_to_csv_with_images(txt_file, csv_file)
