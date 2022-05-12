import os
import requests
from env_search import BEARER_PUBLIC_API


def save_template(url):
    headers = {
    'BEARER_PUBLIC_API': BEARER_PUBLIC_API,
    }
    
    os.chdir('.')
    if not os.path.exists('nft_images'):
        os.makedirs('nft_images')
    os.chdir('nft_images')
    x = 0

    while os.path.isfile('nft-' + str(x) + '.png'):
        x += 1

    with open('nft-' + str(x) + '.png', 'wb') as t:
        template = requests.get(url=url, headers=headers, stream=True)
        if not template.ok:
            raise Exception("Couldn't get_request the nft_image, please verify the image created!")

        for block in template.iter_content(1024):
            if not block:
                raise Exception('NOT BLOCK: An error was found when trying to save this block image!')
            t.write(block)

        f_name, f_ext = os.path.splitext('nft-' + str(x) + '.png')
        if os.path.isfile('nft-' + str(x) + '.png'):
            print(f'Successful created: {template.status_code}')

    return f_name+'.png'