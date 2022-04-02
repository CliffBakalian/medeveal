import re

'''
The regexes for certain things. This is ultimately gross and I 
need a more efficient way of doing this
'''

# empty string all os
# newline_re = re.compile("^\r?\n$") # no longer needed

# formatting
style_re = re.compile("(#\s?(([\w\-]+:[\w\-%]+;)+))") #gross
properties_re = re.compile("(((\-[0-9a-zA-Z_\-]+)\s?)+)$") #gross
property_re = re.compile("(((-[\w\-]+)\s?)+)$") #take properties from properties
fragment_re = re.compile("^\s*?`match(:([0-9]+))?") #fragment with number

# things in slides
image_rs = re.compile("`src=[\w\-\.\"'\\\/]*`") #images
latex_re = re.compile("\$\$(.*?)\$\$") #for latex equations
header_re = re.compile("^\s*?# (\w+)") #titles for slides, I use h3
inline_fragment_re = re.compile("<frag (.*?)( type:([a-zA-Z\-]+))?>")
span_re = re.compile("<span (.*?)( class:([a-zA-Z\-]+))?>") #inline changes like color

#markdown syntax
bold_re = re.compile("\*\*(.*?)\*\*")
italics_re = re.compile("\*(.*?)\*")
code_re = re.compile("```")

#modified markdown
list_re = re.compile("litem\. (.*?)")
dots_re = re.compile("ditem\. (.*?)")

# SLIDES
end_slide_re = re.compile("### END ###")
title_slide_re = re.compile("### Title ###")
rm_slide_re = re.compile("### ROADMAP ###")
pow_slide_re = re.compile("### POW ###") #person of the week

# because all os are equal....nah linux ftw
def remove_newline(line):
  if line[-1] == "\n":
    line[:-1]
  if line[-1] == "\r":
    line[:-1]
  return line

def parse_roadmap(f):
  line = f.readline()
  rm = []
  while re.match(end_slide_re,line) != None:
    (lambda x: rm.append(x) if x != "" else None)(remove_newline(line))
  return rm

def parse_title(f):
  line = f.readline()
  rm = []
  while re.match(end_slide_re,line) != None:
    (lambda x: rm.append(x) if x != "" else None)(remove_newline(line))
  return rm

def parse_pow(f):
 line = f.readline()
 rm = []

def parse_regex(f):
  line = 
