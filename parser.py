import re
import generator
'''
The regexes for certain things. This is ultimately gross and I 
need a more efficient way of doing this
'''

# empty string all os
# newline_re = re.compile("^\r?\n$") # no longer needed

# formatting
data_re = re.compile("(`\s*match[^`]*`)?\s*(.*)") #gross
style_re = re.compile("(`#\s?(([\w\-]+:[\w\-%]+;)+)`)") #gross
properties_re = re.compile("\s`(((\-[0-9a-zA-Z_\-=']+)\s?)+)`\s*$") #gross
property_re = re.compile("(\s|`)-([0-9a-zA-Z_\-=']+)(\s|`\s*$)") #take properties from properties
fragment_re = re.compile("^\s*`match(:\s?([0-9]+))?`") #fragment with number

# things in slides
image_rs = re.compile("`src=[\w\-\.\"'\\\/]*`") #images
latex_re = re.compile("\$\$(.*?)\$\$") #for latex equations
header_re = re.compile("^\s*?# (\w+)") #titles for slides, I use h3
inline_fragment_re = re.compile("<frag (.*)( type:([a-zA-Z\-]+))?>")
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

def parse_content(line):
  #take out the databetween the match and style
  f = re.search(data_re,line)
  if f != None:
    content = f.group(2)
    #due to infinite regex matching on '.*', I have to do nested matches
    style_idx = content.find("`#") #style and maybe properties
    if style_idx != -1:
      return content[0:style_idx]
    prop_idx = content.find("`-") #just properties, no style
    if prop_idx != -1:
      return content[0:prop_idx]
    return content
  return ""

def parse_fragment(line):
  properties = [False,-1] #make alist if fragment and id 
  f = re.search(fragment_re, line)
  if f != None:
    properties[0] = (True)
    f_id = f.group(2) 
    if f_id != None:
      properties[1] = int(f_id) #easier to just have the parser do this
  return properties

def parse_style(line): #i'm dumb and overthought this. just take whats there
  style = ""
  f = re.search(style_re, line)
  if f != None:
    f_style = f.group(2) 
    if f_style != None:
      style =(str(f_style))
  return style

def parse_properties(line): #still dumb. Overthought this. just take whats ther
  properties = []
  f = re.search(properties_re,line)
  if f != None:
    ps = f.group(0)
    while len(ps) > 2: #with the '.*' match I get extra stuff somethimes
      prop = re.search(property_re,ps)
      extract = prop.group(2)
      properties.append(extract)
      ps = ps[ps.find(extract)+len(extract):]
  return properties
#take the line, and take out all this stuff. Will need a different one for 
#multiline content like latex (maybe do what python does and end with \ or smth
def parse_line(line): 
  data = parse_content(line)
  style = parse_style(line)
  properties = parse_properties(line)
  fragments= parse_fragment(line)
  return data,properties,style,fragments
   
  
# parse an entire slide making list of all data lines, properties, and style per line
def parse_slide(f):
  line = f.readline()
  data= []
  properties = []
  style = []
  fragments = []
  while re.search(end_slide_re,line) == None:
    line_data = ""
    line_properties=[]
    line_style=""
    line_frag = [False,-1]
    line_id = -1
    x = remove_newline(line)
    if x != "":
      line_data,line_properties,line_style,line_frag = parse_line(x)
    data.append(line_data)
    if line_frag[1] != -1:
      line_properties.append("data-id="+str(line_frag[1]))
    properties.append(line_properties)
    style.append(line_style) 
    fragments.append(line_frag[0])
    line = f.readline()
  return data,properties,style,fragments

def parse_gen_slide(f):
  data,properties,style,fragments = parse_slide(f)
  return generator.generate_gen_slide(data,properties,style,fragments)

def parse_roadmap(f):
  data,properties,style,_ = parse_slide(f)
  return generator.generate_roadmap_slide("test",data,['purple','blue','green','orange'],properties,style)

def parse_title(f):
  data,properties,style,_ = parse_slide(f)
  for idx,line in enumerate(data):
    if line[0] != "`":
      return generator.generate_title_slide(data,properties,style,idx)  
  return generator.generate_title_slide(data,properties,style,-1)  

def parse_split(f):
 line = f.readline()

r = open("tests/test.road")
print(parse_roadmap(r))
t = open("tests/test.title")
print(parse_title(t))
b = open("tests/test.bore")
print(parse_gen_slide(b))
c = open("tests/test.complex")
print(parse_gen_slide(c))
