import os
import pyvips
import requests
from env_search import BEARER_PUBLIC_API

def svg_conversion(url):
    headers = {
    'BEARER_PUBLIC_API': BEARER_PUBLIC_API,
    }
    
    _image = requests.get(url=url, headers=headers, stream=True)
    # print(_image.headers.get('content-type'))
    if _image.headers.get('content-type') == 'image/svg+xml':
        nft_source = pyvips.Image.svgload_buffer(_image.content)
        nft_source.write_to_file("nft-image.png")
    elif _image.headers.get('content-type') == 'image/jpg' or _image.headers.get('content-type') == 'image/jpeg':
        nft_source = pyvips.Image.jpegload_buffer(_image.content)
        nft_source.write_to_file("nft-image.png")
    elif _image.headers.get('content-type') == 'image/gif':
        nft_source = pyvips.Image.gifload_buffer(_image.content)
        nft_source.write_to_file("nft-image.png")
    elif _image.headers.get('content-type') == 'video/mp4':
        return _image.content
     
# svg_conversion("https://storage.opensea.io/files/3243ae9e09e2881df764d4209a712810.svg")
# svg_conversion("https://lh3.googleusercontent.com/4cQGzUrNtaZzb8GNktAa0LaHNKln-QY2qqpNRKnMt2Gs2PuYP2yycSfWRRflMMmw9-6fmA5k4WtZlXRRSaoInWNhM9igtwNJZfZETEA")
# svg_conversion("https://storage.googleapis.com/apex-go-collections/tron-bulls/tokenID_13456")