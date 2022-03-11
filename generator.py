refs=["dist/reveal.css","dist/theme/white.css","plugin/highlight/stackoverflow.css","theme1.css"]

'''
#HTML PAge
'''

def generate_head(hrefs):
  ##TODO need to make generic
  title = make_tag("title",[],"CMSC250")
  meta_char = '<meta charset="utf-8">\n'  
  meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n'
  links = ""
  for i,v in enumerate(hrefs):
    links+=make_link_tag("stylesheet",v,["","theme","",""][i])
  return make_tag("head",[],title+meta_char+meta+links)

def generate_html(hrefs,body):
  head = generate_head(hrefs)
  final_body = generate_reveal_body(body)
  return make_tag("html",[],head+final_body)

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
    return "<"+tag+">"+body+"</"+tag+">\n"
  else:
    return "<"+tag+" "+properties+">"+body+"</"+tag+">\n"

def generate_shape(shape,properties=[],classes=[],frag=True,frag_idx=-1,frag_type="",data_id=-1,style=""):
  class_prop = make_class_property([make_fragment_classes(frag,frag_type), shape]+classes) 
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
  return make_tag("body",[],slides_body+reveal_info)

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
    plugs += generate_script(i)
  return plugs 

'''
Slide Styles
'''

#ROADMAP

def generate_roadmap_slide(title,roadmap,colors,shape="diamond",connect=True):
  title_attr =generate_text(title,"h3",[],[],False,-1,"",-1,"") 
  body = title_attr+generate_roadmap(roadmap,colors,shape,connect)
  return generate_slide(body,["data-auto-animate","data-auto-animate-unmatched='fade-up'"],"height:600px",[])

def generate_roadmap(text,colors,shape="diamond",connect=True):
  roadmap = ""
  curr_bullet =""
  distance = 80
  base = 60 
  try:
    for idx,value in enumerate(text):
      if idx != 0 and connect:
        curr_bullet += generate_shape("rmvline",[],[],True,idx+1,"fade-down",-1,"top:"+str(base)+"px;")
      curr_bullet += generate_shape(shape,[],[],True,idx+1,"",idx+1,"background:"+colors[idx]+";top:"+str(base+(distance/2))+"px;")
      curr_bullet += generate_text(value,"div",[],["rm-data"],True,idx+1,"fade-down",-1,"top:"+str(base+33)+"px;")
      base+=distance
      roadmap+=curr_bullet
      curr_bullet=""
  except IndexError:  
      curr_bullet += generate_shape(shape,[],[],True,idx+1,"",idx+1,"background:"+colors[len(text)-1]+";top:"+str(base+(distance/2))+"px;")
      curr_bullet += generate_text(value,"div",[],["rm-data"],True,idx+1,"fade-down",-1,"top:"+str(base+33)+"px;")
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
    body += attrs[i]   
  return generate_slide(body,["data-auto-animate","data-auto-animate-unmatched='fade-up'"],"",[])

#DOTS 
def generate_dots(properties=[],style=[],dnum=3,currdot=1,dcolor="purple",shape="rm-circle",space=20,start=-50):
  dots=""
  for i in range(dnum):
    dotstyle="";
    if i+1 == currdot:
      dotstyle+="background:"+dcolor+";"
    dotstyle+="bottom:"+str((dnum-(i+1))*space+start)+"px;"
    dots+=generate_shape(shape,properties[:],[],False,-1,"",i+1,dotstyle) 
  return dots

#TWO COLUMNS
def generate_split_slide(body1,body2,width1=50,width2=50):
  lwidth=make_style_string("width:'"+str(width1)+"'%")
  rwidth=make_style_string("width:'"+str(width2)+"'%")
  lbody=make_tag("div",[lwidth],body1)
  rbody=make_tag("div",[rwidth],body2)
  return make_tag("div",[make_class_property(["container"])],lbody+rbody)

'''
TIME TO EXPORT
'''
# WRITE TO FILE 
def generate_slides(src_file):
  #TODO actually have to write the parser lol
  rm = (generate_roadmap_slide("sets, functions, relations",["person of the week","countability","set proofs"],["purple","blue","orange"],"rm-diamond",True))
  tit =(generate_title_slide("CMSC250","sets, functions, relations","dist/assets/funcpun.jpeg","","","height:300px",[0,1,2]))
  
  #slide1 test
  title_attr = generate_text("slide1","h3",[],[],False,-1,"",-1,"") 
  dots = generate_dots([],[],5,1,"purple","rm-circle",20,-50)
  slide1 = generate_slide(title_attr+dots,["data-auto-animate"],"height:600px",[])
  
  #slide2 test
  title_attr = generate_text("slide2","h3",[],[],False,-1,"",-1,"") 
  dots = generate_dots([],[],5,2,"blue","rm-circle",20,25)

  #slide2.1 test
  s2_1p = make_tag("p",[],"Hello")
  slide2_1 = generate_slide(s2_1p,["data-auto-animate"],"",[])

  #slide2.2 test
  s2_2p = make_tag("p",[],"world")

  slide2_2 = generate_slide(s2_2p,["data-auto-animate"],"",[])
  
  slide2=generate_slide(title_attr+dots+slide2_1+slide2_2,["data-auto-animate"],"",[])

  #slide3 test
  title_attr = generate_text("slide3","h3",[],[],False,-1,"",-1,"") 
  dots = generate_dots([],[],5,3,"green","rm-circle",20,-50)
  slide3 = generate_slide(title_attr+dots,["data-auto-animate"],"height:600px",[])
  
  return generate_html(refs,tit+rm+slide1+slide2+slide3)

f = open("myslides.html", "w")
slides_to_make = raw_input("file name: ")
f.write(generate_slides(slides_to_make))
f.close()
