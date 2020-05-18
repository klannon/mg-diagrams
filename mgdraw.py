#! /usr/bin/env python3

def transform_diagram(diagram, x0, y0, scale_w, scale_h):

    # Break the diagram into its lines
    lines = diagram.splitlines()

    # Now rewrite the diagram relative to the origin
    scale_diagram = ''
    for line in lines:
        if line.strip().endswith('show'):
            scale_diagram+=line
        elif line.strip().endswith('Fblob'):
            tokens = line.strip().split()
            tokens[0] = '{:.4f}'.format(scale_w*float(tokens[0])+x0)
            tokens[1] = '{:.4f}'.format(scale_h*float(tokens[1])+y0)
            tokens[2] = '{:.4f}'.format(((scale_w+scale_h)/2)*float(tokens[2]))
            scale_diagram+=(' '.join(tokens))
        elif line.strip().endswith('moveto'):
            tokens = line.strip().split()
            tokens[0] = '{:.4f}'.format(scale_w*float(tokens[0])+x0)
            tokens[1] = '{:.4f}'.format(scale_h*float(tokens[1])+y0)
            scale_diagram+=(' '.join(tokens))
        else:
            tokens = line.strip().split()
            tokens[0] = '{:.4f}'.format(scale_w*float(tokens[0])+x0)
            tokens[1] = '{:.4f}'.format(scale_h*float(tokens[1])+y0)
            tokens[2] = '{:.4f}'.format(scale_w*float(tokens[2])+x0)
            tokens[3] = '{:.4f}'.format(scale_h*float(tokens[3])+y0)
            scale_diagram+=(' '.join(tokens))
        scale_diagram+='\n'

    return scale_diagram

