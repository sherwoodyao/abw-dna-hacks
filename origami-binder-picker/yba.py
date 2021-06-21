import matplotlib.pyplot as plt
# test input
input_ex = [[1, 1, 2, "A"], [2, 2, 3, "B"], [3, 3, 4, "C"]]


def dict_graph_creator(input_list):
    input_dict = {}
    # new dictionary setup
    for z in range(1, len(input_list)+1):
        input_dict[str(z)] = input_list[z-1]
    # graph setup
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # graph plotting
    for x in input_list:
        ax.scatter([x[1]], [x[2]], color='gray', marker='o')
        for a, b in input_dict.items():
            if x[1] in b and x[2] in b:
                ax.annotate(a, (x[1]+0.01, x[2]+0.03))
    # display graph and return new dictionary
    # plt.show()
    # print(input_dict)
    return input_dict


conversion = dict_graph_creator(input_ex)


def modifyInput(input_dict):
    # loop setup
    letter_add = []
    converter_active = True
    print("---- List ex: 1, 2, 3 ---- Range ex: 1-3 ----")
    while converter_active:
        # user interaction
        prompt = input(f"Select staple(s) (1-{len(input_dict)}) or Quit: ")

        # quit program
        if prompt == "Quit":
            converter_active = False

        # more user interaction
        prompt2 = input("List, or a range? (L or R): ")

        # scan for unusable inputs
        if prompt not in input_dict.keys() and prompt2 != "R" and prompt2 != "L":
            print("Selection out of range.")

        # converting input to add to list
        else:
            # begin scanning through dictionary
            # for number, cords in input_dict.items():
            multiple_cut = prompt.split(", ")
            range_cut = prompt.split("-")
            if prompt2 == "L":
                try:
                    for x in multiple_cut:
                        staple_in = False
                        if input_dict[x][3] not in letter_add:
                            letter_add.append(input_dict[x][3])
                        else:
                            staple_in = True
                    else:
                        if staple_in:
                            print(f"Selected staples already modified.")
                except KeyError:
                    print("Selection out of range.")
            elif prompt2 == "R":
                if len(range_cut) == 1:
                    print("Range selected but only one entry detected.")
                    break
                try:
                    for x in range(int(range_cut[0]), int(range_cut[1])+1):
                        staple_in = False
                        if input_dict[str(x)][3] not in letter_add:
                            letter_add.append(input_dict[str(x)][3])
                        else:
                            staple_in = True
                    else:
                        if staple_in:
                            print(f"Selected staples already modified.")
                except IndexError:
                    print("Selection out of range.")
        if len(letter_add) > 0:
            print(letter_add)
    return letter_add


modifyInput(conversion)

# input_output = {
#     "1": [1.3, 2, 3.90141, "A"],
#     "2": [5.2, 8, 9, "B"],
#     "3": [4.4, 435, 423, "C"],
#     "4": [6, 315, 314, "D"],
#     "5": [3, 132, 2.2222, "Q"]
# }
