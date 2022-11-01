import json
import re
def read_json(path):
    t_file = open(path, "r", encoding = "utf-8")
    json_data = json.load(t_file)
    t_file.close()
    return json_data
def write_json(json_data, path):
    t_file = open(path, "w", encoding = "utf-8")
    json.dump(json_data, t_file)
    t_file.close()
def build_pdf_label_list(pdf_list, valid_sample_list):
    pdf_label_list = []
    seq_list = []
    for seq in valid_sample_list:
        t_pdf = pdf_list[seq]
        pdf_label_list.append(t_pdf)
        seq_list.append(seq)
    return pdf_label_list, seq_list
def build_hypoSen_dict(pdf_label_list):
    sen_list = []
    type_list = []
    for pdf_seq, pdf_obj in enumerate(pdf_label_list):
        t_h_sen_objs = pdf_obj["h_extract_obj"]["h_sen_objs"]
        t_hypo_sen_objs = pdf_obj["h_extract_obj"]["hypo_sen_objs"]
        for t_h_sen_obj in t_h_sen_objs:
            sen_list.append(t_h_sen_obj["h_sen"])
            if t_h_sen_obj["type"] == "hypo":
                t_hypo_sen_obj = t_hypo_sen_objs[t_h_sen_obj["type_seq"]]
                if ("hypo_objs" in t_hypo_sen_obj):
                    t_hypo_obj = t_hypo_sen_obj["hypo_objs"][0]
                    if (type(t_hypo_obj["l"]) == list) and (len(t_hypo_obj["l"]) == 5):
                        type_list.append(1)
                        continue
            type_list.append(0)
    t_dict = {}
    t_dict["sen"] = sen_list
    t_dict["type"] = type_list

    return t_dict
def build_hypoSen_pred_dict(pdf_label_list, seq_list):
    sen_list = []
    type_list = []
    pdf_seq_list = []
    for pdf_seq, pdf_obj in enumerate(pdf_label_list):
        t_h_sen_objs = pdf_obj["h_extract_obj"]["h_sen_objs"]
        for t_h_sen_obj in t_h_sen_objs:
            sen_list.append(t_h_sen_obj["h_sen"])
            type_list.append(0)
            pdf_seq_list.append(seq_list[pdf_seq])
    t_dict = {}
    t_dict["sen"] = sen_list
    t_dict["type"] = type_list
    t_dict["pdf_seq"] = pdf_seq_list
    return t_dict
def build_resuSen_dict(pdf_label_list):
    sen_list = []
    type_list = []
    for pdf_seq, pdf_obj in enumerate(pdf_label_list):
        t_h_sen_objs = pdf_obj["h_extract_obj"]["h_sen_objs"]
        t_len = len(t_h_sen_objs)
        for t_h_sen_obj_seq, t_h_sen_obj in enumerate(t_h_sen_objs):
            sen_list.append(t_h_sen_obj["h_sen"])
            if (t_h_sen_obj["type"] == "resu") or (t_h_sen_obj["type"] == "resu_nodata"):
                type_list.append(1)
            else:
                type_list.append(0)
    t_dict = {}
    t_dict["sen"] = sen_list
    t_dict["type"] = type_list

    return t_dict
def build_all_sen(resu_sen_pred_dict):
    t_dict = {}
    for seq in resu_sen_pred_dict["pdf_seq"]:
        t_dict[seq] = []
    for i, seq in enumerate(resu_sen_pred_dict["pdf_seq"]):
        t_dict[seq].append(resu_sen_pred_dict["sen"][i])
    return t_dict
