import numpy
import random

# The number of voters who will vote in the election
number_of_voters = 10000
# The number of politicians who will run in the election
number_of_politicians = 10
# Increasing this number with make some politicians more popular than others. If it's one then
# everyone will have the same popularity, if it is 2 half will be less popular and half will be
# more popular, if 3 then there are 3 states of popularity and so on.
popularity_scale = 3
# The number of times you want this simulation to run
times_to_run = 10000


# Setting up an array to act as a base to clone later
base_array_int = []

print("loading...")

# Making the array the same length as the number of politicians
for i in range(number_of_politicians):
    base_array_int.append(0)

# This identifies politicians as a thing with both popularity and an ID
class politician():
    def __init__(self):
        self.popularity = 0
        self.id = 0

# This does the election calculation once the ballots are in
def ranked_vote_counting():

    # .copy() IS SUPER IMPORTANT DON'T CHANGE PYTHON IS WEIRD
    election_current_round_results = base_array_int.copy()

    # This counts how many votes each politician had in this round
    for i in voter_array:
        election_current_round_results[i[0]] += 1

    politicians_with_least_votes = []
    smallest_vote = number_of_voters+1

    # This find the smallest amount of votes any politician got or if anyone won the election
    for i in range(len(election_current_round_results)):
        if expelled_politicians[i] != True:
            if smallest_vote > election_current_round_results[i]:
                smallest_vote = election_current_round_results[i]
        if election_current_round_results[i] > number_of_voters/2:
            return "WON"

    # This records how many politician had the smallest amount of votes this round/cycle.
    for i in range(len(election_current_round_results)):
        if election_current_round_results[i] == smallest_vote:
            politicians_with_least_votes.append(i)

    expelled_num = 0

    # This code finds out if there was a tie or not
    for i in expelled_politicians:
        if i == True:
            expelled_num += 1
    if len(politicians_with_least_votes) == len(election_current_round_results)-expelled_num:
        return "TIE"

    # This removes the votes for politicians who lost this round/cycle.
    for i in voter_array:
        for j in politicians_with_least_votes:
            i.remove(j)

    # This just helps keep count of who was kicked out
    for i in politicians_with_least_votes:
        expelled_politicians[i] = True

    # This returns again if there was no tie or win so there can be a new round/cycle
    return ranked_vote_counting()

# This is a loop that will run the election code as many times as the variable times_to_run is set to
while times_to_run >= 1:

    expelled_politicians = base_array_int.copy()

    times_to_run = times_to_run - 1

    politician_array = []
    popularity_total = 0

    # This code just sets of the popularity of the politicians and their ID which will
    # later be referenced in the voter's ballot code.
    for i in range(number_of_politicians):
        politician_array.append( politician() )
        if popularity_scale == 1:
            popularity_total += 1
        else:
            popularity_total += numpy.random.randint(1, popularity_scale)
        politician_array[i].popularity = popularity_total
        politician_array[i].id = i


    voter_array = []


    # This is the code to tell who voted for who in the election.
    for i in range(number_of_voters):
        voter_array.append([])
        temp_politician_array = []
        temp_popularity_total = popularity_total

        # This is making a nested array of all the politicians popularity and id
        for j in range(number_of_politicians):
            temp_politician_array.append([politician_array[j].popularity,politician_array[j].id])

        # Think about getting a Ranked Choice ballot in front of you where it asks you to rank
        # ALL of the politicians running. That is what this code does. It ranks the politicians
        # and weights (weights not sorts) where it ranks them by popularity
        for j in range(number_of_politicians):
            popularity_roll = random.randint(0,temp_popularity_total)

            # This code checks which politician the voter just rolled to vote on and then
            # sets up for the next vote
            for k in range(len(temp_politician_array)):
                if temp_politician_array[k][0] < popularity_roll:
                    continue
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
        # print(voter_array[i])


    # This line tells it to go to the ranked_vote_counting() function to count the vote and do the
    # election math
    result = ranked_vote_counting()

    # From here on what we are doing is recording the results in a text file called win_tie_record.txt
    # It saves the numbers of wins and ties along with a string of characters to tell what the
    # number of voters number of politicians and popularity scale was.

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
            file_data[line_to_write] = f'{result_numbers[0]}:{result_numbers[1]}'
            # print("TIE")
            # print(f'{result_numbers[0] + 1}:{result_numbers[1]}\n')
            if times_to_run == 0:
                print(f'{result_numbers[0]}:{result_numbers[1]}\n')
        else:
            result_numbers[1] = int(result_numbers[1]) + 1
            file_data[line_to_write] = f'{result_numbers[0]}:{result_numbers[1]}'
            # print("WIN")
            # print(f'{result_numbers[0]}:{result_numbers[1]+1}\n')
            if times_to_run == 0:
                print(f'{result_numbers[0]}:{result_numbers[1]}')
        file_read_write = open("win_tie_record.txt", "w")
        file_read_write.writelines(file_data)
        file_read_write.close()
        # print(10000-times_to_run)


# Citation
# Thank you Timmy Gergen for helping me bug check and helping to find the .copy() bug.