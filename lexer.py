import re
'''
The regexes for certain things. 
Am doing it the lexer way. May be slower, but it will definitely work
'''

# Medeval specific

frag_re = re.compile("^`match(:(\d+))?`\s+") #capture group 2
style_re = re.compile("^`#\s+(([\w\-]+:[\w\-%]+;)+)`") # capture group 1
properties_re = re.compile("^`(((\-[0-9a-zA-Z_\-=']+)\s?)+)`") #gross
classes_re = re.compile("^`(((\-\-[a-zA-Z_\-][0-9a-zA-Z_\-']*)\s)+)`") #legacy html and css compliant

property_re = re.compile("^-([0-9a-zA-Z_\-='])+") #take properties from properties
class_re = re.compile("^\-\-[a-zA-Z_\-][0-9a-zA-Z_\-']*") #take a class from classes

medeval_re = [frag_re,style_re,properties_re,classes_re]


#markdown syntax
italics_re = re.compile("^\*[^*]")
bold_re = re.compile("^\*\*[^*]")
emph_re = re.compile("^\*{3}[^*]")
code_re = re.compile("^```([a-z]+)?")
mods_re = [emph_re,bold_re,italics_re,code_re]

## headers
h1_re = re.compile("^#\s")
h2_re = re.compile("^#\#\s")
h3_re = re.compile("^#{3}\s")
h4_re = re.compile("^#{4}\s")
h5_re = re.compile("^#{5}\s")
h6_re = re.compile("^#{6}\s")
headers_re = [h6_re,h5_re,h4_re,h3_re,h2_re,h1_re]

## ordered and unordered lists
olist_re = re.compile("^\+\s")
ulist_re = re.compile("^(\d)+\.\s")
lists_re = [olist_re,ulist_re]

## links
link_text_re = re.compile("^[")
link_ref_re = re.compile("^!?(")
links_re = [link_text_re,link_ref_re]

link_text_end_re = re.compile("^]")
link_ref_end_re = re.compile("^)")
links_end_re = [link_text_end_re,link_ref_end_re]

## newlines and stuff
new_p_re = re.compile("^[\n\r]{2}")
new_line_re = re.compile("^\\\\")
new_lines = [new_p_re,,new_line_re]

## latex
inline_latex_re = re.compile("^\$\$") #this is for inline despite how it looks
cen_latex_re = re.compile("^\${3}") #this is for center though idk if I will ever use this
# I think you can still put \( and \) and medeval will just treat it as data so you can inject code this way
latex_re = [inline_latex_re,cen_latex_re]

# things in slides
inline_fragment_re = re.compile("^<frag\s")
span_re = re.compile("^<span ") #inline changes like color
inline_re = [inline_fragment_re,inline_re]

# SLIDES
end_slide_re = re.compile("^---") #changing from ### END ### so markdown looks good
title_slide_re = re.compile("^### Title ###")
rm_slide_re = re.compile("^### ROADMAP ###")
pow_slide_re = re.compile("^### POW ###") #person of the week
slides_re = [title_slide_re,rm_slide_re,pow_slide_re,end_slide_re,olist_re,ulist_re] 

# escaping
escape_re = re.compile("^\\")

# whitespace
newline_re = re.compile("^\n")
whitespace_re = re.compile("^\s")
ignore_re = [newline_re,whitespace_re]

# Python 3.10 now supports match, but not all systems have this as default :(
regexs = slides_re + lists_re + [frag_re] + latex_re + inline_re + links_re + mods_re + headers_re + new_lines + medeval_re[1:] + [escape_re] + ignore_re

# return -1 on error
def match_re(line):
  for i,reg in enumerate(regexs):
    out = re.search(reg,line):
    if out == None:
      continue
    else:
      if i == len(regexs)-3 #escaping
        try:
          return i,line[len(out.group)+1:] 
        except:
          return -1,line
      else:
        return i,line[len(out.group):] 
