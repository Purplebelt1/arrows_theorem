import math
import numpy
import random

number_of_voters = 2
number_of_politicians = 2
popularity_scale = 1
times_to_run = 100

base_array = []
base_array_int = []

print("loading...")

for i in range(number_of_politicians):
    base_array.append("null")
    base_array_int.append(0)

class politician():
    def __init__(self):
        self.popularity = 0
        self.id = 0

def ranked_vote_counting():
    election_current_round_results = base_array_int
    for i in voter_array:
        election_current_round_results[i[0]] += 1
    politicians_with_least_votes = []
    smallest_vote = number_of_voters+1
    for i in range(len(election_current_round_results)):
        if smallest_vote > election_current_round_results[i]:
            smallest_vote = election_current_round_results[i]
        if election_current_round_results[i] > number_of_voters/2:
            return "WON"
    for i in range(len(election_current_round_results)):
        if election_current_round_results[i] == smallest_vote:
            politicians_with_least_votes.append(i)
    if len(politicians_with_least_votes) == len(election_current_round_results):
        return "TIE"
    for i in voter_array:
        for j in politicians_with_least_votes:
            i.remove(j)
    return ranked_vote_counting()

while times_to_run >= 1:

    times_to_run = times_to_run - 1

    politician_array = []
    popularity_total = 0

    for i in range(number_of_politicians):
        politician_array.append( politician() )
        if popularity_scale == 1:
            popularity_total += 1
        else:
            popularity_total += numpy.random.randint(1, popularity_scale)
        politician_array[i].popularity = popularity_total
        politician_array[i].id = i


    voter_array = []

    for i in range(number_of_voters):
        #voter_array.append( voter() )
        voter_array.append([])
        temp_politician_array = []
        temp_popularity_total = popularity_total
        for j in range(number_of_politicians):
            temp_politician_array.append([politician_array[j].popularity,politician_array[j].id])
        for j in range(number_of_politicians):
            popularity_roll = random.randint(0,temp_popularity_total)
            for k in range(len(temp_politician_array)):
                if temp_politician_array[k][0] < popularity_roll:
                    continue
                #voter_array[i].ballot[j] = temp_politician_array[k][1]
                voter_array[i].append(temp_politician_array[k][1])
                for l in range(k+1, len(temp_politician_array)):
                    if k == 0:
                        temp_politician_array[l][0] = temp_politician_array[l][0] - temp_politician_array[k][0]
                    else:
                        temp_politician_array[l][0] = temp_politician_array[l][0] - (temp_politician_array[k][0] - temp_politician_array[k-1][0])
                temp_politician_array.pop(k)
                if j != number_of_politicians-1:
                    temp_popularity_total = temp_politician_array[-1][0]
                break
        print(voter_array[i])

    result = ranked_vote_counting()
    print(result)
    file_read_write = open("win_tie_record.txt", "r")
    file_data = file_read_write.readlines()
    file_read_write.close()
    line_to_write = "none"
    for i in range(len(file_data)):
        if str(f'|{number_of_voters}/{number_of_politicians}/{popularity_scale}|') in file_data[i]:
            line_to_write = i+1
    if line_to_write == "none":
        file_read_write = open("win_tie_record.txt", "a")
        if result == "TIE":
            file_read_write.write(f'|{number_of_voters}/{number_of_politicians}/{popularity_scale}|\n1:0\n')
        else:
            file_read_write.write(f'|{number_of_voters}/{number_of_politicians}/{popularity_scale}|\n0:1\n')
        file_read_write.close()
    else:
        result_numbers = file_data[line_to_write].split(":")
        if result == "TIE":
            result_numbers[0] = int(result_numbers[0]) + 1
            file_data[line_to_write] = f'{result_numbers[0]+1}:{result_numbers[1]}\n'
            #print(f'{result_numbers[0] + 1}:{result_numbers[1]}\n')
            if times_to_run == 0:
                print(f'{result_numbers[0]+1}:{result_numbers[1]}\n')
        else:
            result_numbers[1] = int(result_numbers[1]) + 1
            file_data[line_to_write] = f'{result_numbers[0]}:{result_numbers[1]}\n'
            #print(f'{result_numbers[0]}:{result_numbers[1]+1}\n')
            if times_to_run == 0:
                print(f'{result_numbers[0]}:{result_numbers[1] + 1}\n')
        file_read_write = open("win_tie_record.txt", "w")
        file_read_write.writelines(file_data)
        file_read_write.close()
print("Done!")