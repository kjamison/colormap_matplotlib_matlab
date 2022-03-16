import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.io import savemat

def write_cmap_matfile(outfile,n=256):
    C={}
    for cname in plt.colormaps():
        cmap = plt.get_cmap(cname, n)(range(n))
        C[cname]=cmap[:,:3]

    C["version_matplotlib"]=matplotlib.__version__
    C["version_python"]="%d.%d.%d" % (sys.version_info.major,sys.version_info.minor,sys.version_info.micro)
    savemat(outfile, C, format="5", do_compression=True)

if __name__ == '__main__':
    outfile=sys.argv[1]
    n=256
    if len(sys.argv) > 2:
        n=int(sys.argv[2])
    write_cmap_matfile(outfile,n)
