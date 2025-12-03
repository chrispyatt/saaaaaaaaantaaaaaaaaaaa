'''
Script to assign secret santa pairs from a list of participants.
Can also take an optional list of excluded pairings.
Author: CoPilot
'''

import argparse
import random


# get command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Assign Secret Santa pairs.')
    parser.add_argument('participants', type=str,
                        help='File of participants for Secret Santa. One per line.')
    parser.add_argument('--exclude', type=str,
                        help='Comma separated file of excluded pairings. One pairing per line.')
    return parser.parse_args()


# read participants from file
def read_participants(file_path):
    with open(file_path, 'r') as f:
        participants = [line.strip().lower() for line in f if line.strip()]
        # ignore header line if present
        if participants and participants[0].startswith('#'):
            participants = participants[1:]
    return participants


# read exclusions from file
def read_exclusions(file_path):
    exclusions = set()
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue  # skip header line
            else:
                pair = tuple([person.strip().lower() for person in line.split(",")])
            if pair:
                exclusions.add(pair)
    return exclusions


# assign pairs
def assign_secret_santa(participants, exclusions):
    if len(participants) < 2:
        raise ValueError("At least two participants are required for Secret Santa.")

    givers = participants[:]
    receivers = participants[:]
    random.shuffle(receivers)

    pairs = {}
    attempts = 0
    max_attempts = 1000

    while attempts < max_attempts:
        pairs.clear()
        valid = True

        for giver in givers:
            receiver = receivers.pop(0)
            if giver == receiver or (giver, receiver) in exclusions:
                valid = False
                break
            pairs[giver] = receiver

        if valid:
            return pairs

        receivers = participants[:]
        random.shuffle(receivers)
        attempts += 1

    raise Exception("Failed to assign Secret Santa pairs without conflicts after multiple attempts.")


def main():
    args = parse_arguments()
    participants = read_participants(args.participants)
    exclusions = read_exclusions(args.exclude) if args.exclude else set()
    
    try:
        pairs = assign_secret_santa(participants, exclusions)
        for giver, receiver in pairs.items():
            print(f"{giver} -> {receiver}")
    except Exception as e:
        print(f"Error: {e}")
    

if __name__ == "__main__":
    main()

