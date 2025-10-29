import os
import csv


def read_csv(source_path, out_path):
    """
    Merge all csv files into one big list.
    :param source_path: Path to source csv files
    :param out_path: Path to output csv files
    :return None
    """
    # list all .csv files in given path
    try:
        all_files = [file for file in os.listdir(source_path) if file.endswith('.csv')]
    except FileNotFoundError:
        print(f"No such directory: {source_path}")
        return None
    except PermissionError:
        print(f"Cannot access the directory: {source_path}")
        return None

    # merge all .csv files
    with open(os.path.join(out_path, 'total.csv'), 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)

        # process the first .csv file, including header
        with open(os.path.join(source_path, all_files[0]), 'r', newline='', encoding='utf-8') as firstfile:
            reader = csv.reader(firstfile)
            header = next(reader)
            writer.writerow(header)
            writer.writerows(reader)
        # process the remaining .csv files
        for file in all_files[1:]:
            with open(os.path.join(source_path, file), 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                # skip the header
                next(reader, None)
                writer.writerows(reader)


def preprocess(file):
    # TODO: Dataset preprocessing
    pass


if __name__ == '__main__':
    read_csv('../datas/', '../model/dataset/')
