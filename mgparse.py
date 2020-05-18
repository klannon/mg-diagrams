#! /usr/bin/env python3

def read_header(line_iter):
    # Read the first part of the file to extract the header
    line = next(line_iter)
    header = ''
    while not line.startswith('% End of the header'):
        header+=line
        line=next(line_iter)
    else:
        header+=line

    return header

def find_page_start(line_iter):
    import itertools
    try:
        # Read until we find the string "(page " and then skip two more
        line = next(line_iter)
        while not '(page ' in line:
            line=next(line_iter)
        else:
            # Fancy code to skip ahead two more lines
            next(itertools.islice(line_iter, 2, 2), None)
            return True
        
    except StopIteration:
        return False

def read_diagram(line_iter):
    # Read until we find the "( diagram " label
    diagram = ''
    line = next(line_iter)

    # We reached the end of the page.  Should always be the first
    # thing we read if we're going to read it.
    if line.strip().startswith('showpage'):
        return None
    
    while not '( diagram ' in line:
        diagram+=line
        line=next(line_iter)
    else:
        # Slurp up two more lines
        diagram+=next(line_iter)
        order_line = next(line_iter)
        orders=extract_orders(order_line)
        diagram+='(DIM6={}, QED={}, QCD={})   show\n'.format(*orders)

    return diagram

def correct_coordinates(raw_diagram):

    # Break the diagram into its lines
    lines = raw_diagram.splitlines()

    # Find the (1) label.  Use this to define the relative coordinate system
    index = -1
    for i, line in enumerate(lines):
        if line.strip() == '(1)   show':
            index = i-1
            break
    tokens = lines[index].strip().split()
    x0 = float(tokens[0])
    y0 = float(tokens[1])

    # Now rewrite the diagram relative to the origin
    corr_diagram = ''
    for line in lines:
        if line.strip().endswith('show'):
            corr_diagram+=line
        elif (line.strip().endswith('Fblob') or
              line.strip().endswith('moveto')):
            tokens = line.strip().split()
            tokens[0] = '{:.4f}'.format(float(tokens[0])-x0)
            tokens[1] = '{:.4f}'.format(float(tokens[1])-y0)
            corr_diagram+=(' '.join(tokens))
        else:
            tokens = line.strip().split()
            tokens[0] = '{:.4f}'.format(float(tokens[0])-x0)
            tokens[1] = '{:.4f}'.format(float(tokens[1])-y0)
            tokens[2] = '{:.4f}'.format(float(tokens[2])-x0)
            tokens[3] = '{:.4f}'.format(float(tokens[3])-y0)
            corr_diagram+=(' '.join(tokens))
        corr_diagram+='\n'

    return corr_diagram

def get_diagram_size(diagram):

    # Break the diagram into its lines
    lines = diagram.splitlines()

    min_x = 9e100
    min_y = 9e100
    max_x = -9e100
    max_y = -9e100
    for line in lines:
        if line.strip().endswith('show'):
            continue
        else:
            tokens = line.strip().split()
            x = float(tokens[0])
            y = float(tokens[1])
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y                
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if not (line.strip().endswith('Fblob') or
              line.strip().endswith('moveto')):
                x = float(tokens[2])
                y = float(tokens[3])
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y                
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y

    return (max_x - min_x, max_y - min_y)


# OK, so the coordinates on some diagrams are just a little off, so
# let's get a form of this diagram that replaces the coordinates with
# arbitrary labels to facilitate comparisons.
def get_comparable(diagram):
    # Keep a list of all the points we've seen so we can use them when
    # they're referred to in this diagram
    point_map = {}
    i = 0

    comp_diagram = ''
    lines = diagram.splitlines()

    for line in lines:
        if line.strip().endswith('show'):
            comp_diagram+=line
        elif (line.strip().endswith('Fblob') or
              line.strip().endswith('moveto')):
            tokens = line.strip().split()
            p = ('{:.4f}'.format(float(tokens.pop(0))),
                 '{:.4f}'.format(float(tokens.pop(0))))
            if p in point_map:
                plabel = point_map[p]
            else:
                plabel = 'P{}'.format(i)
                point_map[p] = plabel
                i+=1

            if line.strip().endswith('Fblob'):
                tokens[0] = 'A'
                tokens[1] = 'B'

            tokens[0:0]=[plabel]
            comp_diagram+=(' '.join(tokens))
        else:
            tokens = line.strip().split()
            p0 = ('{:.4f}'.format(float(tokens.pop(0))),
                 '{:.4f}'.format(float(tokens.pop(0))))
            if p0 in point_map:
                plabel0 = point_map[p0]
            else:
                plabel0 = 'P{}'.format(i)
                point_map[p0] = plabel0
                i+=1
            p1 = ('{:.4f}'.format(float(tokens.pop(0))),
                 '{:.4f}'.format(float(tokens.pop(0))))
            if p1 in point_map:
                plabel1 = point_map[p1]
            else:
                plabel1 = 'P{}'.format(i)
                point_map[p1] = plabel1
                i+=1

            tokens[0:0] = [plabel0,plabel1]
            comp_diagram+=(' '.join(tokens))
            
        comp_diagram+='\n'
    
    return comp_diagram

def extract_orders(diagram):
    # Break the diagram into its lines
    lines = diagram.splitlines()

    # The line we want is the last one
    order_line = lines[-1]

    order_line = order_line.partition(')')[0]
    order_line = order_line.lstrip(' (')

    orders = {'DIM6':1, 'QED':0, 'QCD':0}
    for x in order_line.split(','):
        tokens = x.strip().split('=')
        orders.update({tokens[0]:int(tokens[1])})

    return (orders['DIM6'],orders['QED'],orders['QCD'])

def get_diagrams_from_file(infile):

    diagrams = {}
    
    # Prepare to iterate over the lines in the file
    lines = iter(infile)

    # Find the header.  Could be useful to have it for later.
    header = read_header(lines)

    # Get to the top of a page
    while find_page_start(lines):

        # Read the first diagram into a string
        diagram = read_diagram(lines)
        while (diagram):
            corr_diagram = correct_coordinates(diagram)
            orders = extract_orders(corr_diagram)

            if orders in diagrams:
                diagrams[orders].append(corr_diagram)
            else:
                diagrams[orders] = [corr_diagram]
                    
            # Try reading the next diagram
            diagram = read_diagram(lines)

    return diagrams


if __name__ == "__main__":

    # Set up the command line parser
    import argparse
    parser = argparse.ArgumentParser(description=('Gets the Feynman diagrams out of ' + 
                                                  'the .ps file Madgraph makes'))
    parser.add_argument('ps_file',
                        help='The file to analyze.')

    args = parser.parse_args()

    # Open the file and try to parse it
    with open(args.ps_file) as infile:
        diagrams = get_diagrams_from_file(infile)                
        
    # Print some basic info about diagrams found
    print("Diagrams found:")
    for o in sorted(diagrams.keys()):
        print('{} diagrams with DIM6 = {}, QED = {}, QCD = {}'.format(len(diagrams[o]),
                                                                      *o))
                                                                      
    size = get_diagram_size(diagrams[list(diagrams.keys())[0]][0])
    print('Diagram size: w={:.2f},h={:.2f}'.format(*size))
