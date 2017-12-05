from src import IO as io
from src import LaTeX as ltx
from src import text as txt_lib

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input', metavar='input filepath', type=str, help='an integer for the accumulator')
parser.add_argument("-c", action='store_true', default=False, help="Prints the functions called within functions")
parser.add_argument("-f", action='store_true', default=False, help="Creates a tikz concept map of the subroutines and functions in the file")

args = parser.parse_args()


filepath = io.folder_correct(args.input)
ltxt = io.open_read_close(filepath)


subroutines, sub_beg_indices, _ = txt_lib.splicing(ltxt, "subroutine", "(", "end subroutine")
calls = {i:txt_lib.splicing(subroutines[i][1][:], "call", "(", ")", d_on=False)[0] for i in subroutines}
functions, sub_beg_indices, _ = txt_lib.splicing(ltxt, "function", "(", "end function", start_d_index=len(subroutines)+1)
for i in functions:
    calls[i] = txt_lib.splicing(functions[i][1][:], "call", "(", ")", d_on=False)[0]

io.printer(subroutines, "Subroutines", calls, True, False)
io.printer(functions, "Functions", calls, True, False)

if args.f:
    flow_chart_text = ltx.flow_chart(filepath, subroutines, calls=False, functions=False)
    
    tex_folderpath =  '/home/oem/Documents/PhD/Code/flow_chart_creator/flow_charts/'
    tex_folderpath = io.folder_correct(tex_folderpath)
    mod_name = txt_lib.path2name(filepath).replace(" ", "_")
    tex_folderpath += mod_name
    tex_folderpath = io.folder_correct(tex_folderpath)
    io.check_mkdir(tex_folderpath)
    tex_filepath = tex_folderpath+"flow.tex"
    
    io.Save_Flow(tex_filepath, flow_chart_text)