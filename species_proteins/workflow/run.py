from bioservices import *
u = UniProt()
f = u.get_fasta("P32321")
print("Test fasta print!")
print(f)