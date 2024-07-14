import io
import torch
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

app = FastAPI()

# Load ESRGAN model
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(scale=4, model_path="RealESRGAN_x4plus.pth", model=model, tile=0, tile_pad=10, pre_pad=0, half=False)

@app.post("/upscale/")
async def upscale_image(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    
    # Upscale image
    output, _ = upsampler.enhance(img)
    
    # Save and return image
    img_byte_arr = io.BytesIO()
    Image.fromarray(output).save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)