def write_header(outfile, n_pages):
    header = '''\
%!PS-Adobe-2.0
%%BoundingBox: -20 -20 450  450 
%%DocumentFonts: Helvetica
%%Pages:  {} 
%
% Hacked up from the Madgraph output by Kevin Lannon
%
/Fnopoints 10 def 
/Fr 2.5 def 
/pi 3.14159265359 def

/Frmod {{dup 360 div floor 360 mul sub}} def
/Fsign {{0 ge {{1}} {{-1}} ifelse}} def

/Fbasis
{{/Fby exch def /Fbx exch def /Fdist Fbx Fbx
mul Fby Fby mul add sqrt def /Fxl Fbx Fdist
div Fr mul def /Fyl Fby Fdist div Fr mul def
/Fxt Fby Fdist div Fr mul def /Fyt Fbx neg
Fdist div Fr mul def }} def

/Fstraight 
{{/Fshape exch def /Ftype exch def /Fy2 exch
def /Fx2 exch def /Fy1 exch def /Fx1 exch def
Fx2 Fx1 sub Fy2 Fy1 sub Fbasis /Fttype 1
Ftype 2 mod 2 mul abs sub def Ftype 0 ge
{{/Fddist Fdist Fr div 2 div def /Fn Fddist round
def Ftype 1 gt {{/Fn Fn Fddist Fn sub Fsign
add def}} if}} {{/Fn Fdist Fr div 2 div round 2
mul def}} ifelse Fx1 Fy1 moveto 0 1 Fnopoints
Fn mul {{/Fi exch def Fshape lineto }} for
stroke }} def

/Floop
{{/Fshape exch def /Fe exch def /Ftype exch
def /Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def /Flam 1 Fe Fe mul sub 2 div Fe
div def /Fxc Fx1 Fx2 Flam Fy2 Fy1 sub mul add
add 2 div def /Fyc Fy1 Fy2 Flam Fx1 Fx2 sub
mul add add 2 div def /Frr Fx1 Fxc sub dup
mul Fy1 Fyc sub dup mul add sqrt def /Fth1
Fy1 Fyc sub Fx1 Fxc sub atan def /Fth2 Fy2
Fyc sub Fx2 Fxc sub atan def Fe 0 lt Fth2
Fth1 lt and {{/Fth1 Fth1 360 sub def}} if Fe 0
gt Fth2 Fth1 gt and {{/Fth2 Fth2 360 sub def}}
if /Fdth Fth2 Fth1 sub Fsign def /Fttype 1
Ftype 2 mod abs 2 mul sub def Ftype 0 ge
{{/Fddist Fth2 Fth1 sub abs 180 div pi mul Frr
mul Fr div def /Fn Fddist round def Ftype 1
gt {{/Fn Fn Fddist Fn sub Fsign add def}} if}}
{{/Fn Fth2 Fth1 sub abs 180 div pi mul Frr mul
Fr div 2 div round 2 mul def}} ifelse Fx1 Fy1
moveto 0 1 Fnopoints Fn mul {{/Fi exch def
/Fth Fth1 Fth2 Fth1 sub Fi mul Fnopoints div
Fn div add Frmod def Fth sin neg Fdth mul Fth
cos Fdth mul Fbasis Fshape lineto }} for
stroke }} def

/Farrow
{{ moveto Fxt Fxl sub Fyt Fyl sub
rlineto Fxl 2 mul Fxt sub Fyl 2 mul Fyt sub
rlineto Fxl 2 mul Fxt add neg Fyl 2 mul Fyt
add neg rlineto fill }} def

/Fphoton
{{{{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div Fn
div Fxt Fi 360 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add Fy1 Fy2 Fy1 sub
Fi mul Fnopoints div Fn div Fyt Fi 360 mul
Fnopoints div Frmod sin mul Fttype mul 2 div
add add }} Fstraight }} def

/Fphotonr
{{{{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div Fn
div Fxt Fi 180 mul Fnopoints div Frmod sin
mul Fttype mul 1 div add add Fy1 Fy2 Fy1 sub
Fi mul Fnopoints div Fn div Fyt Fi 180 mul
Fnopoints div Frmod sin mul Fttype mul 1 div
add add }} Fstraight }} def

/Fphotond
{{{{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div Fn
div Fxt Fi 360 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add Fy1 Fy2 Fy1 sub
Fi mul Fnopoints div Fn div Fyt Fi 360 mul
Fnopoints div Frmod sin mul Fttype mul 2 div
add add }} Fstraight Fx1
Fx2 add 2 div Fy1 Fy2 add 2 div Farrow}} def

/Fphotonl
{{exch dup 3 1 roll 0 ge {{{{ Fxc Fth cos Frr
mul Fxt Fi 180 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add Fyc Fth sin Frr
mul Fyt Fi 180 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add }}}} {{{{ Fxc Fth
cos Frr mul Fxt 1 Fi 180 mul Fnopoints div
Frmod cos sub mul Fttype mul 2 div add add
Fyc Fth sin Frr mul Fyt 1 Fi 180 mul
Fnopoints div Frmod cos sub mul Fttype mul 2
div add add }}}} ifelse Floop }} def

/Fgluon
{{2 sub {{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div
Fn div Fxt 1 Fi 180 mul Fnopoints div cos sub
mul Fttype mul Fxl Fi 180 mul Fnopoints div
sin mul add add add Fy1 Fy2 Fy1 sub Fi mul
Fnopoints div Fn div Fyt 1 Fi 180 mul
Fnopoints div cos sub mul Fttype mul Fyl Fi
180 mul Fnopoints div sin mul add add add }}
Fstraight }} def

/Fgluonr
{{2 sub {{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div
Fn div Fxt 0 Fi 120 mul Fnopoints div cos sub
mul Fttype mul Fxl Fi 120 mul Fnopoints div
sin mul add add add Fy1 Fy2 Fy1 sub Fi mul
Fnopoints div Fn div Fyt 0 Fi 120 mul
Fnopoints div cos sub mul Fttype mul Fyl Fi
120 mul Fnopoints div sin mul add add add }}
Fstraight }} def


/Fgluonl
{{exch 2 sub exch {{ Fxc Fth cos Frr mul Fxt 1
Fi 180 mul Fnopoints div cos sub mul Fttype
mul Fxl Fi 180 mul Fnopoints div sin mul add
add add Fyc Fth sin Frr mul Fyt 1 Fi 180 mul
Fnopoints div cos sub mul Fttype mul Fyl Fi
180 mul Fnopoints div sin mul add add add }}
Floop}} def

/Ffermion
{{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def newpath Fx2 Fx1 sub Fy2 Fy1 sub
Fbasis Fx1 Fy1 moveto Fx2 Fy2 lineto stroke Fx1
Fx2 add 2 div Fy1 Fy2 add 2 div Farrow }} def

/Fscalar
{{newpath moveto lineto stroke}} def

/Ffermionl
{{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def newpath /Flam 1 Fe
Fe mul sub 2 div Fe div def /Fxc Fx1 Fx2 Flam Fy2
Fy1 sub mul add add 2 div def /Fyc Fy1 Fy2
Flam Fx1 Fx2 sub mul add add 2 div def /Frr
Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul add
sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub atan
def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan def Fe
0 lt Fth2 Fth1 lt and {{/Fth1 Fth1 360 sub
def}} if Fe 0 gt Fth2 Fth1 gt and {{/Fth2 Fth2
360 sub def}} if /Fthc Fth1 Fth2 add 2 div def
Fxc Fyc Frr Fth1 Fth2 Fe 0 gt {{arcn}} {{arc}}
ifelse stroke Fthc sin Fe 0 lt {{neg}} if Fthc
cos Fe 0 gt {{neg}} if Fbasis Fxc Fthc cos Frr
mul add Fyc Fthc sin Frr mul add Farrow }} def

/Fscalarl
{{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def newpath /Flam 1 Fe
Fe mul sub 2 div Fe div def /Fxc Fx1 Fx2 Flam Fy2
Fy1 sub mul add add 2 div def /Fyc Fy1 Fy2
Flam Fx1 Fx2 sub mul add add 2 div def /Frr
Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul add
sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub atan
def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan def Fe
0 lt Fth2 Fth1 lt and {{/Fth1 Fth1 360 sub
def}} if Fe 0 gt Fth2 Fth1 gt and {{/Fth2 Fth2
360 sub def}} if /Fthc Fth1 Fth2 add 2 div def
Fxc Fyc Frr Fth1 Fth2 Fe 0 gt {{arcn}} {{arc}}
ifelse stroke }} def

/Fblob 
{{/Fshade exch def newpath Fr mul 0 360 arc gsave
1 Fshade sub setgray fill grestore stroke}} def

/Fhiggs
{{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def gsave Fx1 Fx2 sub dup mul
Fy1 Fy2 sub dup mul add sqrt dup Fr div
2 div round 2 mul 1 add div /dashln exch def
[dashln dashln] 0 setdash Fx1 Fy1 moveto
Fx2 Fy2 lineto stroke grestore}} def


/Fhiggsd
{{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def gsave Fx1 Fx2 sub dup mul
Fy1 Fy2 sub dup mul add sqrt dup Fr div
2 div round 2 mul 1 add div /dashln exch def
[dashln dashln] 0 setdash Fx1 Fy1 moveto
Fx2 Fy2 lineto stroke grestore Fx1 Fx2 add 2 div
Fy1 Fy2 add 2 div Farrow}} def

/Fhiggsl
{{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def /Flam gsave 1 Fe
Fe mul sub 2 div Fe div def /Fxc Fx1 Fx2 Flam
Fy2 Fy1 sub mul add add 2 div def /Fyc Fy1
Fy2 Flam Fx1 Fx2 sub mul add add 2 div def
/Frr Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul
add sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub
atan def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan
def Fe 0 lt Fth2 Fth1 lt and {{/Fth1 Fth1 360
sub def}} if Fe 0 gt Fth2 Fth1 gt and {{/Fth2
Fth2 360 sub def}} if /Fthc Fth1 Fth2 add 2
div def Fxc Fyc Frr Fth1 Fth2 Fe 0 gt {{arcn}}
{{arc}} ifelse Fth2 Fth1 sub abs 180 div pi mul
Frr mul dup Fr div 2 div round 2 mul 1 add
div /dashln exch def [dashln dashln] 0
setdash stroke grestore}} def

/Fghost
{{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def Fx2 Fx1 sub Fy2 Fy1 sub Fbasis
/Fn Fx1 Fx2 sub dup mul Fy1 Fy2 sub dup mul
add sqrt Fr div round def 0 1 Fn {{/Fi exch
def Fx2 Fx1 sub Fi Fn div mul Fx1 add Fy2 Fy1
sub Fi Fn div mul Fy1 add Fr 10 div 0 360 arc
fill}} for Fx1 Fx2 add 2 div Fy1 Fy2 add 2 div
Farrow }} def

/Fghostl
{{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def /Flam 1 Fe Fe mul
sub 2 div Fe div def /Fxc Fx1 Fx2 Flam Fy2
Fy1 sub mul add add 2 div def /Fyc Fy1 Fy2
Flam Fx1 Fx2 sub mul add add 2 div def /Frr
Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul add
sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub atan
def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan def Fe
0 lt Fth2 Fth1 lt and {{/Fth1 Fth1 360 sub
def}} if Fe 0 gt Fth2 Fth1 gt and {{/Fth2 Fth2
360 sub def}} if /Fthc Fth1 Fth2 add 2 div def
/Fn Fth2 Fth1 sub abs 180 div pi mul Frr mul
Fr div round def 0 1 Fn {{/Fi exch def Fth2
Fth1 sub Fi Fn div mul Fth1 add dup cos Frr
mul Fxc add exch sin Frr mul Fyc add Fr 10
div 0 360 arc fill}} for Fthc sin Fe 0 lt
{{neg}} if Fthc cos Fe 0 gt {{neg}} if Fbasis Fxc
Fthc cos Frr mul add Fyc Fthc sin Frr mul add
Farrow }} def

/Fproton
{{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def Fx2 Fx1 sub Fy2 Fy1 sub Fbasis
Fx1 Fxt 2 div add Fy1 Fyt 2 div add moveto
Fx2 Fxt 2 div add Fy2 Fyt 2 div add lineto
Fx1 Fxt 2 div sub Fy1 Fyt 2 div sub moveto
Fx2 Fxt 2 div sub Fy2 Fyt 2 div sub lineto
Fx1 Fx2 add 2 div Fxt Fxl sub add Fy1 Fy2 add
2 div Fyt Fyl sub add moveto Fx1 Fx2 add Fxl
add 2 div Fy1 Fy2 add Fyl add 2 div lineto
Fx1 Fx2 add 2 div Fxt Fxl add sub Fy1 Fy2 add
2 div Fyt Fyl add sub lineto stroke}} def

/Fmax {{2 copy lt {{exch}} if pop}} def
/Fstart {{gsave currentpoint
translate 0 0 moveto 0 rm Fr 4 mul
scalefont setfont}} def
/Fsubspt {{gsave currentpoint Fcharheight 5 div
sub translate 0.6 0.6 scale 0 0 moveto 0}} def
/Fsupspt {{gsave currentpoint Fcharheight 0.6 mul
add translate 0.6 0.6 scale 0 0 moveto 0}} def
/Feend {{currentpoint pop Fmax 0.6 mul
grestore currentpoint pop add Fmax}} def
/Fendd {{pop grestore}} def
/Fshow {{exch 0 moveto show currentpoint pop}} def
/Fcharheight
{{gsave (X) true charpath flattenpath pathbbox
3 1 roll pop sub exch pop grestore}} def

/Foverline
{{exch 0 moveto gsave dup true charpath
flattenpath pathbbox Fcharheight 10 div dup
2 div setlinewidth add dup 4
1 roll newpath moveto pop lineto stroke
grestore show currentpoint pop}} def

/Funderline 
{{exch 0 moveto gsave dup true charpath
flattenpath pathbbox pop exch Fcharheight
10 div dup 2 div setlinewidth
sub dup 3 1 roll newpath moveto lineto stroke
grestore show currentpoint pop}} def

/rm /Times-Roman findfont def
/it /Times-Italic findfont def
/sy /Symbol findfont def

/wedge 
/{{ /ystop exch def /xstop exch def /ystart exch def
/xstart exch def /delx xstop xstart sub def /dely 
ystop ystart sub def /dist delx dup mul dely dup 
mul add sqrt def /halfdist dist 2 div def
/angle dely delx atan def xstart ystart moveto 
angle rotate 0 halfdist rlineto dist halfdist
neg rlineto dist neg halfdist neg rlineto 
0 halfdist rlineto }}def

/ch_photon
{{/ystop exch def /xstop exch def /ystart exch def
/xstart exch def /xmid xstart xstop add 2 div def
/ymid ystart ystop add 2 div def
/dx xstop xstart sub def /dy ystop ystart sub def
/length dx dup mul dy dup mul add sqrt def
/xunit dx length div def /yunit dy length div def
/x1 xmid xunit -4.8 mul add def
/y1 ymid yunit -4.8 mul add def
/x2 xmid xunit 4.8 mul add def
/y2 ymid yunit 4.8 mul add def
/y2 ymid yunit 4.8 mul add def
xstart ystart x1 y1 1 Fphoton 
x2 y2 xstop ystop 1 Fphoton
/x1 xmid xunit -5.2 mul add def 
/y1 ymid yunit -5.2 mul add def
/x2 xmid xunit 5.2 mul add def 
/y2 ymid yunit 5.2 mul add def
gsave x1 y1 x2 y2 wedge fill grestore}} def

/ch_higgs 
{{ /ystop exch def /xstop exch def /ystart exch def
/xstart exch def 
/xmid xstart xstop add 2 div def
/ymid ystart ystop add 2 div def
/dx xstop xstart sub def /dy ystop ystart sub def
/length dx dup mul dy dup mul add sqrt def
/xunit dx length div def /yunit dy length div def
/x1 xmid xunit -4.8 mul add def 
/y1 ymid yunit -4.8 mul add def
/x2 xmid xunit 4.8 mul add def 
/y2 ymid yunit 4.8 mul add def
xstart ystart x1 y1 Fhiggs 
x2 y2 xstop ystop Fhiggs
/x1 xmid xunit -5.2 mul add def
/y1 ymid yunit -5.2 mul add def
/x2 xmid xunit 5.2 mul add def
/y2 ymid yunit 5.2 mul add def
gsave x1 y1 x2 y2 wedge fill grestore}} def
% End of the header
'''.format(n_pages)

    outfile.write(header)

