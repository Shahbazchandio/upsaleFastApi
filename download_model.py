import urllib.request
import os

def download_model():
    url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    filename = "RealESRGAN_x4plus.pth"
    
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"{filename} downloaded successfully.")
    else:
        print(f"{filename} already exists.")

if __name__ == "__main__":
    download_model()