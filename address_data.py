import os
import csv
import pandas as pd


def count_mail():
    data_dir = "data/source_data"
    data_list = os.listdir(data_dir)
    address_dict = {}
    address_value = pd.read_csv("data/C2.1/OHackingString2dotCom_format.csv")
    for i in range(0, address_value.shape[0]):
        address_dict[address_value.ix[i, 1]] = address_value.ix[i, 0]
    name_index = {}
    name_data = pd.read_csv("data/Address2Name.csv")
    for i in range(0, name_data.shape[0]):
        for temp_key in str(name_data.ix[i, 1]).split(';'):
            name_index[temp_key] = name_data.ix[i, 0]
            if address_dict.has_key(temp_key):
                name_index[address_dict[temp_key]] = name_data.ix[i, 0]

    result_dict = {}
    time_dict = {}
    for i in range(0, len(data_list)):
        path = os.path.join(data_dir, data_list[i])
        print path
        # path = "data/source_data/s.gallucci.csv"
        if os.path.isfile(path):
            data = pd.read_csv(path)
            for i in range(0, data.shape[0]):
                if name_index.has_key(data.ix[i, 2]):
                    name = name_index[data.ix[i, 2]]
                    if time_dict.has_key(name):
                        if data.ix[i, 11] in time_dict[name]:
                            continue
                        else:
                            time_dict[name] += [data.ix[i, 11]]
                    else:
                        time_dict[name] = [data.ix[i, 11]]
                    # print(data.ix[i, 0], data.ix[i, 11])
                    temp_hour = str(data.ix[i, 11])[str(data.ix[i, 11]).index(" ") + 1: str(data.ix[i, 11]).index(":")]
                    if not result_dict.has_key(name):
                        result_dict.setdefault(name, [0] * 24)
                    result_dict[name][int(temp_hour)] += 1

    result_file = "data/C2.1/hour_heat.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in result_dict.iteritems():
            csv_writer.writerow([k, v])
        csvFile.close()


def count_relation():
    global temp_abbr
    data_dir = "data/source_data"
    data_list = os.listdir(data_dir)
    address_dict = {}
    address_value = pd.read_csv("data/C2.1/OHackingString2dotCom_format.csv")
    for i in range(0, address_value.shape[0]):
        address_dict[address_value.ix[i, 1]] = address_value.ix[i, 0]
    name_index = {}
    name_abbr = {}
    name_data = pd.read_csv("data/Address2Name.csv")

    for i in range(0, name_data.shape[0]):
        temp_str = str(name_data.ix[i, 0])
        temp_abbr = temp_str[0:1] + "." + temp_str[temp_str.rindex(" ") + 1:len(temp_str)]
        name_abbr[temp_abbr] = temp_str
        for temp_key in str(name_data.ix[i, 1]).split(';'):
            name_index[temp_key] = name_data.ix[i, 0]
            if address_dict.has_key(temp_key):
                name_index[address_dict[temp_key]] = name_data.ix[i, 0]

    nodes = {}
    for i in range(0, len(data_list)):
        path = os.path.join(data_dir, data_list[i])
        if os.path.isfile(path):
            temp_str = str(data_list[i])
            temp_id = temp_str[0:temp_str.rindex(".")]
            if name_abbr.has_key(temp_id):
                nodes[name_abbr[temp_id]] = 1
    result_file = "data/C2.1/name_relation_nodes.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in nodes.iteritems():
            csv_writer.writerow([k, v])
        csvFile.close()

    links = {}
    for i in range(0, len(data_list)):
        path = os.path.join(data_dir, data_list[i])
        print path
        if os.path.isfile(path):
            temp_str = str(data_list[i])
            temp_id = temp_str[0:temp_str.rindex(".")]
            data = pd.read_csv(path)
            if not name_abbr.has_key(temp_id):
                continue
            for i in range(0, data.shape[0]):
                if name_index.has_key(data.ix[i, 2]):
                    name = name_index[data.ix[i, 2]]
                    if nodes.has_key(name):
                        if links.has_key(name):
                            links[name] += 1
                        else:
                            links[name] = 1
            result_file = "data/C2.1/name_relation_links.csv"
            with open(result_file, "a+") as csvFile:
                csv_writer = csv.writer(csvFile)
                for k, v in links.iteritems():
                    csv_writer.writerow([k, name_abbr[temp_id], v])
                csvFile.close()


def address_relation():
    path = "data/C2.1/name_relation_links.csv"
    data = pd.read_csv(path)
    nodes = {}
    for i in range(0, data.shape[0]):
        if nodes.has_key(data.ix[i, 0]):
            nodes[data.ix[i, 0]] += data.ix[i, 2]
        else:
            nodes[data.ix[i, 0]] = data.ix[i, 2]
        if nodes.has_key(data.ix[i, 1]):
            nodes[data.ix[i, 1]] += data.ix[i, 2]
        else:
            nodes[data.ix[i, 1]] = data.ix[i, 2]
    result_file = "data/C2.1/name_relation_nodes.csv"
    with open(result_file, "a+") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in nodes.iteritems():
            csv_writer.writerow([k, v])
        csvFile.close()


if __name__ == "__main__":
    address_relation()
