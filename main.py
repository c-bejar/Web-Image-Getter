"""
This script will attempt to grab image urls from specific websites and save them in a .txt file
of your choosing. The .txt file will look something like this:
imagefiles.txt
->
    https://www.sampleimageurl.com/image1
    https://www.sampleimageurl.com/image2
    https://www.sampleimageurl.com/image3
    https://www.sampleimageurl.com/image4
    https://www.sampleimageurl.com/image5
--
These images are intended to be used with Cubari for the purposes of making grabbing images
much easier, as it can be a headache.
"""

import json
from image_url import get_img_urls

# List of supported websites
with open("supported_sites.json", "r") as file:
    websites = json.load(file)

print("Choose from the following supported websites:")
for i in range(1, len(websites) + 1, 1):
    print(f"{i}) {websites[i - 1]}")

# Get user input for site selected
while True:
    site = input("Website: ")
    try:
        if int(site) in range(1, len(websites) + 1):
            break
    except:
        print("\tInvalid value. Enter a number from the list.")
site = websites[int(site) - 1]

chapter_count = 1
while True:
    print("\nEnter full URL for chapter you want to get images for (\"x\" to exit):")
    url = input("URL: ")

    if url == "x":
        break

    many_chapters = input("Automatically get images for following X chapters? (y/n): ")
    match many_chapters:
        case "y": amount = int(input("How many chapters: "))
        case "n": amount = 1
    chapter_images = get_img_urls(url, amount)
    if chapter_images:
        for chapter in chapter_images:
            with open(f"images/Chapter {chapter_count}", "w") as file:
                for img in chapter:
                    if img != chapter[-1]: # check if current image is not the last in the list
                        file.write(img + "\n")
                    else:
                        file.write(img)
            chapter_count += 1