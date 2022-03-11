theme = "my"
refs=["dist/reveal.css","dist/theme/white.css","plugin/highlight/stackoverflow.css","dist/theme1.css"]

'''
#HTML PAge
'''

def generate_head(hrefs):
  ##TODO need to make generic
  title = make_tag("title",[],"CMSC250")+"\n"
  meta_char = '<meta charset="utf-8">\n'  
  meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n'
  links = ""
  for i,v in enumerate(hrefs):
    links+=make_link_tag("stylesheet",v,["","theme","",""][i])
  return make_tag("head",[],title+meta_char+meta+links)

def generate_html(hrefs,body):
  head = generate_head(hrefs)
  final_body = generate_reveal_body(body)
  return make_tag("html",[],head+"\n"+final_body)

'''
# COMMON HTTP Attributes
'''

def make_link_tag(rel,href,id_tag=""):
  if id_tag !="":
    return '<link rel="'+rel+'" href="'+href+'" id="'+id_tag+'">\n'
  return '<link rel="'+rel+'" href="'+href+'">\n'

def make_fragment_classes(frag,frag_type):
  class_string = ""  
  if frag:
    class_string = "fragment"
  if frag_type!="":
    class_string = class_string+" "+frag_type
  return class_string 

def make_class_property(strings):
  classes = ' '.join(map(str, strings))
  if classes!="":
    return "class='"+' '.join(map(str, strings))+"'"
  else:
    return ""

def make_fragment_properties(frag_idx,data_id):
  properties =""
  if frag_idx > -1:
    properties= 'data-fragment-index="'+str(frag_idx)+'"'
  if data_id > -1:
    properties += ' data-id="'+str(data_id)+'"' 
  return properties

def make_style_string(style):
  if style=="":
    return ""  
  else:
    return "style='"+style+"'"

def make_properties(strings):
  return " ".join(map(str, strings))

def make_tag(tag,properties=[],body=""):
  properties = make_properties(list(filter(None,properties))) #remove empty strings
  if properties =="":
    return "<"+tag+">"+body+"</"+tag+">"
  else:
    return "<"+tag+" "+properties+">"+body+"</"+tag+">"

def generate_shape(shape,properties=[],classes=[],frag=True,frag_idx=-1,frag_type="",data_id=-1,style=""):
  class_prop = make_class_property([make_fragment_classes(frag,frag_type), theme+'-'+shape]+classes) 
  properties.append(class_prop) 
  properties.append(make_properties([make_fragment_properties(frag_idx,data_id)])) 
  properties.append(make_style_string(style))

  return make_tag("div",properties,"")          

def generate_text(text,tag="p",properties=[],classes=[],frag=True,frag_idx=-1,frag_type="",data_id=-1,style=""):
  class_prop = make_class_property([make_fragment_classes(frag,frag_type)]+classes)
  properties.append(class_prop)
  properties.append(make_properties([make_fragment_properties(frag_idx,data_id)])) 
  properties.append(make_style_string(style))

  return make_tag(tag,properties,text)          

def generate_img(src,properties=[],classes=[],frag=True,frag_idx=-1,frag_type="",data_id=-1,style=""):
  properties.append("src='"+src+"'")
  return generate_text("","img",properties,classes,frag,frag_idx,frag_type,data_id,style)

def generate_slide(body,properties,style,classes):
  return generate_text("\n"+body,"section",properties,classes,False,-1,"",-1,style)

def generate_script(src):
  return make_tag("script",['src="'+src+'"'],"")

'''
REVEAL JS wrapper 
'''

def generate_reveal_body(body):
  slides_body = make_tag("div",[make_class_property(["reveal"])],make_tag("div",[make_class_property(["slides"])],"\n"+body))
  reveal_info = generate_reveal_plugins()+generate_reveal_script()
  return make_tag("body",[],slides_body+"\n"+reveal_info)

def generate_reveal_script():
  return make_tag("script",[],generate_reveal_config()+generate_reveal_init())

