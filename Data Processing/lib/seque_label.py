import json
import re
def read_json(path):
    t_file = open(path, "r")
    json_data = json.load(t_file)
    t_file.close()
    return json_data
def write_json(json_data, path):
    t_file = open(path, "w")
    json.dump(json_data, t_file)
    t_file.close()
def build_pdf_label_list(pdf_list, valid_sample_list):
    pdf_label_list = []
    for seq in valid_sample_list:
        t_pdf = pdf_list[seq]
        pdf_label_list.append(t_pdf)

    return pdf_label_list
def build_codedSen_conceLabel_list(pdf_label_list):
    coded_sen_list = []
    conce_label_list = []

    item_list = ["l", "r", "me", "mo"]
    for pdf_seq, pdf_obj in enumerate(pdf_label_list):
        t_h_sen_objs = pdf_obj["h_extract_obj"]["h_sen_objs"]
        t_hypo_sen_objs = pdf_obj["h_extract_obj"]["hypo_sen_objs"]
        for t_hypo_sen_obj in t_hypo_sen_objs:
            valid = 0
            if "hypo_objs" in t_hypo_sen_obj:
                if len(t_hypo_sen_obj["hypo_objs"]) == 1:
                    for hypo_obj in t_hypo_sen_obj["hypo_objs"]:
                        if (type(hypo_obj["l"]) == list) and (len(hypo_obj["l"]) == 5):
                            valid = 1
                        t_dict = {}
                        for item in item_list:
                        	if (type(hypo_obj[item]) == list) and (len(hypo_obj[item]) == 5):
                        		t_dict[item] = hypo_obj[item][2]
            if valid == 1:
                t_h_sen_seq = t_hypo_sen_obj["h_sen_seq"]
                t_coded_sen = t_h_sen_objs[t_h_sen_seq]["codedtext"]
                coded_sen_list.append(t_coded_sen)
                conce_label_list.append(t_dict)
    return [coded_sen_list, conce_label_list]
def build_codedSen_conceLabel_all_list(pdf_label_list):
    coded_sen_list = []
    conce_label_list = []

    item_list = ["l", "r", "me", "mo"]
    for pdf_seq, pdf_obj in enumerate(pdf_label_list):
        t_h_sen_objs = pdf_obj["h_extract_obj"]["h_sen_objs"]
        t_hypo_sen_objs = pdf_obj["h_extract_obj"]["hypo_sen_objs"]
        for t_hypo_sen_obj in t_hypo_sen_objs:
            valid = 0
            if "hypo_objs" in t_hypo_sen_obj:
                for hypo_obj in t_hypo_sen_obj["hypo_objs"]:
                    if (type(hypo_obj["l"]) == list) and (len(hypo_obj["l"]) == 5):
                        valid = 1
                    t_dict = {}
                    for item in item_list:
                        if (type(hypo_obj[item]) == list) and (len(hypo_obj[item]) == 5):
                            t_dict[item] = hypo_obj[item][2]
            if valid == 1:
                t_h_sen_seq = t_hypo_sen_obj["h_sen_seq"]
                t_coded_sen = t_h_sen_objs[t_h_sen_seq]["codedtext"]
                coded_sen_list.append(t_coded_sen)
                conce_label_list.append(t_dict)
    return [coded_sen_list, conce_label_list]
def process_noHypo_codedSen_list(coded_sen_list):
    newcoded_sen_list = []
    for sen in coded_sen_list:
        label_parts = re.split("\>", sen)
        new_label_parts = []
        for label_part in label_parts:
            t_hypos = re.findall("\$(.*)\$\<(?:h.*)\, *(?:ca|co)\, *(?:po|ne|-1)\, *(?:st|we|-1)", label_part)

            if t_hypos:
                label_part = re.sub("\$.*\$\<(?:h.*)\, *(?:ca|co)\, *(?:po|ne|-1)\, *(?:st|we|-1)", t_hypos[0], label_part)
            else:
                t_vars = re.findall("(\$.*\$)\<", label_part)
                if t_vars:
                    t_vars[0] = t_vars[0].replace("\\","")
                    label_part = re.sub("\$.*\$\<.*", t_vars[0], label_part)
            new_label_parts.append(label_part)
        new_sen = "".join(new_label_parts)
        new_sen = new_sen.replace("#", "")

        new_sen = new_sen.replace("\n", "")
        newcoded_sen_list.append(new_sen)
    return newcoded_sen_list
def build_token_labels_list(coded_sen_list):
    token_labels_list = []
    min_len = 100
    for coded_sen in coded_sen_list:


        words = coded_sen.split(" ")
        new_words = []
        state = "out"

        for i in range(len(words)):
            
            word = words[i].replace("\n", "")

            if ("$" in word) and (state == "out"):
                t_label = "B"
                state = "in"
            elif ("$" in word) and (state == "in"):
                t_label = "I"
                state = "out"
            elif ("$" not in word) and (state == "out"):
                t_label = "O"
            elif ("$" not in word) and (state == "in"):
                t_label = "I"
            word = word.replace("$", "")
            if word.strip(" ") == "":
                continue
            new_words.append([word, t_label])
        if len(new_words) < min_len:
            min_len = len(new_words)
        token_labels_list.append(new_words)
    return token_labels_list
