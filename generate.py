import os
import sys
import argparse
from faker import Faker

fake = Faker()

#############
# CLI Flags #
#############
parser = argparse.ArgumentParser()

parser.add_argument("-n", "--num", type=int, default=100, help="Number of attributes to generate")
parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing mock data files")
parser.add_argument("-x", "--exclude", nargs='*', type=str, help="Exclude attribute(s) from being generated (comma-separated)")

args = parser.parse_args()

######################
# Generative Methods #
######################
def generate_uuid():
    return fake.uuid4()

def generate_description():
    return fake.text()

##############
# Attributes #
##############
attribute_list = [
    {
        "name": "uuid",
        "file": "./output/uuid.txt",
        "callback": generate_uuid,
        "data": []
    },

    {
        "name": "description",
        "file": "./output/description.txt",
        "callback": generate_description,
        "data": []
    },
]

##################
# Helper Methods #
##################
def write_to_file(file_name, data):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    mode = "w" if args.overwrite else "a"
    with open(file_name, mode) as file:
        file.write(data)

###############
# Main Method #
###############
def main():
    for i in range(args.num):
        for attribute in attribute_list:
            if not args.exclude or attribute["name"] not in args.exclude:
                callback = attribute["callback"]
                data = callback()
                attribute["data"].append(data)

    for attribute in attribute_list:
        file_name = attribute["file"]
        data = '\n'.join(attribute["data"])
        write_to_file(file_name, data)

if __name__ == "__main__":
    main()