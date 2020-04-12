import os
import glob
import shutil
import errno
import xml_mgr as xml
import HTMLgen
import MDgen as md
import datetime as dt

def get_files(directory, file_type):
    files = []
    pattern = '*.{}'.format(file_type)
    for f in os.listdir(directory):
        if f.endswith(file_type):
            files.append(f)
    return files


def get_dirs(directory):
    dirs = []
    for g in glob.glob(directory + '*/'):
        dirs.append(g)
    return dirs


def get_filetype(direc, file_type, ret):
    files = get_files(direc, file_type)
    dirs = get_dirs(direc)
    for f in files:
        file_name = os.path.splitext(f)[0]
        ret.append([direc + f, file_name])
    if len(dirs) < 1:
        return ret
    for d in dirs:
        ret = get_filetype(d, file_type, ret)
    return ret


def create_path(subject, file_name):
    path = '.'
    if os.path.splitext(file_name)[1] == '.md':
        path += '/md/'.lower()
        if os.path.exists(path) == False:
            os.mkdir(path)
    if subject == None:
        return '{}/{}'.format(path, file_name)[1:]
    path += '/subjects/'.lower()
    if os.path.exists(path) == False:
        os.mkdir(path)
    path = '{}{}'.format(path, subject).lower()
    if os.path.exists(path) == False:
        os.mkdir(path)
    return '{}/{}'.format(path, file_name)[1:].lower()


def save_file(subject, file_name, content):
    #path = './{}'.format(file_name)
    path = create_path(subject, file_name)
    if subject != None:
        pass
        #path = create_path(subject, file_name)
    if os.path.exists(path) == True:
        output = open(path, 'w')
        print('Saving file "{}"'.format(path))
    else:
        print('Creating file "{}"'.format(path))
        output = open(path[1:], "w+")
    output.write(content)
    print('Saved file: "{}"'.format(path))
    output.close()
            

def save_template(content):
    f = open("template_updated.html", "w")
    if f.mode == 'w':
        f.write(content)
        f.close()


def ignore_func(ignore):
    def _ignore_(path, names):
        i_names = []
        if ignore in names:
            i_names.append(ignore)
        return set(i_names)
    return _ignore_


def update_templates():
    btn_html = update_btns()
    temps = ['template.html', 'subtemplate.html']
    for t in temps:
        f = open(t, "r")
        if f.mode == 'r':
            temp_html = f.read()
            new_html = md.insert_at_id(temp_html, 'buttons', btn_html)
            t_updated = os.path.splitext(t)[0] + '_updated.html'
            f_updated = open(t_updated, 'w')
            f_updated.write(new_html)
            f_updated.close()
        f.close()


def update_btns():
   links = xml.get_link_data()
   btn_html = ''
   for link in links:
       if len(link) == 2:
            btn_html += HTMLgen.make_static_button(link[0], link[1])
       else:
           btn_html += HTMLgen.make_drop_button(link[0], link[1], link[2])
   return btn_html
   
   

def update_site():
    backup_site()
    update_templates()
    if os.path.exists('./md/') == False: os.mkrdir('./md/')
    md_files = get_filetype('./md/', '.md', [])
    template_html = open('template_updated.html', 'r')
    for f in md_files:
        subject = None
        if f[0].find('subjects') != -1:
            dirs = f[0].split('/')
            i = dirs.index('subjects')
            subject = dirs[i+1]
        title = xml.get_title(f[1])
        md_html = md.create_page_content(f[0], title, subject)        
        save_file(subject, '{}.html'.format(f[1]), md_html)

    template_html.close()


def backup_site():
    backup_dirs = get_dirs('./backup/')
    version = len(backup_dirs) + 1
    today = dt.date.today()
    print('version: {}'.format(version))
    try:
        shutil.copytree('./', './backup/v{}_{}-{}-{}'.format(version, today.year, today.month, today.day), ignore=ignore_func('backup'))
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            print('That\'s not a dir')
        else:
            print('bad directory')        


#update_site()













