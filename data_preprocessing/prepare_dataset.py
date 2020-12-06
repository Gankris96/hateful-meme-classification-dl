import json
import shutil
import os
import csv
import traceback
from argparse import ArgumentParser

description_help_string = \
    '''
    Preprocess the facebook hateful meme dataset
    Creates the following files:- 
    1. train_split.csv
    2. validation_split.csv
    3. test_split.csv    
    '''

src_help_string = \
    '''
    The source directory containing the following files \n
    train.json, dev_seen.jsonl, dev_unseen.jsonl, \n
    test_seen.jsonl and test_unseen.jsonl \n
    along with the img folder containing all images
    '''

dst_help_string = \
    '''
    The destination folder path.
    This folder will contain the preprocessed data along with the following files -
    1. train_split.csv
    2. validation_split.csv
    3. test_split.csv
    '''


def process_jsonl_to_list(file_name: str, split_list, img_dir, src_folder):
    with open(file_name, 'r') as f1:
        for line in f1:
            json_data = json.loads(line)
            image_name = json_data['img']
            sentence = json_data['text']
            label = json_data['label']
            img_name = image_name.split('/')[0]
            image_name_in_csv = f"{image_name}"
            # print("json_data = ", json_data)
            shutil.copy(f"{src_folder}/{image_name_in_csv}", img_dir)
            item = [image_name_in_csv, sentence, label]
            split_list.append(item)
    return


def write_list_to_csv(split_list, dest_folder: str, file_name: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_path = f"{dest_folder}/{file_name}"
    with open(dest_path, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
        wr.writerows(split_list)
    return


def preprocess_data(src_folder: str, dest_folder: str, train_split: int = 10000, val_split: int = 1000,
                    test_split: int = 1000) -> bool:
    try:
        train_data_file = f"{src_folder}/train.jsonl"
        train_data_list = [['image_name', 'sentence', 'label']]
        if not os.path.exists("./data/training"):
            os.makedirs("data/training")
        process_jsonl_to_list(train_data_file, train_data_list, "data/training", src_folder)

        # train data list created
        val_data_file = f"{src_folder}/dev_seen.jsonl"
        validation_data_list = [['image_name', 'sentence', 'label']]
        if not os.path.exists("./data/validation"):
            os.makedirs("./data/validation")
        process_jsonl_to_list(val_data_file, validation_data_list, "data/validation", src_folder)
        # validation data list created

        test_data_file = f"{src_folder}/dev_unseen.jsonl"
        test_data_list = [['image_name', 'sentence', 'label']]
        if not os.path.exists("data/testing"):
            os.makedirs("data/testing")
        process_jsonl_to_list(test_data_file, test_data_list, "data/testing", src_folder)

        write_list_to_csv(train_data_list, dest_folder, "train_split.csv")
        write_list_to_csv(validation_data_list, dest_folder, "validation_split.csv")
        write_list_to_csv(test_data_list, dest_folder, "test_split.csv")

    except FileNotFoundError:
        raise


def write_image_path(src_path):
    try:
        img_folder_path = f"{src_path}/img"
        absolute_path = os.path.abspath(img_folder_path)
        image_path_file_name = "image_folder_name.txt"
        with open(image_path_file_name, 'w') as f1:
            f1.write(absolute_path + "\n")
    except Exception:
        raise


if __name__ == '__main__':
    parser = ArgumentParser(description=description_help_string)
    parser.add_argument('-s', '--source', dest='src_folder',
                        help=src_help_string)
    parser.add_argument('-d', '--destination', dest='dest_folder', help=dst_help_string)
    parser.add_argument('-train', '--training_split_size', dest='train_split', type=int, default=10000,
                        help='Size of training split (default=10000)')
    parser.add_argument('-val', '--validation_split_size', dest='val_split', type=int, default=1000,
                        help='Size of validation split (default=1000)')
    parser.add_argument('-test', '--test_split_size', dest='test_split', type=int, default=1000,
                        help='Size of test split (default=1000)')
    args = parser.parse_args()

    print(args)
    preprocess_data(args.src_folder, args.dest_folder, args.train_split, args.val_split, args.test_split)
    write_image_path(args.src_folder)

    print("Pre-processing complete.")
