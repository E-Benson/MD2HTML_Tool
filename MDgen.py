import mistune
import latex2mathml.converter
import os

def py_states(content):
    states = '```{}```'
    state = 0
    new_content = ''
    word = ''
    for c in content:
        if states[state] == c:
            if state == 7:
                new_content = new_content + '</pre></div>'
                word = ''
                state = 0
            else:
                if (state >= 0  and state <= 3) or (state == 5 or state == 6):
                    word = word + c
                elif state == 4:
                    new_content = new_content + '<div class="codeblock"><pre class="prettyprint">'
                    word = ''
                state = state + 1
        else:
            if (state >= 1 and state <= 3) or (state == 6 or state == 7):
                new_content = new_content + word + c
            elif state != 4:
                new_content = new_content + c
    new_content = new_content + '<script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>'

    return new_content


def html_states(content):
    html = '<script src="https://fred-wang.github.io/mathml.css/mspace.js"></script>\n'
    state = 0
    states = [[1 ,2 ,0], [0 ,1 ,1], [0 ,0 ,0]]
    math = ''
    for c in content:
        if state == 1 and c != '$':
            math = math + c
        elif '$' == c:
            if state == 1:
                html = html + latex2mathml.converter.convert(math)
                math = ''
            state = states[state][0]
        elif '\\' == c:
            state = states[state][1]
        else:
            if state == 2:
                html = html + '\\' + c
            elif state == 0:
                html = html + c
            state = states[state][2]
    return html


def math_states(content):
    new_content = ''
    word = ''
    state = 0
    states = '<math>'
    for c in content:
        if states[state] == c:
            word = word + c
            if state == len(states) - 1:
                new_content = new_content + '<math xmlns="http://www.w3.org/1998/Math/MathML">'
                state = 0
            else:
                state = state + 1
        else:
            new_content = new_content + word + c
            word = ''
            state = 0
    return new_content


def table_states(content):
    new_content = ''
    word = ''
    state = 0
    states = '<table>>ad>'
    for c in content:
        if states[state] == c:
            if state == 6:
                new_content = new_content + word + ' class="table table-striped table-bordered">'
                state = 0
                word = ''
            elif state == 7:
                new_content = new_content + word + ' scope="col">'
                state = 0
                word = ''
            elif state == 10:
                new_content = new_content + word + ' class="thead-light">'
                state = 0
                word = ''
            else:
                state = state + 1
                word = word + c
        else:
            if state == 2 and c == 'h':
                state = 7
                word = word + c
            elif state == 7 and c == 'e':
                state = state + 1
                word = word + c
            else:
                new_content = new_content + word + c
                word = ''
                state = 0
    return new_content


def insert_at_id(html, identity, content):
    states = '<div id="{}">'.format(identity)
    state = 0
    new_html = ''
    word = ''
    for c in html:
        if state == len(states)-2:
            if c == '>':
                new_html += word + c + content
                state = 0
                word = ''
            else:
                word += c
        elif states[state] == c:
            state += 1
            word += c
        else:
            state = 0
            new_html += word + c
            word = ''
    return new_html


def insert_content(input_template, new_content, title):
    template = open(input_template, 'r')
    if template.mode == 'r':
        print('Inserting HTML')
        html_template = template.read()
        html_template = insert_at_id(html_template, 'inject', new_content)
        new_html = insert_at_id(html_template, 'title', title)
        template.close()
        return new_html
    else:
        print('Input template file not found.')


def create_page_content(input_file, title, subject):
    print(input_file)
    file = open(input_file, 'r')
    if file.mode == 'r':
        print('Creating HTML content')
        md_content = file.read()
        md_parser = mistune.Markdown()

        parsed_code = py_states(md_content)
        html = md_parser(parsed_code)
        html = math_states(html)
        html = table_states(html)
        template = 'subtemplate_updated.html' if subject != None else 'template_updated.html'
        final_output = insert_content(template, html, title) 
        return final_output
    else:
        print('Input file not found.')


def test2():
    output = open('md_output2.html', 'w+')
    output.write(create_page_content('example_sheet.Rmd'))
    output.close()

#test2()
