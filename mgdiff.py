#! /usr/bin/env python3

import mgparse


if __name__ == "__main__":

    # Set up the command line parser
    import argparse
    parser = argparse.ArgumentParser(description=('Analyzes overlaps and differences in ' +
                                                  'two Madgraph runs'))
    parser.add_argument('dir_a',
                        help='First directory')

    parser.add_argument('dir_b',
                        help='Second directory')

    parser.add_argument('-p','--ps', metavar='PSFILE_BASE',
                        help=('Output various groups of diagrams to .ps files'+ 
                              ' starting with %(metavar)s'))

    args = parser.parse_args()

    # Get the list of all
    from pathlib import Path

    # Process all the matrix elements in dir_a
    diagrams_a = {} # Initially all diagrams in a, but will delete
                    # those in common with b
    counts_a = {} # Counts of diagrams per order in dir_a
    for pspath in Path(args.dir_a).glob('**/*.ps'):
        with pspath.open() as psfile:
            diags = mgparse.get_diagrams_from_file(psfile)
            for o in diags.keys():
                if o in diagrams_a.keys():
                    diagrams_a[o] += diags[o]
                    counts_a[o] += len(diags[o])
                else:
                    diagrams_a[o] = diags[o]
                    counts_a[o] = len(diags[o])

    # Now reconcile against what we find in dir_b.  For purposes of
    # not exploding the memory, let's not read all of dir_b into
    # memory and then start making lists of common and unique
    # diagrams.  Instead, let's build the final list directly.

    counts_b = {} # Number of diagrams in dir_b of different orders
    diagrams_common = {}  #In both
    diagrams_b = {} #Only in b
    for pspath in Path(args.dir_b).glob('**/*.ps'):
        with pspath.open() as psfile:
            diags = mgparse.get_diagrams_from_file(psfile)
            for o in diags.keys():
                # Tally number of diagrams in b
                if o in counts_b.keys():
                    counts_b[o] += len(diags[o])
                else:
                    counts_b[o] = len(diags[o])

                # Check the overlap between these diagrams and those in a
                if o in diagrams_a.keys():
                    # Check whether any of these diagrams match
                    for db in diags[o]:
                        db_comp = mgparse.get_comparable(db)
                        # Check in a for this diagram
                        for i,da in enumerate(diagrams_a[o]):
                            da_comp = mgparse.get_comparable(da)
                            if da_comp == db_comp:
                                # Found the match!
                                if o in diagrams_common.keys():
                                    diagrams_common[o].append(db)
                                else:
                                    diagrams_common[o] = [db]
                                # Since it's in both a and b, remove it
                                # from diagrams_a so what's left at the
                                # end will be just diagrams unique to a
                                del diagrams_a[o][i]
                                break
                        else:
                            # Not found in a, so this is unique to b
                            if o in diagrams_b.keys():
                                diagrams_b[o].append(db)
                            else:
                                diagrams_b[o] = [db]
                else:
                    # Diagrams_a is entirely missing this order of
                    # diagrams.  Add it to the "b-only" list.
                    if o in diagrams_b.keys():
                        diagrams_b[o] += diags[o]
                    else:
                        diagrams_b[o] = diags[o]

    # Print some basic info about diagrams found in dir_a
    print("A = {}:".format(args.dir_a))
    print("B = {}:".format(args.dir_b))
    total_a_all = 0
    total_b_all = 0
    total_common = 0
    total_a_only = 0
    total_b_only = 0

    print('DIM6 QED QCD   In A   In B   Common   A only   B only')
    for o in sorted(set(list(counts_a.keys())+list(counts_b.keys()))):
        if o in counts_a.keys():
            a_all = counts_a[o]
        else:
            a_all = 0
        
        total_a_all += a_all
        
        if o in counts_b.keys():
            b_all = counts_b[o]
        else:
            b_all = 0

        total_b_all += b_all

        if o in diagrams_a.keys():
            a_only = len(diagrams_a[o])
        else:
            a_only = 0

        total_a_only += a_only

        if o in diagrams_b.keys():
            b_only = len(diagrams_b[o])
        else:
            b_only = 0

        total_b_only += b_only

        if o in diagrams_common.keys():
            common = len(diagrams_common[o])
        else:
            common = 0
            
        total_common += common

        print('{:4d} {:3d} {:3d}   {:4d}   {:4d}   {:6d}   {:6d}   {:6d}'.format(
            *o, a_all, b_all, common, a_only, b_only))

    
    print('Total          {:4d}   {:4d}   {:6d}   {:6d}   {:6d}'.format(
        total_a_all, total_b_all, total_common, total_a_only, total_b_only))

    # Make the postscript output file if desired
    if args.ps:
        import mgdraw
        
        for o in diagrams_common.keys():
            if len(diagrams_common[o]) > 0:
                filename = '{}_DIM6{}_QED{}_QCD{}_common.ps'.format(args.ps,*o)
                with open(filename,'w') as outfile:
                    mgdraw.write_diagrams(outfile,diagrams_common[o])

        for o in diagrams_a.keys():
            if len(diagrams_a[o]) > 0:
                filename = '{}_DIM6{}_QED{}_QCD{}_a.ps'.format(args.ps,*o)
                with open(filename,'w') as outfile:
                    mgdraw.write_diagrams(outfile,diagrams_a[o])

        for o in diagrams_b.keys():
            if len(diagrams_b[o]) > 0:
                filename = '{}_DIM6{}_QED{}_QCD{}_b.ps'.format(args.ps,*o)
                with open(filename,'w') as outfile:
                    mgdraw.write_diagrams(outfile,diagrams_b[o])

