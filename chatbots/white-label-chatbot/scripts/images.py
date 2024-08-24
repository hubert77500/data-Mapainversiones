import requests
import os

from PIL import Image

#Script I used to convert images from webp to png.

def download_images(image_urls, save_folder):
    """
    Downloads each image from the provided list of URLs and saves them into the specified folder.

    :param image_urls: List of image URLs (strings)
    :param save_folder: Folder where images will be saved
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Download each image
    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check that the request was successful

            # Save the image
            image_path = os.path.join(save_folder, f'image_{idx}.webp')
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {url} to {image_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {str(e)}")


def convert_images_to_png_with_background(source_folder, output_folder, background_color=(255, 255, 255)):
    """
    Converts all images in the source folder to PNG format with a white background and saves them in the output folder.

    :param source_folder: Folder containing images with transparency
    :param output_folder: Folder where PNG images will be saved
    :param background_color: Tuple representing the RGB color of the background, default is white (255, 255, 255)
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files that you expect to have transparency (like .png, .webp)
    files = [f for f in os.listdir(source_folder) if f.endswith(('.png', '.webp'))]

    # Convert each file
    for file in files:
        file_path = os.path.join(source_folder, file)
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_with_bg.png")

        try:
            # Open the image file
            with Image.open(file_path) as img:
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    # Create a white background image
                    background = Image.new('RGBA', img.size, background_color + (255,))
                    # Paste the image using alpha channel as mask
                    background.paste(img, mask=img.split()[3])
                    # Convert to RGB
                    rgb_background = background.convert('RGB')
                    rgb_background.save(output_file_path, 'PNG')
                else:
                    # If no transparency, just convert
                    img.convert('RGB').save(output_file_path, 'PNG')
            print(f"Converted {file} to {output_file_path}")

        except IOError as e:
            print(f"Failed to convert {file}: {str(e)}")


# Example usage
image_urls = [
    "https://acdn.mitiendanube.com/stores/001/083/008/products/000515-29e95df689ce21a20b17105338860775-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/000422-81d298355eb203de5017105335280886-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/003420-38567f9bdc6f9e377a17105326500433-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/gt-22ges-78698332cabf543b2917105309697758-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/8001-a2218aeac2616760ff16086508283418-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/srm-520es-003636-95e4b24794877ad60917105328784185-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/d_nq_np_2x_984789-mla45638967254_042021-f1-19a1194e57313b5a5c16395753571591-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/d_nq_np_2x_780840-mla46320512630_06202121-af4fd01644a6c79fff16395758328390-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/0-desktop-11-c1c83b3da454647e8516482992470269-640-0.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/0-desktop-111-c1c83b3da454647e8516482993215793-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/d_nq_np_2x_780840-mla46320512630_06202111-af4fd01644a6c79fff16395755924246-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/bomba-czerweny-trif1-dc9302c288caa806b215862122572674-640-0.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/0-desktop-121-c1c83b3da454647e8516482994064763-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/electrica21-ceb92d3b00430cc50116317568995146-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/chulengo1-8c2fd65b5918bb13f916317567419907-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/1100-gris-logo-negro-11-ea9223f9caae49d90416239636313959-1024-1024.webp",
    "https://acdn.mitiendanube.com/stores/001/083/008/products/felco-311-108b39ef6ffa5dec5c16848543386594-1024-1024.webp",
]

# download_images(image_urls, './images')
convert_images_to_png_with_background('./images', './pngs')

