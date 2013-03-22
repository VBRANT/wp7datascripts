'''Simple visualisation tool, creating html page from brat stand off files.

Takes two compulsory arguements:
1) the name of brat format annotation file
2) the name of the matching plain text file
   see <http://brat.nlplab.org/standoff.html> for more on file formats

And two optional arguments:
prev - the name of an html file that logically precedes the viewed page
next - the name of an html file that logically succedes the viewed page

Note: HTML special characters are not escaped so relies on UTF-8 for
accurate rendering.

David King <David.King@open.ac.uk>
For ViBRANT <http://vbrant.eu//>
January 2013

License: GPLv2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt>
'''

import re

extract_stand_off = re.compile('(?P<ID>\S+)\t'
                               '(?P<type>\S+)\W'
                               '(?P<start_offset>\d+)\W'
                               '(?P<end_offset>\d+)\t'
                               '(?P<text>\S+)')
top = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '\
'"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'\
'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'\
'<head>\n'\
'<title>Visualisation</title>\n'\
'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'\
'<style type="text/css">\n'\
'dfn { background-color: chartreuse; }\n'\
'</style>\n'\
'</head>\n'\
'<body>\n'\
'<div>\n'
tail = '</div>\n'\
'</body>\n'\
'</html>\n'

def mark_up(text_file, ann_file, prev=None, next=None):
    # get the text as one long string
    with open(text_file, 'r', encoding='utf-8', newline='\n') as f:
        text = f.read()
    # get the matching annotations as a list, each line becoming an entry
    with open(ann_file, 'r', encoding='utf-8', newline='\n') as f:
        annotations = f.readlines()
    if annotations == []:
        # there are no annotations so build plain text page instead
        print('no annotations to apply in {:s}'.format(ann_file))
        body = text.replace('\n', '<br/>\n')
    else:
        # somewhere to build body of html page from annotations
        body_list = []
        # get text from start to first annotation
        stand_off = extract_stand_off.search(annotations[0])
        body_list.append(text[:int(stand_off.group('start_offset'))])
        start_text = int(stand_off.group('end_offset'))
        # loop through annotations inserting html mark up for each one
        for annotation in annotations:
            stand_off = extract_stand_off.search(annotation)
            body_list.append(text[start_text:int(stand_off.group('start_offset'))])
            body_list.append('<dfn title="{:s}">{:s}</dfn>'
                             .format(stand_off.group('type'),
                                     stand_off.group('text')))
            start_text = int(stand_off.group('end_offset'))
        # get remainging text from last annotation to end
        body_list.append(text[start_text:])
        # check optional arguments
        if prev is not None:
            body_list.append('<a href="' + prev + '"><button>prev</button></a>')
        if next is not None:
            body_list.append('<a href="' + next + '"><button>next</button></a>')
        # and finish off bulding the page
        body = ''.join(body_list)
        body = body.replace('\n', '<br/>\n')
        return top + body + tail

if __name__ == '__main__':
    import os
    dir = '../bca_03_aves_v4_ocr/'
    ann_list = [entry for entry in os.listdir(dir) if entry.endswith('ann')]
    for ann_file in ann_list:
        txt_file = ann_file[:-3] + 'txt'
        if os.path.exists(dir + txt_file):
            html_file = ann_file[:-3] + 'html'
            html_page = mark_up(
                dir +  txt_file,
                dir +  ann_file)
        with open(dir + html_file, 'w', encoding='utf-8', newline='\n') as f:
            if html_page is not None:
                f.write(html_page)