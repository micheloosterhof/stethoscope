#!/usr/bin/env python
# #pypy3

from collections import Counter, defaultdict
import math
import random
import sys
from typing import Dict, List

import gematria
import lp_section_data as lp

# import totient() method from sympy
import sympy
from sympy.ntheory.factor_ import totient, reduced_totient

from lib import *

g = gematria.gematria

djubei =[ 23,11,1,17,18,10 ]

# test alphabet of first letters of each word

def first_letter_of_word():
    for i in [lp.section1, lp.section2, lp.section3, lp.section4,
    lp.section5, lp.section6, lp.section7, lp.section8,
    lp.section9, lp.section10, lp.section11, lp.section12,
    lp.section13 ]:
        firstrune=[]
        for j in i["all_words"]:
            firstrune.append(j[0])
        print(firstrune)
        firstletter=[]
        for r in firstrune:
            firstletter.append(g.rune_to_position_forward_dict[r])
        print(ioc(firstletter))

s1="".join(lp.section1["all_words"])
s2="".join(lp.section2["all_words"])
s3="".join(lp.section3["all_words"])
s4="".join(lp.section4["all_words"])
s5="".join(lp.section5["all_words"])
s6="".join(lp.section6["all_words"])
s7="".join(lp.section7["all_words"])
s8="".join(lp.section8["all_words"])
s9="".join(lp.section9["all_words"])
s10="".join(lp.section10["all_words"])
s11="".join(lp.section11["all_words"])
s12="".join(lp.section12["all_words"])
s13="".join(lp.section13["all_words"])
s=s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+s11+s12+s13
sl = list(s)
segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13]

# RL is a random rune list same size as all the other runes
rl = []
for i in range(0, len(s)):
   rl.append(random.randrange(0,MAX))

# rsegments are random lists, same size as the LP
rsegments = []
for i in segments:
    l = len(i)
    f = prime_factors(l)
    r = []
    for i in range(0, l):
        r.append(random.randrange(0,MAX))
    rsegments.append(r)

# GL are the runes in 0-28 format, in one big list
gl = []
for i in sl:
     gl.append(g.rune_to_position_forward_dict[i])

# SGL are the runes in 0-28 format by segment, list of a list by chapter
sgl = []
for i in segments:
    bgl = []
    for j in i:
        bgl.append(g.rune_to_position_forward_dict[j])
    sgl.append(bgl)



def overlapping_permutations(ciphertext):
    """
    """
    length = 4
    sequences = {}

    for i in range(0,len(ciphertext)-length):
        # seq = f"{ciphertext[i]}-{ciphertext[i+1]}-{ciphertext[i+2]}-{ciphertext[i+3]}-{ciphertext[i+4]}"
        seq = f"{ciphertext[i]}-{ciphertext[i+1]}-{ciphertext[i+2]}-{ciphertext[i+3]}"
        seq = f"{ciphertext[i]}-{ciphertext[i+1]}-{ciphertext[i+2]}"
        seq = f"{ciphertext[i]}-{ciphertext[i+1]}"
        if seq in sequences.keys():
            sequences[seq] += 1
        else:
            sequences[seq] = 1
        
    #print(sequences)
    print(sorted( ((v,k) for k,v in sequences.items()), reverse=True))


#bigram_diagram(diffstream(gl))

print("djubei")
print(find(djubei,gl))

print(isomorph(gl,min=6))

N=len(sgl)
p = primes(100000)
for i in range(0,N):
  gl = sgl[i]
  print(f"#### segment {i+1} ######")
  print(f"len {len(gl)} factors:{prime_factors(len(gl))}" )
  

  #for j in range(i,N):
  #    print(f"chi {i}-{j}: {chi(sgl[i],sgl[j])*MAX}")
  #    print(f"rand chi {i}-{j}: {chi(sgl[i],rsegments[j])*MAX}")

  english_output(gl, limit=20)

  doublets(gl, trace=True)

  #print("kappa test")
  #kappa(gl)

  #run_test2(gl)
  #run_test3(gl)

  print(f"#### segment {i+1} bruteforce autokey ######")
  #bruteforce_autokey(gl,     maxkeylength=4)

  print(f"#### segment {i+1} IOC's #######")
  print(f" ioc={ioc(gl):.3f}")
  print(f" ioc2={ioc2(gl,cut=0):.3f} ioc2a={ioc2(gl,cut=1):.3f}, ioc2b={ioc2(gl,cut=2):.3f}")
  print(f" ioc3={ioc3(gl,cut=0):.3f} ioc3a={ioc3(gl,cut=1):.3f}, ioc3b={ioc3(gl,cut=2):.3f}, ioc3c={ioc3(gl,cut=3):.3f}")
  # print(f" ioc4={ioc4(gl,cut=0):.4f} ioc4a={ioc4(gl,cut=1):.4f}, ioc4b={ioc4(gl,cut=2):.4f}, ioc4c={ioc4(gl,cut=4):.4f}")

  print(f"#### segment {i+1} ISOMORPH's ######")
  print(f" isomorphs length 3: {isomorph2(gl,min=3,max=3)}")
  print(f" isomorphs length 4: {isomorph2(gl,min=4,max=4)}")
  print(f" isomorphs length 5: {isomorph2(gl,min=5,max=5)}")

