import pymupdf

def parse_report_file(file: str) -> dict:
    doc = pymupdf.open(file)
    return parse_report(doc) 

def parse_report(doc: pymupdf.Document) -> dict:
    page = doc[0]
    tabs = page.find_tables()

    data = {"student_info": {}, "meta": {}, "courses":[], "legend": {}}
    tab = tabs[0]
    for line in tab.extract():
        for tok in line:
            if tok:
                key, value = tok.split(": ")
                data["student_info"]['_'.join(key.strip().lower().split())] = value.strip()

    for key, value in tabs[2].extract()[1:]:
        data["legend"][key] = value
    tab = tabs[1]
    lines = tab.extract()

    exams = []
    for tok in lines[0][1:]:
        if tok:
            exams.append(tok)

    data["meta"]["exams"] = exams
    data["meta"]["cols"] = len(exams)
    data["meta"]["rows"] = len(lines[2:])

    for course in lines[2:]:
        c = {}
        name_code = course[0]
        c["code"] = name_code.split('\n')[-1].strip(" ()")
        c["name"] = ' '.join(name_code.split('\n')[:-1])
        c["exams"] = {}
        
        marks_slice = course[1:]
        i = 0
        cols = 0
        while i < len(marks_slice):
            if marks_slice[i] == '-':
                cols+=1
                i+=2
                continue

            marks = {"remarks": "none"}
                
            if marks_slice[i] == 'A':
                marks["remarks"] = "absent"
            else:
                marks["OM"], marks["FM"] = map(float, marks_slice[i].split("/ "))

            marks["OW"], marks["WT"] = map(float, marks_slice[i + 1].split("/"))
        
            c["exams"][exams[cols]] = marks
            cols += 1
            i+=2
        
        data["courses"].append(c)
    
    return data


