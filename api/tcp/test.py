flag = 1
multipart_dict = {}


def split_multipart_databody(list_value: list):
    global flag
    global multipart_dict
    temp_list = []
    for i in range(0, len(list_value)):
        if isinstance(list_value[i], list) and (list_value[-1] != list_value[i]):
            for j in list_value[i:]:
                temp_list.append(j)
            multipart_dict[flag] = temp_list
            flag += 1
            return split_multipart_databody(list_value[i])
        elif isinstance(list_value[i], list) and (list_value[-1] == list_value[i]):
            temp_list.append(list_value[i])
            multipart_dict[flag] = temp_list
            flag += 1
            return split_multipart_databody(list_value[i])
        else:
            temp_list.append(list_value[i])
    multipart_dict[flag] = temp_list


if __name__ == '__main__':
    flag = 1
    multipart_dict = {}
    list_a = ['H', 2, ['H', 3, ['H', 4, ['ABCDEF', 5, 6, 7, 8, 9, ['H', 16, ['BBHH', 11, 12, 13, 14], 'FGH', 4, 5, 7],
                                         'UIO', 8, 9, 10]]]]
    list_b = ['H', 2, 2, 2, ['H', 3, ['BBHH', 11, 12, 13, 14]], 'HH', 2, 3]
    list_c = ['H', 2, 2, 2, ['HH', 2, 3], 4]
    list_d = ['H', 2, 2, 2, 4]
    split_multipart_databody(list_d)
    print(multipart_dict)