def start_new_page(outfile, i_page, n_pages):

    if i_page > 1:
        outfile.write('showpage\n')

    text = '''\
%%Page:       {0}       {0}
%%PageBoundingBox:-20 -20 600 800
%%PageFonts: Helvetica

/Helvetica findfont 9 scalefont setfont
 50         770  moveto
 () show
 525         770  moveto
 (page {0}/{1}) show
 260         50  moveto
 (Diagrams made by MadGraph5_aMC@NLO) show
'''.format(i_page,n_pages)

    outfile.write(text)

def end_document(outfile):

    outfile.write('%%trailer\n')

def write_diagrams(outfile, diagrams):

    # I'm hardcoding 6 per page because I want to.
    target_w = 216
    target_h = 181.5
    initial_x = 67
    initial_y = 560
    spacing_x = 275
    spacing_y = 220
    cols_per_page = 2
    rows_per_page = 3
    diagrams_per_page = cols_per_page * rows_per_page
    
    import math
    n_pages = math.ceil(len(diagrams)/diagrams_per_page)

    # Start the file
    write_header(outfile, n_pages)

    import mgparse
    i_page = 1
    for i,d in enumerate(diagrams):
        if i % diagrams_per_page == 0:
            start_new_page(outfile,i_page,n_pages)
            i_page+=1

        # Transform the diagram to fit on the page
        size = mgparse.get_diagram_size(d)
        scale_w = target_w/size[0]
        scale_h = target_h/size[1]
        x0 = initial_x + (i % cols_per_page)*spacing_x
        y0 = initial_y - (i % rows_per_page)*spacing_y

        dt = transform_diagram(d,x0, y0, scale_w, scale_h)

        outfile.write(dt)

    end_document(outfile)


