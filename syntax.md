# Syntax for Medeval

This is mostly a markdown compiler to reveal js. So many common Markdown syntax will be supported. THe only addition is for revealsj parts. This is mostly for my own use so parts of RevealJS which I don't use will not be supported right away.

## Medeval Synatx

### General matching style
Most lines will look something like this: 

`match:id` content `\# style1:val;style2:val2;` `-property1 -property2` `--class1 --class2`

+ **match** will tell revealjs that the content should be in a fragment
+ **:id** will give the fragment an id which can be match for auto-animations. This is optional
+ content is what will be displayed
+ **\# style1:val;** will add the inline style to the html tag in the form of `<tag style="style1:val;">content</tag>`
+ **-property** will add the property to the html tag: `<tag property>content</tag>`. Useful for data-auto-animate and the like 
+ **--class** will add the class to the html tag: `<tag class=class>content</tag>`. Useful for animations like fade-up and the like 

### inline changes
Sometimes however we want inline stuff like animattions or stuff. We are going to hijack the span class and make a new tag called `frag`  
\<frag content type:fade-up\>  
\<span content class:class0\>

Frag is for making inline fragments whereas span is the more generic. Techincally frag is the special case of class.
Unlike an html tag, there is not end tag, so we just place everythiing between the angle brackets. 
+ **type:** will tell revealjs that the content should be in a fragment. This is optional
+ **class:** will give the span a single class. I want this because this is useful for making shapes.

### Latex
$$inline-latex$$

## Markdown Syntax

This mostly follows the classic markdown syntax but I've made some modifications
### Headers

\# Header 1 `regex: /^# /`  
\#\# Header 2 `regex: /^#{2} /`  
\#\#\# Header 3 `regex: /^#{3} /`  
\#\#\#\# Header 4 `regex: /^#{4} /`  
\#\#\#\#\# Header 5 `regex: /^#{5} /`  
\#\#\#\#\#\# Header 6 `regex: /^#{6} /`  

**Note: space after \#**  

### Paragraphs
this is paragraph 1

this is paragraph 2 

`regex:  /[\n\cr\br]{2}/`

### Line breaks

here is a new line\\\\

**Note: a double space will not be tagged**

### Bold and Emphasis

this is **\*\*bold\*\*** text `regex: /**/`

this is *\*italicized\** text `regex: /*/`

this is***\*\*\*bold and italizised\*\*\****

**Note: Medeval supports latex so you cannot do these in the latex environment**

### Lists
The ordered list looks like
1. item 1
2. item 2
`regex: /^\d\. .*$/` 

The unordered lists looks like
+ item 1
+ item 2
`regex: /^+ .*$/`

**Note: Due to regex not doing well with the dot-star combination, if a line starts with either of these two symbols, Medeval will assume that the entire line is the item**
**Addendum: You can still put style modifiers in an item:** 
> 1. `match:1` here is text `#height:30px;` `-data-fragment-id:1 -property2`

### Elements in Lists

//TODO
I didn't know this was a thing in classic markdown but now I am aware and I would like to keep this functionality
Guess I need to implement it :(
Easiest way to to just look for lines that begin with `regex: /^\t\t/`. I personally convert my tabs to spaces and I tpyically use 2 spaces instead of the orignal 4, however for this, I will look for 4 spaces or `regex: /^    /`

**Note: much like list style modifiers, Medeval will look for them after the tabs or spaces**

### Code and Codeblocks

I did not know that code blocks were denoted by 4 spaces or 1 tab as I have been used to the triple backtick, so the tripple backtick we will use and Medeval will not currently support the 4 spaces or 1 tab convention.

here is `\`inline code\``. 

```\`\`\`
here is 
block code
\`\`\````

`inline code regex: /`[^`]/`
`code block regex: /```\n/`
`code langauge block regex: /```[a-z]+\n/`

The syntax highlighting for Medeval will be based on your revealjs settings.
**Note: double back ticks `regex:/``[^`]/` will be used for latex open quotes

### Links and Images

Medeval supports the typical link notation of

\[text\]\(link\)

and image notation of 

\[text\]!\(link\)

You should be able to format it much like in regualar markdown: \*\*\[text\]\(link\)\*\* should make a bold link. However if you want ot use Medeval's formatting syntax, place it in the `text` section since we want links to have inline support. 
> this is a **\[`match: 1` formatted link `#height:20px;`\]\(link\)**

**Note: When using Medeval's formatting for images, the image will be the thing modified, not the alt text** 

### 
