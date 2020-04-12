import filesys as fs
import HTMLgen
import MDgen as md
import xml_mgr as xml
import os
#import con2
#import lxml.etree


def choose_links():
    links = xml.get_link_list()
    option = 0
    print('\t=====  Link Order ======')
    while option > -1:
        for i in range(0, len(links)):
            print('\t%d:\t%s' % (i, links[i]))
        inp1 = input('\tSelect the index of which to move: ')
        inp2 = input('\tSelect the index to move to: ')
        if inp1 >= 0 and inp2 >= 0:
            xml.swap_child(inp1, inp2)
            option = input('\tEnter 1 to change another link, or -1 to exit: ')
        else:
            option = -1
    xml.save_tree()
    print(xml.et.tostring(xml.root))


def add_page():
    print('\t====== Add New Page ======')
    md_file = raw_input('\tEnter the name of the .md file: ')
    subject = subject_menu()
    title = raw_input('\tEnter a title for the page: ')
    filename = os.path.splitext(md_file)[0]
    path = fs.create_path(subject, "{}.html".format(filename))
    f = open(md_file, 'r')
    fs.save_file(subject, md_file, f.read())
    if subject == None:
        xml.add_static(path, title)
    else:
        xml.add_drop(subject, path, title)
    xml.save_tree()
    if raw_input('Would you like to arrange your links?[y/n] ') == 'y':
        choose_links()
    fs.update_site()
      
     
def subject_menu():
    option = 0
    subs = xml.get_subjects()
    size = len(subs)
    print('\t====== Subjects ======')
    for i in range(0, size):
        print('\t{}.\t{}'.format(i, subs[i]))
    print('\t{}.\tNone'.format(size))
    print('\tEnter -1 to create a new subject.')
    option = input('\t\tOption #: ')
    if option < 0:
        return raw_input('\tNew subject: ')
    elif option == size:
        return None;
    else:
        return subs[option]

def menu():
    option = 0
    while option > -1:
        os.system('clear')
        print('\n---- Menu Options ----')
        print('-1.\tExit')
        print('1.\tAdd new page')
        print('2.\tArrange links')
        print('3.\tUpdate Site')
        option = input('Select an option: ')
        if option == 1:
            add_page()
        elif option == 2:
            choose_links()
        elif option == 3:
            fs.update_site()
        elif option <= -1:
            break
        else:
            print('\tEnter a valid option number.')
            option = 0

menu()
