# Shree KRISHNAya Namaha
# Parse Meta-Data File
# Author: Nagabhushan S N


class MetaDataParser:
    def __init__(self, metadata_filepath):
        self.metadata_filepath = metadata_filepath
        self.metadata_dict = {}
        self.parse_metadata()

    def parse_metadata(self):
        with open(self.metadata_filepath) as md_file:
            lines = md_file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        for i in range(int(len(lines) / 2)):
            self.metadata_dict[lines[2 * i]] = lines[2 * i + 1]


if __name__ == '__main__':
    md_parser = MetaDataParser('../Meta-Data (Sample).txt')
    print(md_parser.metadata_dict)
