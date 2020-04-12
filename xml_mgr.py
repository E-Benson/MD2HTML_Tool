import lxml.etree as et
import os


link_xml_file = 'link_tree.xml'
if os.path.exists(link_xml_file) == False:
    root = et.Element('Navigation-Links')
else:
    link_xml = open(link_xml_file, 'r')
    if link_xml.mode == 'r':
        root = et.XML(link_xml.read())


def is_static(element):
    return True if element.get("type") == 'static' else False


def is_drop(element):
   return True if element.get("type") == 'drop' else False


def find_drop_element(target):
    for child in root:
        if is_drop(child):
            if child[0].text == target:
                return child
    return None


def add_static(path, title):
    link = et.SubElement(root, 'link', type="static")
    pathE = et.SubElement(link, 'path')
    titleE = et.SubElement(link, 'title')
    pathE.text = path.lower()
    titleE.text = title


def get_subjects():
    subs = []
    for child in root:
        if child.get("subject") != None:
            subs.append(child.get("subject"))
    return subs


def find_subject(subject):
    for child in root:
        if child.get("subject") == subject:
            return child
    return None    


def add_drop(_subject, path, title):
    linkE = find_subject(_subject)
    if linkE == None:
        linkE = et.SubElement(root, 'link', type="drop", subject="{}".format(_subject))
    pathE = et.SubElement(linkE, 'path')
    titleE = et.SubElement(linkE, 'title')
    pathE.text = path
    titleE.text = title


def save_tree():
    content = et.tostring(root, pretty_print=True)
    
    if os.path.exists('link_tree.xml') == False:
        f = open('link_tree.xml', 'w+')
    else:
        f = open('link_tree.xml', 'w')
    f.write(content)
    f.close()



def get_title(filename):
    for link in root:
        print(filename.lower())
        for i in range(0, len(link)):
            print(link[i].tag + ' ' + link[i].text)
            print(link[i].text.find(filename.lower()))
            if link[i].tag == 'path' and link[i].text.find(filename) != -1:
                return link[i+1].text
    return 'NO TITLE'


def get_child_index(target):
    for i in range(0, len(root)):
        if target is root[i]:
            return i
    return -1


def swap_child(c1, c2):
    tmp = root[c2]
    root[c2] = root[c1]
    root.insert(c1, tmp)


def get_link_list():
    links = []
    for child in root:
        if child.get("subject") == None:
            for sub in child:
                if sub.tag == 'title': links.append(sub.text)
        else:
            links.append(child.get("subject"))
    return links


def get_links():
    ret = []
    for child in root:
        for subchild in child:
            if subchild.tag == "title" or subchild.tag == "subject":
                ret.append(subchild.text)
    return ret


def get_link_data():
    ret = []
    for link in root:
        if link.get("type") == "static":
            tmp = []
            for sub in link:
                tmp.append(sub.text)
            ret.append(tmp)
        elif link.get("type") == "drop":
            tmp = [[link.get("subject")]]
            paths = []
            links = []
            for i in range(0, len(link)):
                if i % 2 == 0:
                    paths.append(link[i].text)
                else:
                    links.append(link[i].text)
            tmp.append(paths)
            tmp.append(links)
            ret.append(tmp)
    return ret


def print_link_data():
    arr = get_link_data()
    for link in arr:
        if len(link) == 2:
            print("p: {}\tt: {}".format(link[0], link[1]))
        else:
            print(link[0])
            for i in range(0, len(link[1])):
                print("\t{}\t{}".format(link[1][i], link[2][i]))

#print(get_subjects()) 
