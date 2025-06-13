from PIL import Image
def mockup_3d(png_path:str)->str:
    base=Image.open(png_path).convert("RGBA");W,H=base.size
    persp=base.transform((int(W*0.85),int(H*0.85)),Image.AFFINE,(1,-0.3,0,0,1,0),Image.BICUBIC)
    canvas=Image.new("RGBA",(W+200,H+100),"#FFFFFF");canvas.paste(persp,(100,50),persp)
    out=png_path.replace('_cover_','_mock3d_');canvas.convert("RGB").save(out);return out
