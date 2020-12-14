from source import ConcreteSlab

# Problem 2-30

slab=ConcreteSlab(8, 3000, 60000, 300)
slab.k_required()

slab.main_steel(0.0059)

#6 bars at 18" oc (A_s=0.29 in^2)
# slab.main_steel_spacing(18)
#6 bars at 18" oc is inadequate...

#5 bars at 14" oc (A_s=0.27 in^2)
slab.main_steel_spacing(14)
slab.new_effective_depth(5)

slab.st_steel()
#3 bars at 12" oc (A_s=0.11 in^2)
slab.st_steel_spacing(12)

print('\n')

# Problem 2-32

slab2=ConcreteSlab(13, 3000, 60000, 200)
slab2.k_required()
slab2.main_steel(0.0039)

#6 bars at 16" oc (A_s=0.33 in^2)
slab2.main_steel_spacing(16)
slab2.new_effective_depth(6)

slab2.st_steel()
#4 bars at 14" oc (A_s=0.17 in^2)
slab2.st_steel_spacing(14)
