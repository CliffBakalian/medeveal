\e empty string

P -> SP|S
W -> ### slidetype ###\nS\n### END ###
S -> LS|L
L -> + M|D. M|M
D -> digit
M -> F C S E B
F -> `match:D` |`match`|\e
S -> `# P`|\e
R -> style:val;R|style:val;
E -> `G`|\e
G -> -property G|-property
B -> `H`|\e
H -> --class H|--class
C -> I N|J C|K C|T C|U C
I -> #|##|###|####|#####|######
J -> ***T***|**T**|*T*
K -> `L`|```\nL\n```|```langauge\nL\n```
T -> <span MO>|<frag MQ>|N
U -> $$V$$
N -> content|[M](text)|[M]!(text)
O ->  class:text|\e
Q ->  type:text|\e
V -> valid ktext