def build_resuTypeSen_dict(pdf_label_list):
    sen_list = []

    count1 = 0
    count2 = 0
    count_hypo = 0
    for pdf_seq, pdf_obj in enumerate(pdf_label_list):
        t_hypoid_dict = {}
        t_hypo_sen_objs = pdf_obj["h_extract_obj"]["hypo_sen_objs"]
        for t_hypo_sen_obj in t_hypo_sen_objs:
            if "hypo_objs" in t_hypo_sen_obj:
                for t_hypo_obj in t_hypo_sen_obj["hypo_objs"]:
                    
                    t_hypoid_dict[t_hypo_obj["attr"][0]] = 0
        count_hypo += len(t_hypoid_dict.keys())
        
        t_h_sen_objs = pdf_obj["h_extract_obj"]["h_sen_objs"]
        t_resu_sen_objs = pdf_obj["h_extract_obj"]["resu_sen_objs"]

        t_len = len(t_h_sen_objs)
        for t_h_sen_obj_seq, t_h_sen_obj in enumerate(t_h_sen_objs):
            if (t_h_sen_obj["type"] == "resu") and (t_h_sen_obj_seq != t_len-1):
                t_type_seq = t_h_sen_obj["type_seq"]
                t_resu_sen_obj = t_resu_sen_objs[t_type_seq]

                if "resu_objs" in t_resu_sen_obj:
                    t_sen = t_h_sen_obj["h_sen"]
                    t_codedtext = t_h_sen_obj["codedtext"]
                    t_codedtext = t_codedtext.replace("$|$", "")
                    t_codedtext = t_codedtext.replace("\n", "")
                    t_resu_objs = t_resu_sen_obj["resu_objs"]
                    made = 0
                    hypo_ids = []
                    parts = t_codedtext.split(">")
                    for part in parts:
                        t_ids = re.findall("\$(.*)\$", part)
                        if t_ids:
                            for t_id in t_ids:
                                hypo_ids.append(t_id)
                    for t_id in hypo_ids:
                        t_id = t_id.strip(" ")
                        if t_id.lower().replace("(", "").replace(")", "").replace(" ", "").replace("#", "") not in t_sen.lower().replace(" ", ""):
                            made = 1
                            break
                    if made == 0:
                        t_codedtext2 = t_h_sen_obj["codedtext2"]
                        sen_list.append(t_codedtext2)
                        count1 += len(t_resu_objs)
                    else:
                        count2 += len(t_resu_objs)
    


    return sen_list
def process_removeAdd_space_list(coded_sen_list):
    new_coded_sen_list = []
    for sen in coded_sen_list:
        sen = sen.replace(" $<", "$<")
        
        pattern = "\>[^ ]"
        t_res = re.findall(pattern, sen)
        for item in t_res:
            new_item = item[0]+" "+item[1]
            sen = sen.replace(item, new_item)

        sen = re.sub("\$[ ]*", "$", sen)

        pattern = "[^ ]\$[^\<]"
        t_res = re.findall(pattern, sen)
        for item in t_res:
            new_item = item[0]+" "+item[1:]
            sen = sen.replace(item, new_item)

        new_coded_sen_list.append(sen)
    return new_coded_sen_list
def process_remainSuPo_list(coded_sen_list):
    newcoded_sen_list = []
    for sen in coded_sen_list:
        label_parts = re.split("\>", sen)
        new_label_parts = []
        for label_part in label_parts:
            t_hypos = re.findall("(\$.*\$)\<(?:h.*)\, *(su|re|pa)\, *(po|ne|-1)\, *(?:st|we|-1)", label_part)
            
            if t_hypos:
                t_hypo = t_hypos[0]

                t_hypo_0 = t_hypo[0]
                if "S" in t_hypo_0:
                    t_hypo_0 = t_hypo_0.replace("S", "5")

                t_hypo_2 = t_hypo[2]
                if t_hypo_2 == "-1":
                    t_hypo_2 = "nu"
                label_part = re.sub("(\$.*\$)\<(?:h.*)\, *(su|re|pa)\, *(po|ne|-1)\, *(?:st|we|-1)", t_hypo[1]+t_hypo_2+t_hypo_0, label_part)
            new_label_parts.append(label_part)
        new_sen = "".join(new_label_parts)

        new_sen = new_sen.replace("( ", "")
        new_sen = new_sen.replace(" )", "")
        new_sen = re.sub(" +", " ", new_sen)
        new_sen = new_sen.replace("\n", "")
        newcoded_sen_list.append(new_sen)
    return newcoded_sen_list
