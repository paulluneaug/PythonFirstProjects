from PIL import Image

def ascii_art(img_name,extension):
    img=Image.open(img_name+extension)
    img_bw=img.convert('L')
    # img.show()
    resx=3
    resy=resx
    width, height = img.size
    d=[[0 for x in range(width//resx+1)] for y in range(height//resy+1)]
    palette="@$#%+*/=°,:-'. "
    # strimg=''
    # for j in range(13):
    #     for e in palette:
    #         strimg+=26*e
    #     strimg+='\n'
    
    # print(strimg,file=open('palette.txt','w',encoding='utf-8'))
        
    # return None  
    for x in range(0,width):
        for y in range(0,height):
            d[y//resy][x//resx]+=img_bw.getpixel((x,y))/(resx*resy)
      
    strimg=''            
    for x in d:
        for y in x:
            strimg+=palette[int(y/256*len(palette))]
        strimg+='\n'
    print(strimg,file=open(f'asciiart{img_name}.txt','w',encoding='utf-8'))
        
def tup2str(tup):
    return f'#{hex(tup[0])}{hex(tup[1])}{hex(tup[2])}'
ascii_art('example','.jpg')