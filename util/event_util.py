import uproot as ur
import numpy as np

# Returns a flattened list of calo images.
# Ordering is consistent with event/topo-cluster ordering in input.
# TODO: Check if this still works, maybe needed for JetClusteringPion.ipynb
def setupCellsOld(calo_images, layer, nevents = -1):
        
    # 1st dim is number of clusters (VARIABLE)
    # 2nd dim is eta (or phi?) (CONSTANT)
    # 3rd dim is phi (or eta?) (CONSTANT)
    
    if(nevents > 0): image_set = calo_images[layer][:nevents].flatten()
    else: image_set = calo_images[layer].flatten() # flattened list of 2D images
    # get number of pixels from shape of initial entry
    num_pixels = image_set.shape[-1] * image_set.shape[-2]
    image_set = image_set.reshape(image_set.shape[0],num_pixels)
    return image_set
    
    
# Returns a flattened list of calo images.
# Ordering is consistent with event/topo-cluster ordering in input.
def setupCells(calo_images, layer, nevents = -1):
        
    # 1st dim is number of clusters (VARIABLE)
    # 2nd dim is eta (or phi?) (CONSTANT)
    # 3rd dim is phi (or eta?) (CONSTANT)
    if(nevents > 0): image_set = calo_images[layer][:nevents]
    else: image_set = calo_images[layer]
        
    # get number of pixels from shape of initial entry
    num_pixels = image_set.shape[-1] * image_set.shape[-2]
    image_set = image_set.reshape(image_set.shape[0],num_pixels)
    return image_set
    