from jiit_marks import parse_report_file
import json
import sys

if __name__ == "__main__":
    print(json.dumps(parse_report_file(sys.argv[1])))

