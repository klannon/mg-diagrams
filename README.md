# mg-diagrams
Some utilities for analyzing the postscript files Madgraph generates to show diagrams.

## Introduction
The main purpose of this code is to categorize the diagrams included in two different runs of Madgraph in terms of their orders (DIM6, QED, and QCD) and to figure out which diagrams are in common between the two runs and which only appear in one versus the other.  This is accomplished by looking through all of the `matrix*.ps` files in two directory trees, extracting the Feynman diagrams from those files and comparing them between the two runs.  A table summarizing the information is printed to the screen and a set of postscript files are optionally produced with the diagrams in different categories.

## Examples
Below are some examples of using the program.  These examples assume that all of the relevant postscript files are in subdirectories of `ttX-ttXJet_QED_QCD_comp` in your current working directory.

### Simple Printout
Just print a table summarizing the diagrams in the two files:
```
<kplmac 2196>./mgdiff.py ttX-ttXJet_QED_QCD_comp/ttH_HanV4-noOrderConstraints ttX-ttXJet_QED_QCD_comp/ttHJet_HanV4-noOrderConstraints 
A = ttX-ttXJet_QED_QCD_comp/ttH_HanV4-noOrderConstraints:
B = ttX-ttXJet_QED_QCD_comp/ttHJet_HanV4-noOrderConstraints:
DIM6 QED QCD   In A   In B   Common   A only   B only
   0   1   2     18     18       18        0        0
   0   1   3      0    230        0        0      230
   0   3   0     34     34       34        0        0
   0   3   1      0    492        0        0      492
   1   0   2      1      1        1        0        0
   1   0   3      0     21        0        0       21
   1   1   0     10     10       10        0        0
   1   1   1      0    150        0        0      150
   1   1   2     51     51       51        0        0
   1   1   3      0    746        0        0      746
   1   2   0     55     55       55        0        0
   1   2   1      0    768        0        0      768
   1   3   0     91     91       91        0        0
   1   3   1      0   1635        0        0     1635
Total           260   4302      260        0     4042
```

### Making Postscript Output
To create postscript output files, add `--ps PSFILE_BASE` to the command line, where `PSFILE_BASE` is some text you want at the start of the output postscript files.  The program will create a set of files named `PSFILE_BASE_DIM6?_QED?_QCD?_{common,a,b}.ps` to summarize the diagrams that are in common or unique to one of the two sets organized by the order of the diagrams.  If there are no diagrams in a particular category, that .ps file is not created.
```
<kplmac 2198>./mgdiff.py ttX-ttXJet_QED_QCD_comp/ttH_HanV4-noOrderConstraints ttX-ttXJet_QED_QCD_comp/ttHJet_HanV4-noOrderConstraints --ps ttH_0_vs_1
A = ttX-ttXJet_QED_QCD_comp/ttH_HanV4-noOrderConstraints:
B = ttX-ttXJet_QED_QCD_comp/ttHJet_HanV4-noOrderConstraints:
DIM6 QED QCD   In A   In B   Common   A only   B only
   0   1   2     18     18       18        0        0
   0   1   3      0    230        0        0      230
   0   3   0     34     34       34        0        0
   0   3   1      0    492        0        0      492
   1   0   2      1      1        1        0        0
   1   0   3      0     21        0        0       21
   1   1   0     10     10       10        0        0
   1   1   1      0    150        0        0      150
   1   1   2     51     51       51        0        0
   1   1   3      0    746        0        0      746
   1   2   0     55     55       55        0        0
   1   2   1      0    768        0        0      768
   1   3   0     91     91       91        0        0
   1   3   1      0   1635        0        0     1635
Total           260   4302      260        0     4042
<kplmac 2199>ls *.ps
ttH_0_vs_1_DIM60_QED1_QCD2_common.ps	ttH_0_vs_1_DIM61_QED0_QCD2_common.ps	ttH_0_vs_1_DIM61_QED1_QCD2_common.ps	ttH_0_vs_1_DIM61_QED3_QCD0_common.ps
ttH_0_vs_1_DIM60_QED1_QCD3_b.ps		ttH_0_vs_1_DIM61_QED0_QCD3_b.ps		ttH_0_vs_1_DIM61_QED1_QCD3_b.ps		ttH_0_vs_1_DIM61_QED3_QCD1_b.ps
ttH_0_vs_1_DIM60_QED3_QCD0_common.ps	ttH_0_vs_1_DIM61_QED1_QCD0_common.ps	ttH_0_vs_1_DIM61_QED2_QCD0_common.ps
ttH_0_vs_1_DIM60_QED3_QCD1_b.ps		ttH_0_vs_1_DIM61_QED1_QCD1_b.ps		ttH_0_vs_1_DIM61_QED2_QCD1_b.ps
```

## Shortcomings
This code was hacked together so it's far from perfect.  Here are the known shortcomings:
* I'm only paying attention to the DIM6, QED, and QCD couplings.  If there are others (FCNC?) they are ignored.  In other words, it's pretty much specific to the dim6top model.
* This code will not compare SMEFT@NLO to dim6top because it's not smart enough to map NP=2 to DIM6=1.  That would be a straightforward modifications however.
* The code assumes that unless otherwise specified, a diagram has DIM6=1, QED=0, and QCD=0.  This is because some of the diagrams I was looking at omited the "DIM6" tag when DIM6=1.  I don't know why that was the case nor why it was only some of the runs but not all of them.  If you try to use this on a case where omitting DIM6 actually means DIM6=0, etc. this code will fail.
