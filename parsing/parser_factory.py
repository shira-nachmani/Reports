from parsing.type_a_parser import parse_type_a_line
from parsing.type_b_parser import parse_type_b_line

class ParserFactory:
    @staticmethod
    def get_parser(report_type: str):
        if report_type == "Type A":
            return parse_type_a_line
        return parse_type_b_line