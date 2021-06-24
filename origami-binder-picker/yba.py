import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import csv
import pandas

input_ex = [[1, 1, 2, "A"], [2, 2, 3, "B"], [3, 3, 4, "C"]]
input_ex_v2 = [[1, 3, 95, "A", "I", "3'"], [2, 1, 2, "B", "O", "3'"], [3, 3, 4, "C", "I", "5'"]]
oligo_dict_ex = {
    "A": "AAAAAAAAAAAAAAA",
    "B": "GGGGGGGGGGGGGGG",
    "C": "CCCCCCCCCCCCCCC",
    "D": "TTTTTTTTTTTTTTT"
}


def sort(sub_li, num):
    sub_li.sort(key=lambda x: x[num])
    return sub_li


def checklist(input_list, user_y='', user_z='', user_oligo='', user_direc='', user_prime=''):
    t1 = False
    t2 = False
    t3 = False
    t4 = False
    t5 = False
    range_y = user_y.split("-")
    range_z = user_z.split("-")
    multiple_cut = user_oligo.split(",")
    user_oligo_list = [x.replace(" ", "") for x in multiple_cut]

    if user_y == '':
        t1 = True
    else:
        for x in range(int(range_y[0]), int(range_y[1]) + 1):
            if input_list[1] == x:
                t1 = True
                continue

    if user_z == '':
        t2 = True
    else:
        for x in range(int(range_z[0]), int(range_z[1]) + 1):
            if input_list[2] == x:
                t2 = True
                continue

    if user_oligo == '':
        t3 = True
    else:
        for x in user_oligo_list:
            if input_list[3] == x:
                t3 = True
                continue

    if user_direc == '':
        t4 = True
    else:
        if user_direc == "U" or user_direc == "u":
            user_direc = "I"
        elif user_direc == "D" or user_direc == "d":
            user_direc = "O"
        if user_direc == input_list[4]:
            t4 = True

    if user_prime == '':
        t5 = True
    else:
        if input_list[5] == user_prime:
            t5 = True

    if t1 and t2 and t3 and t4 and t5:
        return True


# Function that takes a list of lists in the form [x, y, z, oligo_ID, in/out, 5'/3']
# Also uses the list of lists to create a plot graph.


def dict_graph_creator(input_list):
    input_dict = {}
    range_ys = ['']
    range_zs = ['']
    oligo_ids = ['']
    directions = ['']
    primes = ['']
    graph_runner = True

    # Reformats the list into a dictionary
    for z in range(1, len(input_list) + 1):
        input_dict[str(z)] = input_list[z - 1]

    while graph_runner:
        # User selects/inputs restrictions
        main_prompt = input("[A]dd restrictions, [R]emove restrictions or [G]raph: ")

        if main_prompt == "A" or main_prompt == "a":
            menu_select = input("Select filter: Range_[Y], Range_[Z], [O]ligo ID, [D]irection, or 3/5 [P]rime: ")

            if menu_select == "Y" or menu_select == "y":
                sort(input_list, 1)
                user_range_y = input(f"Range of Y values? ({input_list[0][1]}-{input_list[-1][1]}nm): ")
                range_y = user_range_y.split("-")

                if len(range_y) == 1:
                    print("Command only accepts range.")
                    continue
                else:
                    range_ys.append(user_range_y)

            elif menu_select == "Z" or menu_select == "z":
                sort(input_list, 2)
                user_range_z = input(f"Range of Z values? ({input_list[0][2]}-{input_list[-1][2]}nm): ")
                range_z = user_range_z.split("-")

                if len(range_z) == 1:
                    print("Command only accepts range.")
                    continue
                else:
                    range_zs.append(user_range_z)

            elif menu_select == "O" or menu_select == "o":
                user_oligo_id = input("Oligo IDs (Ex: A, B, C): ")
                oligo_ids.append(user_oligo_id)

            elif menu_select == "D" or menu_select == "d":
                user_direction = input("[U]p or [D]own?: ")
                directions.append(user_direction)

            elif menu_select == "P" or menu_select == "p":
                user_prime = input("[5'] or [3']?: ")
                primes.append(user_prime)
            else:
                print("Invalid input.")

        elif main_prompt == "R" or main_prompt == "r":
            range_ys.clear()
            range_zs.clear()
            oligo_ids.clear()
            directions.clear()
            primes.clear()
            range_ys = ['']
            range_zs = ['']
            oligo_ids = ['']
            directions = ['']
            primes = ['']

        elif main_prompt == "G" or main_prompt == "g":
            # Base construction of graph
            fig = plt.figure()
            ax = fig.add_subplot(111)
            # plt.ion()

            for x in input_list:
                color = ""
                marker = ""

                if x[4] == "I":
                    color = "blue"
                elif x[4] == "O":
                    color = "red"

                if x[5] == "5'":
                    marker = 'o'
                elif x[5] == "3'":
                    marker = ','

                # Set up legend
                colors = ["red", "blue"]
                circles = [Line2D([0], [0], color=x, marker="o", linewidth=0) for x in colors]
                squares = [Line2D([0], [0], color=x, marker="s", linewidth=0) for x in colors]
                shapes = circles + squares
                # plt.draw()
                # plt.pause(0.001)

                # sort1 = sort(input_list, 1)
                # sort2 = sort(input_list, 2)
                # ax.set_xlim([sort1[0][1]-2, sort1[-1][1]+2])
                # ax.set_ylim([sort2[0][2]-2, sort2[-1][2]+2])

                # Plot/create legend if meets filters or if no filters
                if checklist(x, range_ys[-1], range_zs[-1], oligo_ids[-1], directions[-1], primes[-1]):
                    ax.scatter([x[1]], [x[2]], color=color, marker=marker)
                    ax.legend(shapes, ["5' down", "5' up", "3' down", "3' up"], bbox_to_anchor=(1.1, 1.05))

                    # Marks the points
                    for a, b in input_dict.items():
                        if x[1] == b[1] and x[2] == b[2]:
                            ax.annotate(a, (x[1] + 0.0079*x_len, x[2] + 0.0079*y_len))

            # print(input_dict)
            plt.show()
    return input_dict


