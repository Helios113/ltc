from PIL import Image
import hashlib
from pathlib import Path

from ltc import settings as st
import os

# Generate an avatar for a course
def generate_identicon(text):
    block = 8;
    width = 64
    height = width
    den = int(width/block)
    img  = Image.new( mode = "RGB", size = (width, height) )
    hs = hashlib.sha512(text.encode('utf-8')).digest()
    hs += hashlib.sha512(hs).digest()
    hs += hashlib.sha512(hs).digest()
    res = ''.join(format(i, '08b') for i in bytearray(hs))
    res = [int(res[i:i + 4],2) for i in range(0, len(res), 4)]
    m = max(res)
    res = [int(255*res[i]/m) for i in range(0, len(res))]
    it = iter(res)
    A = list(zip(it, it, it))
    for x in range(width//den):
        for y in range(height//den):
            new_color = A[den*x+y]
            for z in range(den**2):
                img.putpixel( (den*x+z//den,den*y+z%den), new_color)
        
    savePath = Path(os.path.join(*[st.STATIC_DIR, 'identicons',text+'.png']))
    img.save(savePath)
    return os.path.join(*['identicons',text+'.png'])