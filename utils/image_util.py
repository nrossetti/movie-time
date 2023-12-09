import aiohttp
from PIL import Image
import io

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                return image_data
            else:
                print(f"Failed to download image from {url}. HTTP Status Code: {response.status}")
                return None     

def convert_image_format(image_data, format="JPEG"):
    image = Image.open(io.BytesIO(image_data))
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format=format)
    return image_byte_arr.getvalue()