def process_removeAdd_space_list(coded_sen_list):
    new_coded_sen_list = []
    for sen in coded_sen_list:
        #" $<"=>"$<"
        sen = sen.replace(" $<", "$<")
        
        #">#"=>"> #"
        pattern = "\>[^ ]"
        t_res = re.findall(pattern, sen)
        for item in t_res:
            new_item = item[0]+" "+item[1]
            sen = sen.replace(item, new_item)

        #"$ I like" => "$I like"
        sen = re.sub("\$[ ]*", "$", sen)

        # "asdf$I like" => "asdf $I like"
        pattern = "[^ ]\$[^\<]"
        t_res = re.findall(pattern, sen)
        for item in t_res:
            new_item = item[0]+" "+item[1:]
            sen = sen.replace(item, new_item)

        new_coded_sen_list.append(sen)
    return new_coded_sen_list
def process_remainRole_list(coded_sen_list):
    newcoded_sen_list = []
    for sen in coded_sen_list:
        label_parts = re.split("\>", sen)
        new_label_parts = []
        for label_part in label_parts:
            t_hypos = re.findall("\$(.*)\$\<(?:h.*)\, *(?:ca|co)\, *(?:po|ne|-1)\, *(?:st|we|-1)", label_part)

            if t_hypos:
                label_part = re.sub("\$.*\$\<(?:h.*)\, *(?:ca|co)\, *(?:po|ne|-1)\, *(?:st|we|-1)", t_hypos[0], label_part)
            else:
                t_vars = re.findall("(\$.*\$)\<", label_part)
                t_roles = re.findall("\$.*\$\<(..)", label_part)
                if t_vars:
                    t_vars[0] = t_vars[0].replace("\\","")
                    label_part = re.sub("\$.*\$\<.*", t_roles[0]+t_vars[0], label_part)
            new_label_parts.append(label_part)
        new_sen = "".join(new_label_parts)
        new_sen = new_sen.replace("(###", "")
        new_sen = new_sen.replace("###)", "")
        new_sen = re.sub(" +", " ", new_sen)

        new_sen = new_sen.replace("\n", "")
        newcoded_sen_list.append(new_sen)
    return newcoded_sen_list
def process_remainPos_list(coded_sen_list):
    newcoded_sen_list = []
    for sen in coded_sen_list:
        label_parts = re.split("\>", sen)
        new_label_parts = []
        for label_part in label_parts:
            t_hypos = re.findall("(\$.*\$)\<(h.*)\, *(ca|co)\, *(po|ne|-1)\, *(st|we|-1)", label_part)

            if t_hypos:
                t_hypos = t_hypos[0]
                t_label = t_hypos[3]
                if t_hypos[3] == "-1":
                    t_label = "nu"
                label_part = re.sub("\$.*\$\<(?:h.*)\, *(?:ca|co)\, *(?:po|ne|-1)\, *(?:st|we|-1)", t_label+t_hypos[0], label_part)
            else:
                t_vars = re.findall("\$(.*)\$\<", label_part)
                t_roles = re.findall("\$.*\$\<(..)", label_part)
                if t_vars:
                    t_vars[0] = t_vars[0].replace("\\","")
                    label_part = re.sub("\$.*\$\<.*", t_vars[0], label_part)
            new_label_parts.append(label_part)
        new_sen = "".join(new_label_parts)
        new_sen = new_sen.replace("(###", "")
        new_sen = new_sen.replace("###)", "")
        new_sen = re.sub(" +", " ", new_sen)

        new_sen = new_sen.replace("\n", "")
        newcoded_sen_list.append(new_sen)
    return newcoded_sen_list
def build_token_labels_list_ivdvmemo(coded_sen_list):
    token_labels_list = []
    min_len = 100
    count = -1
    for coded_sen in coded_sen_list:
        count += 1
        words = coded_sen.split(" ")
        new_words = []
        state = "out"
        role = ""
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

            if (len(t_label) != 4) and (t_label != "O"):
                print(count, coded_sen)
                print(words[i].replace("\n", ""))
                print("!"+role)
                print("?"+t_label)
                print()
            new_words.append([word, t_label])
        if len(new_words) < min_len:
            min_len = len(new_words)
        token_labels_list.append(new_words)
    return token_labels_list
def build_token_labels_pred_list(hypo_sen_single_list):
    token_labels_pred_list = []
    for sen in hypo_sen_single_list:
        words = sen.split(" ")
        new_words = []
        for word in words:
            word = word.strip(" ")
            word = word.strip("\n")
            if word == "":
                continue
            new_words.append([word, "O"])
        token_labels_pred_list.append(new_words)
    return token_labels_pred_list