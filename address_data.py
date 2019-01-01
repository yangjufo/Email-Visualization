# coding=utf-8
import os
import csv
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
import string


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
            if temp_key in address_dict:
                name_index[address_dict[temp_key]] = name_data.ix[i, 0]

    result_dict = {}
    time_dict = {}
    for i in range(0, len(data_list)):
        path = os.path.join(data_dir, data_list[i])
        print(path)
        # path = "data/source_data/s.gallucci.csv"
        if os.path.isfile(path):
            data = pd.read_csv(path)
            for j in range(0, data.shape[0]):
                if data.ix[j, 2] in name_index:
                    name = name_index[data.ix[j, 2]]
                    if name in time_dict:
                        if data.ix[i, 11] in time_dict[name]:
                            continue
                        else:
                            time_dict[name] += [data.ix[i, 11]]
                    else:
                        time_dict[name] = [data.ix[i, 11]]
                    # print(data.ix[i, 0], data.ix[i, 11])
                    temp_hour = str(data.ix[i, 11])[str(data.ix[i, 11]).index(" ") + 1: str(data.ix[i, 11]).index(":")]
                    if not name in result_dict:
                        result_dict.setdefault(name, [0] * 24)
                    result_dict[name][int(temp_hour)] += 1

    result_file = "data/C2.1/hour_heat.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in result_dict.items():
            csv_writer.writerow([k, v])
        csvFile.close()


def count_relation():
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
            if temp_key in address_dict:
                name_index[address_dict[temp_key]] = name_data.ix[i, 0]

    nodes = {}
    for i in range(0, len(data_list)):
        path = os.path.join(data_dir, data_list[i])
        if os.path.isfile(path):
            temp_str = str(data_list[i])
            temp_id = temp_str[0:temp_str.rindex(".")]
            if temp_id in name_abbr:
                nodes[name_abbr[temp_id]] = 1
    result_file = "data/C2.1/name_relation_nodes.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in nodes.items():
            csv_writer.writerow([k, v])
        csvFile.close()

    links = {}
    for i in range(0, len(data_list)):
        path = os.path.join(data_dir, data_list[i])
        print(path)
        if os.path.isfile(path):
            temp_str = str(data_list[i])
            temp_id = temp_str[0:temp_str.rindex(".")]
            data = pd.read_csv(path)
            if not temp_id in name_abbr:
                continue
            for j in range(0, data.shape[0]):
                if data.ix[j, 2] in name_index:
                    name = name_index[data.ix[j, 2]]
                    if name in nodes:
                        if name in links:
                            links[name] += 1
                        else:
                            links[name] = 1
            result_file = "data/C2.1/name_relation_links.csv"
            with open(result_file, "a+") as csvFile:
                csv_writer = csv.writer(csvFile)
                for k, v in links.items():
                    csv_writer.writerow([k, name_abbr[temp_id], v])
                csvFile.close()


def address_relation():
    path = "data/C2.1/name_relation_links.csv"
    data = pd.read_csv(path)
    nodes = {}
    for i in range(0, data.shape[0]):
        if data.ix[i, 0] in nodes:
            nodes[data.ix[i, 0]] += data.ix[i, 2]
        else:
            nodes[data.ix[i, 0]] = data.ix[i, 2]
        if data.ix[i, 1] in nodes:
            nodes[data.ix[i, 1]] += data.ix[i, 2]
        else:
            nodes[data.ix[i, 1]] = data.ix[i, 2]
    result_file = "data/C2.1/name_relation_nodes.csv"
    with open(result_file, "a+") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in nodes.items():
            csv_writer.writerow([k, v])
        csvFile.close()


def classify_mails():
    name_abbr = {}
    name_data = pd.read_csv("data/Address2Name.csv")

    for i in range(0, name_data.shape[0]):
        temp_str = str(name_data.ix[i, 0])
        temp_abbr = temp_str[0:1] + "." + temp_str[temp_str.rindex(" ") + 1:len(temp_str)]
        name_abbr[temp_abbr] = temp_str

    total = 0
    final_dict = {}
    data_dir = "data/C2.2/notice_confluence_support_mails"
    data_list = os.listdir(data_dir)

    for i in range(0, len(data_list) - 1):
        path = os.path.join(data_dir, data_list[i])
        data = pd.read_csv(path)
        final_dict[str(data_list[i])[0:str(data_list[i]).rindex("_")]] = data.shape[0]
        total += data.shape[0]
    final_dict["inner"] = pd.read_csv("data/C2.2/inner_mail_list.csv").shape[0]
    final_dict["inner_other"] = final_dict["inner"] - total

    temp_dict = {}
    path = "data/C2.2/out_mail_by_domain/domain_filename_linenum.csv"
    data = pd.read_csv(path)
    for i in range(0, data.shape[0]):
        if data.ix[i, 0] in temp_dict:
            temp_dict[data.ix[i, 0]] += 1
        else:
            temp_dict[data.ix[i, 0]] = 1

    temp_dict = sorted(temp_dict.items(), reverse=True)
    total = 0
    for i in range(0, 15):
        total += temp_dict[i][1]
        final_dict[temp_dict[i][0]] = temp_dict[i][1]

    final_dict["outer"] = pd.read_csv("data/C2.2/outer_mail_list.csv").shape[0]
    final_dict["outer_other"] = final_dict["outer"] - total

    result_file = "data/C2.2/inner_outer_mail.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in final_dict.items():
            csv_writer.writerow([k, v])