if __name__ == "__main__":

    # Set up the command line parser
    import argparse
    parser = argparse.ArgumentParser(description=('Outputs Feynman diagrams in PS format.'))
    parser.add_argument('ps_file',
                        help='Input file')

    args = parser.parse_args()

    # Open the file and try to parse it
    import mgparse
    with open(args.ps_file) as infile:
        diagrams = mgparse.get_diagrams_from_file(infile)                
        
    # Print some basic info about diagrams found
    print("Diagrams found:")
    for o in sorted(diagrams.keys()):
        print('{} diagrams with DIM6 = {}, QED = {}, QCD = {}'.format(len(diagrams[o]),
                                                                      *o))
    d = diagrams[list(diagrams.keys())[0]][0]                             
    size = mgparse.get_diagram_size(d)
    print('Diagram size: w={:.2f},h={:.2f}'.format(*size))

    scale_w = 100./size[0]
    scale_h = 300./size[1]

    scaled_d = transform_diagram(d,100,100,scale_w,scale_h)
    print(scaled_d)

    size = mgparse.get_diagram_size(scaled_d)
    print('Diagram size: w={:.2f},h={:.2f}'.format(*size))

    # Test writing the document
    with open('test.ps','w') as outfile:
        write_diagrams(outfile, diagrams[list(diagrams.keys())[0]])