conversion = dict_graph_creator(input_ex_v2)


# Function that sets up the modified oligonucleotide dictionary
# Uses the dictionary produced from dict_graph_creator and an oligonucleotide dict


def modify_input(input_dict, oligo_dict):
    # Function variable setup
    letter_add = []
    code_display = []
    key_display = []
    mod_dict = {
        "modifier": "strand"
    }
    modified_oligo_dict = {
        "letter": "modified_strand"
    }
    converter_active = True
    staple_in = False
    while converter_active:
        # Asks to configure modifications dict, configure staples, load/save, or exit program
        general_prompt = input(f"[E]dit modification types, [S]elect staples, [L]oad/[Save], or [Q]uit: ")

        # Quits program
        if general_prompt == "Q" or general_prompt == "q":
            converter_active = False
            continue

        # Section to configure modifications dict
        elif general_prompt == "E" or general_prompt == "e":
            edit_input = input("[A]dd modification, [V]iew modifications, [D]elete, or [S]ave/[L]oad: ")

            # Add to modifications dict
            if edit_input == "A" or edit_input == "a":
                print(f"Modifications:")
                print(*key_display, sep=", ")
                prompt3v1 = input("What is the reference name?: ")
                prompt4 = input("What is the modification sequence? (5' -> 3'): ")
                mod_dict[prompt3v1] = prompt4
                for modifier, strand in mod_dict.items():
                    if modifier != "modifier" and modifier not in key_display:
                        key_display.append(modifier)
                print(f"Modifications:")
                print(*key_display, sep=", ")

            # View modifications dict
            elif edit_input == "V" or edit_input == "v":
                if len(mod_dict) == 0:
                    print("There are no modifications currently loaded.")

                else:
                    first = next(iter(mod_dict))
                    for xy, zy in mod_dict.items():
                        if xy == first:
                            continue
                        else:
                            print(f"{xy} : {zy}")

            # Delete modifications dict elements
            elif edit_input == "D" or edit_input == "d":
                print("Modifications:")
                print(*key_display, sep=", ")
                delete_prompt = input(f"Delete [A]ll or [S]elect?: ")

                if delete_prompt == "A" or delete_prompt == "a":
                    mod_dict.clear()
                    key_display.clear()

                elif delete_prompt == "S" or delete_prompt == "s":
                    select_delete = input("Which would you like to delete?: ")
                    delete_split = select_delete.split(",")
                    delete_split_fix = [x.replace(" ", "") for x in delete_split]

                    try:
                        for b in delete_split_fix:
                            del mod_dict[b]
                            key_display.remove(b)

                    except KeyError:
                        print("Selection does not exist.")
                else:
                    print("Enter A/a or S/s.")

            # Save modifications dict to csv file
            elif edit_input == "S" or edit_input == "s":
                save_input = input("What file would you like to save to? (Ex: modifications): ")

                with open(f"{save_input}.csv", "w") as file:
                    writer = csv.writer(file)
                    for key, value in mod_dict.items():
                        writer.writerow([key, value])

                print("Successfully saved.")

            # Load modifications data from csv file
            elif edit_input == "L" or edit_input == "l":
                load_input = input("What file would you like to load? (Ex: modifications): ")

                try:
                    mod_data = pandas.read_csv(f"{load_input}.csv").to_dict()
                    mod_df = pandas.DataFrame(mod_data)
                    for (index, row) in mod_df.iterrows():
                        mod_dict[row.modifier] = row.strand
                    for modifier, strand in mod_dict.items():
                        if modifier != "modifier" and modifier not in key_display:
                            key_display.append(modifier)

                except FileNotFoundError:
                    print("No records of previously saved files.")

                except AttributeError:
                    print("File corrupted, select another.")

                else:
                    print("Successfully loaded.")

        # Modify staples/configure modified oligonucleotide dictionary
        elif general_prompt == "S" or general_prompt == "s":
            # Gets user inputs and checks for validity
            mod_select = input("What modification?: ")

            if mod_select not in mod_dict.keys():
                print("Invalid modification choice.")
                continue

            prime_select = input("5' or 3'?: ")

            if prime_select != "5'" and prime_select != "3'":
                print("Invalid prime choice.")
                continue

            list_range = input("List, or a range? (L or R): ")

            if list_range != "R" and list_range != "r" and list_range != "L" and list_range != "l":
                print("Pick L/l or R/r.")

            else:
                # Configure staples/ modified oligonucleotide dict using a list
                if list_range == "L" or list_range == "l":
                    print("---- List ex: 1, 2, 3 ----")
                    list_input = input(f"List: ")
                    multiple_cut = list_input.split(",")
                    multiple_cut_fix = [x.replace(" ", "") for x in multiple_cut]

                    try:
                        for x in multiple_cut_fix:
                            staple_in = False
                            if (input_dict[x][3], input_dict[x][5]) not in letter_add:
                                code_display.append(x)
                                letter_add.append((input_dict[x][3], input_dict[x][5]))
                                if prime_select == "3'":
                                    modified_oligo_dict[input_dict[x][3]] = \
                                        oligo_dict[input_dict[x][3]] + mod_dict[mod_select]

                                elif prime_select == "5'":
                                    modified_oligo_dict[input_dict[x][3]] = \
                                        mod_dict[mod_select] + oligo_dict[input_dict[x][3]]
                            else:
                                staple_in = True
                        else:
                            if staple_in:
                                print(f"Selected staples already modified.")
                    except KeyError:
                        print("Invalid entry.")

                # Configure staples/ modified oligonucleotide dict using a range
                elif list_range == "R" or list_range == "r":
                    print("---- Range ex: 1-3 ----")
                    range_input = input(f"Range: ")
                    range_cut = range_input.split("-")

                    if len(range_cut) == 1:
                        print("Range selected but only one entry detected.")

                    try:
                        for x in range(int(range_cut[0]), int(range_cut[1]) + 1):
                            zb = str(x)
                            staple_in = False
                            if (input_dict[zb][3], input_dict[zb][5]) not in letter_add:
                                code_display.append(zb)
                                letter_add.append((input_dict[zb][3], input_dict[zb][5]))
                                if prime_select == "3'":
                                    modified_oligo_dict[input_dict[zb][3]] = \
                                        oligo_dict[input_dict[zb][3]] + mod_dict[mod_select]

                                elif prime_select == "5'":
                                    modified_oligo_dict[input_dict[zb][3]] = \
                                        mod_dict[mod_select] + oligo_dict[input_dict[zb][3]]
                            else:
                                staple_in = True
                        else:
                            if staple_in:
                                print(f"Selected staples already modified.")
                    except IndexError:
                        print("Invalid entry.")

            # Prints out staples and modified oligonucleotide dict
            if len(code_display) > 0:
                fixed1 = ''
                for letter, modded_strand in modified_oligo_dict.items():
                    if mod_dict[mod_select] in modded_strand:
                        fixed1 = modded_strand.replace(mod_dict[mod_select],
                                                       ("\033[4m" + mod_dict[mod_select] + "\033[0m"))
                    print(letter + " : " + fixed1)
                print(code_display)

        # Saves oligonucleotide dict
        elif general_prompt == "Save":
            save_input = input("What file would you like to save to? (Ex: modifications): ")
            with open(f"{save_input}.csv", "w") as file:
                writer = csv.writer(file)
                for key, value in modified_oligo_dict.items():
                    writer.writerow([key, value])
            print("Successfully saved.")

        # Loads oligonucleotide dict
        elif general_prompt == "L" or general_prompt == "l":
            load_input = input("What file would you like to load? (Ex: modifications): ")
            try:
                mod_data = pandas.read_csv(f"{load_input}.csv").to_dict()
                mod_df = pandas.DataFrame(mod_data)
                for (index, row) in mod_df.iterrows():
                    modified_oligo_dict[row.letter] = row.modified_strand
            except FileNotFoundError:
                print("No records of previously saved files.")
            except AttributeError:
                print("File corrupted, select another.")
            else:
                print("Successfully loaded.")
    return modified_oligo_dict

# modify_input(conversion, oligo_dict_ex)