def build_token_labels_list_su_po(coded_sen_list):
    t_label_dict = {}
    token_labels_list = []
    min_len = 100
    count = -1
    for coded_sen in coded_sen_list:
        count += 1
        words = coded_sen.split(" ")
        new_words = []
        state = "out"
        role = ""
        good_sen = 1
        for i in range(len(words)):
            
            word = words[i].replace("\n", "")

            if ("$" in word) and (state == "out"):
                role = word.split("$")[0]
                word = "$".join(word.split("$")[1:])
                t_label = "B"+"-"+role.upper()
                state = "in"
                if re.search("\$$", word):
                    state = "out"
                    role = ""
            elif ("$" in word) and (state == "in"):
                t_label = "I"+"-"+role.upper()
                state = "out"
                role = ""
            elif ("$" not in word) and (state == "out"):
                t_label = "O"
            elif ("$" not in word) and (state == "in"):
                t_label = "I"+"-"+role.upper()
            word = word.replace("$", "")
            if word.strip(" ") == "":
                continue

            t_label = t_label.replace("(", "")
            if (len(t_label) != 6) and (t_label != "O"):
                good_sen = 0
                print(count, coded_sen)
                print(i, words[i].replace("\n", ""))
                print("!"+role)
                print("?"+t_label)
                print()

            if t_label in t_label_dict:
                t_label_dict[t_label] += 1
            else:
                t_label_dict[t_label] = 1
            new_words.append([word, t_label])
        if len(new_words) < min_len:
            min_len = len(new_words)
        if good_sen == 1:
            token_labels_list.append(new_words)
    print(t_label_dict)
    return token_labels_list
def shorten(token_labels_list):
    new_token_labels_list = []
    for sen_list in token_labels_list:
        new_sen_list = []
        for item in sen_list:
            t_list = []
            t_list.append(item[0])
            t_list.append(item[1][:4])

            new_sen_list.append(t_list)
        new_token_labels_list.append(new_sen_list)
    return new_token_labels_list
def shorten2(token_labels_list):
    new_token_labels_list = []
    for sen_list in token_labels_list:
        new_sen_list = []
        for item in sen_list:
            t_list = []
            t_list.append(item[0])             
            t_list.append(item[1][:2] + item[1][4:6])

            new_sen_list.append(t_list)
        new_token_labels_list.append(new_sen_list)
    return new_token_labels_list
def testREaccuracy(coded_sen_list, token_labels_list):
    sen_dict = {}
    for sen_seq in range(len(token_labels_list)):
        sen_dict[sen_seq] = []
    for sen_seq, sen in enumerate(token_labels_list):
        t_hid = ""
        hid_in = 0
        hid_resu = ""
        resu_objs = []
        for item in sen:
            if item != "":
                t_label = item[1]
                t_word = item[0]
            if (item == "") or ("O" == t_label) or ("B-" in t_label) or ("X" == t_label):
                if hid_in == 1:
                    t_resu_obj = {}
                    t_hid = t_hid.replace("la", "1a")
                    t_hid = t_hid.replace("HS", "H5")
                    t_hid = re.findall("(\d+[A-Za-z]*)(?!\d)", t_hid)

                    t_resu_obj["hid"] = t_hid
                    t_resu_obj["resu"] = hid_resu
                    resu_objs.append(t_resu_obj)

                    hid_in = 0
                    t_hid = ""
                    hid_resu = ""
            if "B-" in t_label:
                hid_in = 1
                hid_resu = t_label.split("-")[1].rstrip("\n").lower()
            if hid_in == 1:
                t_hid += t_word + " "

        for resu_obj in resu_objs:
            sen_dict[sen_seq].append(resu_obj)
    count = 0
    accuracy = 0
    support_pat = "support|confirm|as .. predicted|consistent|significant|in line with|validate"
    reject_pat = "not support|except|not confirm|not consistent|not significant|not in line with|not validate|not hold|reject"
    partial_pat = "partial|part"

    for sen_seq in sen_dict:
        t_sen = coded_sen_list[sen_seq]
        for resu_obj in sen_dict[sen_seq]:
            if len(resu_obj["hid"]) == 0:
                continue
            t_hid = resu_obj["hid"][0]
            count += 1
            
            t_sen = t_sen.replace("la", "1a")
            if t_hid in t_sen:
                if re.search(reject_pat, t_sen, flags=re.IGNORECASE):
                    t_resu = "re"
                    if t_resu == resu_obj["resu"][:2]:
                        accuracy += 1
                elif re.search(support_pat, t_sen, flags=re.IGNORECASE):
                    t_resu = "su"
                    if re.search(partial_pat, t_sen):
                        t_resu = "pa"
                    if t_resu == resu_obj["resu"][:2]:
                        accuracy += 1
            else:
                print(t_hid,t_sen)

    print(accuracy/count)