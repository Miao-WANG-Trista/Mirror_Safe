def read_test(file_path):
    """
        Parse the information in the test case txt file

        Parameters
        ----------
        file_path: string
            the path of test case file

        Returns
        -------
        r: int
            the number of rows
        c: int
            the number of columns
        joint_list: a list of tuples of 3
            joint_mirror_list, each element of which will be like (row_number, col_number,'left'/'right')
    """
    data = []
    with open(file_path) as f:
        for line in f.readlines():
            temp = [int(i) for i in line.split()]
            data.append(temp)

    r = data[0][0]
    c = data[0][1]
    m = data[0][2]
    n = data[0][3]

    joint_list = []
    # a joint list of tuples of 3
    for i in range(1, m + 1):
        row, col = data[i]
        joint_list.append((row, col, "left"))

    for i in range(m + 1, m + n + 1):
        row, col = data[i]
        joint_list.append((row, col, "right"))

    return r, c, joint_list

# create two dictionaries mapping orientation changes
LEFT_MIRROR = {
    (0, 1): (-1, 0), # for example, once meeting a / mirror, (0,1): right will be changed to (-1,0) :up
    (-1, 0): (0, 1),
    (1, 0): (0, -1),
    (0, -1): (1, 0)
}

RIGHT_MIRROR = {
    (0, 1): (1, 0),
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
    (0, -1): (-1, 0)
}
