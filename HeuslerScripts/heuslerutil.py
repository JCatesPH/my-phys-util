#!/anaconda3/envs/aseenv/bin/python
# -*- coding: utf-8 -*-
"""
# Created on Thu Apr  4 20:15:28 2019

@author: jalendesktop
"""

# Environment setting
from ase import Atoms
import numpy as np
from ase.visualize import view

def makeFull16( X, Y, Z, cellParam ):
    """
    Takes input for heusler lattice to create 16 atom cell. Allows manipulation to make slabs, defects, etc.

    Inputs:
    X : Atomic symbol of X site atom
    Y : Atomic symbol of Y site atom
    Z : Atomic symbol of Z site atom
    cellparam : cell parameter
    Outputs:
    L21cell : ase.Atoms object with 16 atoms
    """
    a = cellParam
    L21cell = Atoms((X, X, X, X, X, X, X, X, Y, Y, Y, Y, Z, Z, Z, Z),
                positions = [(0,0,0), (.5*a,0,0), (0,.5*a,0), (.5*a,.5*a,0), (0,0,.5*a), (.5*a,0,.5*a), (0,.5*a,.5*a), (.5*a,.5*a,.5*a),
                             (.25*a,.25*a,.25*a), (.75*a, .75*a, .25*a), (.75*a, .25*a, .75*a), (.25*a,.75*a,.75*a),
                             (.75*a,.25*a,.25*a), (.25*a,.75*a,.25*a), (.25*a,.25*a,.75*a), (.75*a,.75*a,.75*a)],
                cell = (cellParam, cellParam, cellParam))
    return L21cell


def makeInverse16( X, Y, Z, cellParam ):
    """
    Takes input for heusler lattice to create 16 atom cell. Allows manipulation to make slabs, defects, etc.

    Inputs:
    X : Atomic symbol of X site atom
    Y : Atomic symbol of Y site atom
    Z : Atomic symbol of Z site atom
    cellparam : cell parameter
    Outputs:
    XAcell : ase.Atoms object with 16 atoms
    """
    a = cellParam
    XAcell = Atoms((X, X, X, X, X, X, X, X, Y, Y, Y, Y, Z, Z, Z, Z),
                positions = [(.5*a,0,0), (0,.5*a,0), (0,0,.5*a), (.5*a,.5*a,.5*a), (.75*a,.25*a,.25*a), (.25*a,.75*a,.25*a), (.25*a,.25*a,.75*a), (.75*a,.75*a,.75*a),
                             (.25*a,.25*a,.25*a), (.75*a, .75*a, .25*a), (.75*a, .25*a, .75*a), (.25*a,.75*a,.75*a),
                             (0,0,0), (.5*a,0,.5*a), (0,.5*a,.5*a), (.5*a,.5*a,0)],
                cell = (cellParam, cellParam, cellParam))
    return XAcell

def superFullH(acell16):
    """
    Takes the 16 atom cell as input, then performs the translations to get supercell with the same X, Y, Z, and cell param.
    """
    ions = acell16.get_chemical_symbols()
    X = ions[0]
    a = acell16.get_cell()[0,0]
    w = a/2
    AddedX = Atoms((X, X, X,  X, X, X,  X, X, X,  X, X, X,  X, X, X,  X, X, X, X),
                   positions = [(0,a,0), (a,0,0), (a,w,0),
                                (a,a,0), (w,a,0), (0,a,w),
                                (a,0,w), (a,w,w), (a,a,w),
                                (w,a,w), (0,0,a), (0,w,a),
                                (0,a,a), (w,0,a), (a,0,a),
                                (w,w,a), (a,w,a), (a,a,a),
                                (w,a,a)])
    return acell16.extend(AddedX)

def swapSites(acell16, disorder):
    """
    The function takes the L21 cell and desired disorder, then it swaps the sites in the cell to get the desired POSCAR file.
    Will work on this one to make it more robust (for IH as well).
    
    Input:
        acell16 : L21 cell as ase.Atoms object
        disorder : string with values '12.5', '25', '37.5', or '50' describing disorder percentage
    Output:
        disorderedcell : A new ase.Atoms object with desired disorder
    """
    copyofacell16 = acell16
    if (disorder=='12.5'):
        copyofacell16.positions[[8,7]] = copyofacell16.positions[[7,8]]
        
    elif (disorder=='25'):
        copyofacell16.positions[[8,7]] = copyofacell16.positions[[7,8]]
        copyofacell16.positions[[4,11]] = copyofacell16.positions[[11,4]]
        
    elif (disorder=='37.5'):
        copyofacell16.positions[[8,7]] = copyofacell16.positions[[7,8]]
        copyofacell16.positions[[4,11]] = copyofacell16.positions[[11,4]]
        copyofacell16.positions[[1,9]] = copyofacell16.positions[[9,1]]
        
    elif (disorder=='50'):
        copyofacell16.positions[[8,7]] = copyofacell16.positions[[7,8]]
        copyofacell16.positions[[4,11]] = copyofacell16.positions[[11,4]]
        copyofacell16.positions[[1,9]] = copyofacell16.positions[[9,1]]
        copyofacell16.positions[[2,10]] = copyofacell16.positions[[10,2]]
        
    else : print('Please enter acceptable disorder amount: "12.5", "25", "37.5", or "50"')
    
    return copyofacell16

def disorderSeriesMaker(cell):
    cell125 = swapSites(cell, '12.5')
    cartpos125 = cell125.get_positions()
    print('\n New positions (12.5%):\n')
    print(cartpos125)
#    cell125.write('cell125disorder', 'vasp')

    cell25 = swapSites(cell, '25')
    cartpos25 = cell25.get_positions()
    print('\n New positions (25%):\n')
    print(cartpos25)
#    cell25.write('cell25disorder', 'vasp')
    
    cell375 = swapSites(cell, '37.5')
    cartpos375 = cell.get_positions()
    print('\n New positions (37.5%):\n')
    print(cartpos375)
#    cell375.write('cell375disorder', 'vasp')

    cell50 = swapSites(cell, '50')
    cartpos50 = cell50.get_positions()
    print('\n New positions (50%):\n')
    print(cartpos50)
#    cell50.write('cell50disorder', 'vasp')

    print('\n Series has been made! Check the working directory for POSCARs \n')
    return
    