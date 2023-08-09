
import csv
import json
import random


DATA_PATH = 'panitia-jbc-2023.json'
TOTAL_TEAMS = 6
DIVISIONS = ['Inti', 'EO', 'CO', 'LOA', 'LoC', '3D',
             'MPR', 'Sponsorship', 'Fundraising']
EXCLUDED_DIVISIONS = ['LOA']


def get_lacking_teams(teams):
    """
    Returns the indexes of teams that is still lacking in members.
    """

    minimum = min([len(i) for i in teams])
    return [idx for idx, team in enumerate(teams)
            if len(team) == minimum]


def get_lacking_division(teams, division):
    """
    Returns the indexes of teams that is still lackingin a specified division.
    """

    filtered_teams = [[member for member in team
                       if member['division'] == division]
                      for team in teams]

    minimum = min([len(team) for team in filtered_teams])


    return [idx for idx, filtered_team in enumerate(filtered_teams)
            if len(filtered_team) == minimum]


def recommended_team(
        teams,
        currrent_division,
        on_divisions=False,
        maximum_members=None):
    """
    Returns an index on which team is best suited to be append upon.

    By default, the recommended team will be set to a team's lacking member.
    It can be changed on a team's lacking division by setting the variable
    `on_lacking_division` to true.
    """

    lacking_teams = get_lacking_teams(teams)
    lacking_divisions = get_lacking_division(teams, currrent_division)
    excluded_teams_index = []

    if maximum_members is not None:
        excluded_teams_index = [idx for idx, team in enumerate(teams)
                                if len(team) >= maximum_members]


    for excluded_team_index in excluded_teams_index:
        if excluded_team_index in lacking_teams:
            lacking_teams.remove(excluded_team_index)
        if excluded_team_index in lacking_divisions:
            lacking_divisions.remove(excluded_team_index)

    # get intersection of lacking teams and member's division
    recommended_teams = list(set(lacking_teams).intersection(lacking_divisions))

    # returns any reccomended teams if any intersection exist
    if len(recommended_teams) > 0:
        return random.choice(recommended_teams)


    if on_divisions and len(lacking_divisions) > 0:
        current_idx = lacking_divisions[0]
        current_amount = len(teams[current_idx])

        # update curr_idx to the least membered team
        for idx in lacking_divisions:
            amount = len(teams[idx])

            if current_amount > amount:
                current_idx = idx
                current_amount = amount

    else:
        current_idx = lacking_teams[0]
        current_amount = len([member for member in teams[current_idx]
                              if member['division'] == currrent_division])

        # update curr_idx to the least membered division
        for idx in lacking_teams:
            amount = len([member for member in teams[idx]
                          if member['division'] == currrent_division])

            if current_amount > amount:
                current_idx = idx
                current_amount = amount


    return current_idx


def insert_members(teams, total_teams, members):
    """
    Inserts the teams list with the members.
    Note that the variable `teams` will be updated.

    Each team will be first insert based off a team's least membered division,
    until a threshold is met that changes the condition to least membered team.
    """

    # minimum amount of members needed to be inserted based on division
    threshold = 5

    current_max_members = max([len(team) for team in teams])
    members_remain = len(members)
    empty_slots = sum([current_max_members - len(team) for team in teams])
    max_members = (members_remain - empty_slots) // total_teams + current_max_members

    if (members_remain - empty_slots) % total_teams > 0:
        max_members += 1

    while members_remain > 0:
        random_idx = random.randint(0, members_remain - 1)
        member = members.pop(random_idx)
        is_by_division = members_remain >= threshold

        # get the recommended team's index
        idx = recommended_team(teams, member['division'],
                               is_by_division, max_members)

        teams[idx].append(member)
        members_remain -= 1


def generate_upgrading_teams(members, total_teams, excluded_divisions=[]):
    teams = [[] for _ in range(total_teams)]

    # filter out excluded divisions
    filtered_members = [member for member in members
                        if member['division'] not in excluded_divisions]

    # seperate each members based on specific attribtutes
    kabinets = [member for member in filtered_members if member['isKabinet']]
    mabas = [member for member in filtered_members
             if not member['isKabinet'] and member['isMaba']]
    kating_non_kabinets = [member for member in filtered_members
                           if not member['isKabinet'] and not member['isMaba']]

    # insert to the teams in a orderly fashion
    insert_members(teams, total_teams, kabinets)
    insert_members(teams, total_teams, mabas)
    insert_members(teams, total_teams, kating_non_kabinets)


    return teams


if __name__ == '__main__':

    # import data from json
    with open(DATA_PATH, 'r') as json_file:
        data = json.load(json_file)

    teams = generate_upgrading_teams(data, TOTAL_TEAMS, EXCLUDED_DIVISIONS)


    # export teams to csv format
    with open('output.csv', 'w', newline='') as csv_file:
        w = csv.writer(csv_file)
        formatted_teams = []
        max_team_member = max([len(team) for team in teams])

        for team in teams:

            # filter only the full name attribute
            formatted_team = [member['fullName'] for member in team]
            formatted_team.sort()

            # insert empty members to accomodate maximum team members
            while len(formatted_team) < max_team_member:
                formatted_team.append('')

            formatted_teams.append(formatted_team)

        # transpose the teams to fix the output display
        formatted_teams = [list(row) for row in zip(*formatted_teams)]

        # write to csv file
        w.writerow([f'Team {i+1}' for i in range(TOTAL_TEAMS)])
        w.writerows(formatted_teams)


    # export teams metadata to json format
    with open('output.json', 'w') as json_file:
        contents = {}

        for i, team in enumerate(teams):
            divisions = {}
            mabas = 0
            kabinets = 0
            kating_non_kabinets = 0

            # update each division's value
            for division in DIVISIONS:
                if division in EXCLUDED_DIVISIONS:
                    continue

                # insert each division amount
                divisions[division] = len([member for member in team
                                           if member['division'] == division])

            # update each member section's value
            for member in team:
                if member['isKabinet']:
                    kabinets += 1
                else:
                    if member['isMaba']:
                        mabas += 1
                    else:
                        kating_non_kabinets += 1

            content = {
                'total': mabas + kabinets + kating_non_kabinets,
                'mabas': mabas,
                'kabinets': kabinets,
                'katingNonKabinets': kating_non_kabinets,
                'divisions': divisions,
            }

            # insert the content
            contents[f'Team {i+1}'] = content

        # write to json file
        output = json.dumps(contents, indent=4, separators=(',', ': '))
        json_file.write(output)


    print(f'Successfully created {TOTAL_TEAMS} teams!')