def get_tokens(text1):
    remove_punctuation_map = dict((str(char), None) for char in string.punctuation)
    no_punctuation = text1
    for k, v in remove_punctuation_map.items():
        no_punctuation = no_punctuation.maketrans(k, " ")
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def extract_feature():
    with open("data/C2.3/subject_period_inner_inner_chat/top_subject_period_201402-201405.txt") as file:
        words_count = {}
        data = file.readlines()
        for line in data:
            words = line.split()
            time = int(words[-1])
            text1 = ""
            for w in words[0: -1]:
                text1 += w + " "
            text1 = ""
            for i in range(0, len(text1)):
                if ord(text1[i:i + 1]) < 128:
                    text1 += text1[i:i + 1]
            text = text1.lower()
            tokens = get_tokens(text)
            filtered = [w for w in tokens if w not in stopwords.words('english')]
            count = Counter(filtered)
            for k, v in count.items():
                if k in words_count:
                    words_count[k] += v * time
                else:
                    words_count[k] = v * time
        with open("data/C2.3/subject_period_inner_inner_chat/top_subject_feature_period_201402-201405.csv",
                  "wb") as csvFile:
            final_dict = sorted(words_count.items(), reverse=True)
            csv_writer = csv.writer(csvFile)
            for i in range(0, len(final_dict)):
                csv_writer.writerow(final_dict[i])


def collect_feature():
    data_dir = ["data/C2.3/subject_period_inner_inner_chat", "data/C2.3/subject_period_inner_outer_chat"]
    temp_dict = []
    for i in range(0, len(data_dir)):
        data_list = os.listdir(data_dir[i])
        for j in range(0, len(data_list)):
            if not data_list[j].endswith(".csv"):
                continue
            path = os.path.join(data_dir[i], data_list[j])
            if os.path.isfile(path):
                item = []
                data = pd.read_csv(path, header=None)
                for k in range(0, 100):
                    item += [{"word": data.ix[k, 0], "value": data.ix[k, 1]}]
                if "inner_inner" in data_dir[i]:
                    name = "inner"
                else:
                    name = "outer"
                if "top" in data_list[j]:
                    name += "_top"
                else:
                    name += "_add"
                name += str(data_list[j])[str(data_list[j]).rindex("_"):str(data_list[j]).rindex(".")]
                temp_dict += [{"name": name, "values": item}]

    result_file = "data/C2.3/subject_feature.json"
    with open(result_file, "wb") as jsonFile:
        jsonFile.write(json.dumps(temp_dict))


def collect_top_subject():
    data_dir = ["data/C2.3/subject_period_inner_inner_chat", "data/C2.3/subject_period_inner_outer_chat"]
    final_dict = []
    for i in range(0, len(data_dir)):
        data_list = os.listdir(data_dir[i])
        for j in range(0, len(data_list)):
            if not data_list[j].endswith(".txt"):
                continue
            if not (data_list[j].startswith("top") or data_list[j].startswith("new")):
                continue
            path = os.path.join(data_dir[i], data_list[j])
            if os.path.isfile(path):
                with open(path) as file:
                    item = []
                    data = file.readlines()
                    for line in data[0:15]:
                        text1 = ""
                        words = line.split()
                        time = words[-1]
                        for w in words[0: -1]:
                            text1 += w + " "
                        text = ""
                        for k in range(0, len(text1)):
                            if ord(text1[k:k + 1]) < 128:
                                text += text1[k:k + 1]
                        item += [{"subject": text, "value": time}]
                    if "inner_inner" in data_dir[i]:
                        name = "inner"
                    else:
                        name = "outer"
                    if "top" in data_list[j]:
                        name += "_top"
                    else:
                        name += "_add"
                    name += str(data_list[j])[str(data_list[j]).rindex("_"):str(data_list[j]).rindex(".")]
                    final_dict += [{"name": name, "values": item}]
    result_file = "data/C2.3/subject_top.json"
    with open(result_file, "wb") as jsonFile:
        jsonFile.write(json.dumps(final_dict))


