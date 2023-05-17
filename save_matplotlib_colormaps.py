import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import sys
from scipy.io import savemat

def complementary_colormap(cmap,new_cmap_name='complementary_cmap'):
    from colorspacious import cspace_converter


    
    try:
        n=cmap.N
        v=np.linspace(0,1,n)
        base_colors=cmap(v)[:,:3]
    except TypeError:
        n=cmap.shape[0]
        base_colors=cmap.copy()[:,:3]
    
    lab_colors=cspace_converter("sRGB1", "JCh")(base_colors[np.newaxis,:,:])
    new_colors=lab_colors
    new_colors[0,:,2]=(lab_colors[0,:,2]+180) % 360
    new_rgb=cspace_converter("JCh","sRGB1")(new_colors)
    new_rgb=np.clip(new_rgb,0,1)
    new_cmap=LinearSegmentedColormap.from_list(new_cmap_name, new_rgb[0,:,:],N=n)

    return new_cmap

def write_cmap_matfile(outfile,n=256,add_complementary=False, add_complementary_diverging=False):

    C={}
    for cname in plt.colormaps():
        print("Adding %s" % (cname))
        cmap = plt.get_cmap(cname, n)(range(n))
        C[cname]=cmap[:,:3]

    if add_complementary:
        for cname in plt.colormaps():
            if cname.endswith("_r"):
                new_cname=cname[:-2]+"_comp_r"
            else:
                new_cname=cname+"_comp"
            
            new_cmap = complementary_colormap(plt.get_cmap(cname, n))

            print("Adding %s" % (new_cname))
            cmap = new_cmap(range(n))
            C[new_cname]=cmap[:,:3]

    if add_complementary_diverging:
        for cname in plt.colormaps():
            if cname.endswith("_r"):
                continue
            else:
                new_cname=cname+"_compdiv"
            
            halfn=n//2
            new_cmap = complementary_colormap(plt.get_cmap(cname+"_r", halfn))

            print("Adding %s" % (new_cname))
            cmap1 = plt.get_cmap(cname, halfn)(range(halfn))
            cmap2 = new_cmap(range(halfn))
            cmap=np.vstack((cmap2,cmap1))
            C[new_cname]=cmap[:,:3]

            print("Adding %s" % (new_cname+"_r"))
            C[new_cname+"_r"]=cmap[::-1,:]

    C["version_matplotlib"]=matplotlib.__version__
    C["version_python"]="%d.%d.%d" % (sys.version_info.major,sys.version_info.minor,sys.version_info.micro)
    savemat(outfile, C, format="5", do_compression=True)

if __name__ == '__main__':
    outfile=sys.argv[1]
    n=256
    if len(sys.argv) > 2:
        n=int(sys.argv[2])
    write_cmap_matfile(outfile,n,add_complementary=True,add_complementary_diverging=True)
