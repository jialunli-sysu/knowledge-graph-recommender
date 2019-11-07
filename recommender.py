import pickle
import torch
import argparse

from model import KPRN
from model import train
from data.format import format_paths

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train',
                        default=False,
                        action='store_true',
                        help='whether to train the model')
    parser.add_argument('--eval',
                        default=False,
                        action='store_true',
                        help='whether to evaluate the model')
    parser.add_argument('--model_dir',
                        type=str,
                        default='/model',
                        help='directory to save the model to')
    parser.add_argument('--epochs',
                        type=int,
                        default=1,
                        help='number of epochs for training model')

    return parser.parse_args()


def load_sample_data():
    '''
    Constructs a couple fake hardcoded paths for testing
    '''
    with open('data/song_data_vocab/song_person_ix.dict', 'rb') as handle:
        song_person = pickle.load(handle)

    with open('data/song_data_vocab/person_song_ix.dict', 'rb') as handle:
        person_song = pickle.load(handle)

    with open('data/song_data_vocab/user_song_ix.dict', 'rb') as handle:
        user_song = pickle.load(handle)

    user1 = list(user_song.keys())[0]
    user2 = list(user_song.keys())[1]
    song1 = list(song_person.keys())[0]
    song2 = list(song_person.keys())[1]
    song3 = list(song_person.keys())[2]
    person1 = list(person_song.keys())[0]

    # training_data = [
    #     ([[user1, 1, 2], [song1, 2, 0],
    #         [person1, 0, 1], [song2, 2, 5]], 1),
    #     ([[user1, 1, 2], [song1, 2, 3],
    #         [user2, 1, 2], [song3, 2, 5]], 0),
    #     ([[user1, 1, 2], [song1, 2, 5]], 1)
    # ]


    #first item in tuple is list of paths, 2nd item is if interaction occured
    training_data = [
        ([[[user1, 1, 2], [song1, 2, 0],
            [person1, 0, 1], [song2, 2, 5]],
          [[user1, 1, 2], [song1, 2, 3],
                [user2, 1, 2], [song2, 2, 5]],
          [[user1, 1, 2], [song2, 2, 5]]], 1),

        ([[[user1, 1, 2], [song1, 2, 0],
            [person1, 0, 1], [song3, 2, 5]],
          [[user1, 1, 2], [song1, 2, 3],
             [user2, 1, 2], [song3, 2, 5]]], 0),

        ([[[user1, 1, 2], [song1, 2, 5]]], 1),
    ]

    return training_data


def load_string_to_ix_dicts():
    '''
    Loads the dictionaries mapping entity, relation, and type to id
    '''
    with open('data/song_data_vocab/type_to_ix.dict', 'rb') as handle:
        type_to_ix = pickle.load(handle)

    with open('data/song_data_vocab/relation_to_ix.dict', 'rb') as handle:
        relation_to_ix = pickle.load(handle)

    with open('data/song_data_vocab/entity_to_ix.dict', 'rb') as handle:
        entity_to_ix = pickle.load(handle)

    return type_to_ix, relation_to_ix, entity_to_ix


def main():
    '''
    Main function for our graph recommendation project,
    will eventually have command line args for different items
    '''

    args = parse_args()

    #TODO: Load dense subgraph here

    if args.train:
        #TODO: Load training set of user item interactions,
        #Then for each user item pair in training set, find all paths, and save these to disk
        #for each user item interaction, label set of paths with 0 or 1 for whether it occured or not

        t_to_ix, r_to_ix, e_to_ix = load_string_to_ix_dicts()

        #sample data is a list of (path_list, target) tuples
        training_data = load_sample_data()
        print(training_data)

        padding_token = '#PAD_TOKEN'

        formatted_data = format_paths(training_data, e_to_ix, t_to_ix, r_to_ix, padding_token)
        print(formatted_data)

        batch_size = 3
        model = train(formatted_data, batch_size, args.epochs, len(e_to_ix), len(t_to_ix), len(r_to_ix))


if __name__ == "__main__":
    main()
