# -*- coding: utf-8 -*

#列表函数生成器重新生成需求格式
def list_of_groups(init_list, childern_list_len):

    list_of_groups = zip(*(iter(init_list),) *childern_list_len)

    end_list = [list(i) for i in list_of_groups]

    count = len(init_list) % childern_list_len

    end_list.append(init_list[-count:]) if count !=0 else end_list

    return end_list


if __name__ == '__main__':

    a = [1,2,3,4,5,6]

    print(list_of_groups(a,3))