def classify_by_subject():
    keywords = ["windows", "linux", "mac", "ios", "windows phone",
                "symbian", "blackberry", "android", "exploit",
                "rcs", "botnet", "malware", "0day", "ddos",
                "biglietti", "itinerary", "aerei",
                "delta", "pasticcini", "hotel", "anons",
                "pranzo", "gift", "maglietta", "ticket",
                "torta", "visa", "mastercard"]
    path = "data/C2.2/classify_mail_by_subject/subject.csv"
    data = pd.read_csv(path, header=None)
    final_dict = {}
    for i in range(0, len(keywords)):
        final_dict[keywords[i]] = 0
    for i in range(0, data.shape[0]):
        words = data.ix[i, 0].lower().split()
        for w in words:
            if w in keywords:
                final_dict[w] += 1
        if "windows phone" in data.ix[i, 0]:
            final_dict["windows phone"] += 1
            final_dict['windows'] -= 1
    result_file = "data/C2.2/classify_by_keywords.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k, v in final_dict.items():
            csv_writer.writerow([k, v])


def format_data():
    words_list = ["Windows", "Linux", "Mac", "IOS",
                  "Windows Phone", "Symbian", "Blackberry", "Android",
                  "Exploit", "RCS", "Botnet", "Malware", "0day", "DDOS"]

    result_file = "data/C2.3/subject_keywords_period_heat.csv"
    life_dict = {}
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        path = "data/C2.3/keywords_period_heat.csv"
        data = pd.read_csv(path, header=None)
        for i in range(0, data.shape[0]):
            if data.ix[i, 0] in ["Windows", "Linux", "Mac", "IOS",
                                 "Windows Phone", "Symbian", "Blackberry", "Android"]:
                csv_writer.writerow(["Work Mails-Operating System-" + data.ix[i, 0], data.ix[i, 1]])

            elif data.ix[i, 0] in ["Exploit", "RCS", "Botnet", "Malware", "0day", "DDOS"]:
                csv_writer.writerow(["Work Mails-Attack-" + data.ix[i, 0], data.ix[i, 1]])
            else:
                csv_writer.writerow(["Life Mail-" + life_dict[data.ix[i, 0]], data.ix[i, 1]])


def business_keywords_count():
    keywords = ["windows", "linux", "mac", "ios", "windows phone",
                "symbian", "blackberry", "android", "exploit",
                "rcs", "botnet", "malware", "0day", "ddos"]

    key_dict = {"windows": "Windows", "linux": "Linux", "mac": "Mac",
                "ios": "IOS", "windows phone": "Windows Phone", "symbian": "Symbian",
                "blackberry": "Blackberry", "android": "Android", "exploit": "Exploit",
                "rcs": "RCS", "botnet": "Botnet", "malware": "Malware", "0day": "0day",
                "ddos": "DDOS"}

    data_dir = ["data/C2.3/subject_period_inner_inner_chat", "data/C2.3/subject_period_inner_outer_chat"]
    final_dict = {}
    for i in range(0, len(data_dir)):
        data_list = os.listdir(data_dir[i])
        for j in range(0, len(data_list)):
            if not data_list[j].endswith(".txt"):
                continue
            if not (data_list[j].startswith("subject")):
                continue
            path = os.path.join(data_dir[i], data_list[j])
            print(path)
            if os.path.isfile(path):
                with open(path) as file:
                    data = file.readlines()
                    old_date = ""
                    for line in data:
                        words = line.split()
                        count = int(words[-1])
                        date = words[0]
                        if not old_date == date:
                            if not old_date == "":
                                for w in keywords:
                                    if not old_date + "," + key_dict[w] in final_dict:
                                        final_dict[old_date + "," + key_dict[w]] = 0
                            old_date = date

                        for w in words[1: -1]:
                            text = re.sub("[[]\(\)?!,.\"\']+", "", w)
                            if text.lower() in keywords:
                                if date + "," + key_dict[text.lower()] in final_dict:
                                    final_dict[date + "," + key_dict[text.lower()]] += count
                                else:
                                    final_dict[date + "," + key_dict[text.lower()]] = count
                            if "windows phone" in line:
                                if date + "," + "Windows Phone" in final_dict:
                                    final_dict[date + ",Windows Phone"] += count
                                else:
                                    final_dict[date + "," + "Windows Phone"] = count
                                if date + "," + "Windows" in final_dict:
                                    final_dict[date + ",Windows"] += count
                                else:
                                    final_dict[date + "," + "Windows"] = count

    final_dict = sorted(final_dict.items())
    result_file = "data/C2.3/keywords_period_heat.csv"
    with open(result_file, "wb") as csvFile:
        csv_writer = csv.writer(csvFile)
        for k in final_dict:
            csv_writer.writerow([k])


if __name__ == "__main__":
    business_keywords_count()
