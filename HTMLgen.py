pre = '/css/bensonea'

def make_static_button(link_path, name):
    path = pre + link_path.lower()
    return  """<li class="nav-item rounded mb-2 shadow">
              <a class="nav-link text-white" href="{}">{}</a>
            </li>\n""".format(path, name)


def make_drop_button(subject, paths, links):
    html = """<li class="nav-item  rounded dropdown">
              <a class="nav-link dropdown-toggle mb-2 col col-sm-12 text-white" data-toggle="dropdown"
              href="#" role="button" aria-haspopup="true" aria-expanded="false">{}</a>
              <div class="dropdown-menu">\n""".format(subject[0])
    for i in range(0, len(links)):
        path = pre + paths[i].lower()
        html += '<a class="dropdown-item" href="{}">{}</a>\n'.format(path, links[i])
    return html + "</div>\n</li>\n"


