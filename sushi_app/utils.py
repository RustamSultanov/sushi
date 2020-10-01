def create_dict_from_choices(original_list, revert=False):
    """
    создаёт юзабельный словарь из Django choice списка
    """
    created_dict = dict()
    for i in original_list:
        if len(i) > 2:
            return False
        else:
            if not revert:
                created_dict[i[0]] = i[1]
            else:
                created_dict[i[1]] = i[0]
    return created_dict