#TODO Need to make this read a json file
def generate_reveal_config():
  return """Reveal.configure({ 
        keyboard: {
          40: 'next', // go to the next slide with down arrow
          38: 'prev', // go to the next slide with up arrow
        }
      });"""

#TODO Need to make this read a json file
def generate_reveal_init():
  return """Reveal.initialize({
center: true,
hash: true,
controlsTutorial: false,
showSlideNumber: 'print',
pdfSeparateFragments: false,
math: {
// mathjax: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js',
config: 'TeX-AMS_HTML-full',
TeX: {
Macros: {
R: '\\mathbb{R}',
set: [ '\\left\\{#1 \\; ; \\; #2\\right\\}', 2 ]}}},
plugins: [ RevealHighlight, RevealMarkdown, RevealMath, RevealSearch, RevealZoom ]});""" 

def generate_reveal_plugins(plugins=["dist/reveal.js","plugin/highlight/highlight.js","plugin/markdown/markdown.js","plugin/math/math.js","plugin/search/search.js","plugin/zoom/zoom.js"]):
  plugs = ""
  for i in plugins:
    plugs += generate_script(i)+"\n"
  return plugs 

'''
Slide Styles
'''

#ROADMAP

def generate_roadmap_slide(title,roadmap,colors,shape="diamond",connect=True):
  title_attr =generate_text(title,"h3",[],[],False,-1,"",-1,"") 
  body = title_attr+"\n"+generate_roadmap(roadmap,colors,shape,connect)
  return generate_slide(body,["data-auto-animate","data-auto-animate-unmatched='fade-up'"],"height:600px",[])

def generate_roadmap(text,colors,shape="diamond",connect=True):
  roadmap = ""
  curr_bullet =""
  distance = 80
  base = 60 
  try:
    for idx,value in enumerate(text):
      if idx != 0 and connect:
        curr_bullet += generate_shape("rmvline",[],[],True,idx+1,"fade-down",-1,"top:"+str(base)+"px;")+"\n"
      curr_bullet += generate_shape(shape,[],[],True,idx+1,"fade-down",idx+1,"background:"+colors[idx]+";top:"+str(base+(distance/2))+"px;")+"\n"
      curr_bullet += generate_text(value,"div",[],[theme+"-rm-data"],True,idx+1,"fade-down",-1,"top:"+str(base+33)+"px;")+"\n\n"
      base+=distance
      roadmap+=curr_bullet
      curr_bullet=""
  except IndexError:  
      curr_bullet += generate_shape(shape,[],[],True,idx+1,"fade-down",idx+1,"background:"+colors[len(text)-1]+";top:"+str(base+(distance/2))+"px;")+"\n"
      curr_bullet += generate_text(value,"div",[],[theme+"-rm-data"],True,idx+1,"fade-down",-1,"top:"+str(base+33)+"px;")+"\n\n"
      roadmap+=curr_bullet
      
  return roadmap

#TITLE
def generate_title_slide(title,subtitle,img="",title_style="",subtitle_style="",img_style="",order=[0,1,2]):
  title_attr =generate_text(title,"h1",[],[],False,-1,"",-1,title_style) 
  subtitle_attr = generate_text(subtitle,"h3",[],[],False,-1,"",-1,subtitle_style)
  img_attr = generate_img(img,[],[],False,-1,"",-1,img_style)
  attrs = [title_attr,subtitle_attr,img_attr]
  body = ""
  for i in order:
    body += attrs[i]+"\n"   
  return generate_slide(body,["data-auto-animate","data-auto-animate-unmatched='fade-up'"],"",[])

# WRITE TO FILE 
def generate_slides(src_file):
  #TODO actually have to write the parser lol
  rm = (generate_roadmap_slide("sets, functions, relations",["person of the week","countability","set proofs"],["purple","blue","orange"],"rm-diamond",True))
  tit =(generate_title_slide("CMSC250","sets, functions, relations","dist/assets/funcpun.jpeg","","","height:300px",[0,1,2]))
  return generate_html(refs,tit+"\n"+rm)

f = open("myslides.html", "w")
slides_to_make = raw_input("file name: ")
f.write(generate_slides(slides_to_make))
f.close()
