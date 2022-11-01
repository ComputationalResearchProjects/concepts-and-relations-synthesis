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
def nertxt2varLabel2(conceLabel_list, codedSen_role_list, token_labels_list):

    var_list = []
    lab_list = []
    t_sen_list = []
    remove_label = "who.educator.characteristics"
    
    for sen_seq, sen in enumerate(token_labels_list):
        sen.append(["", ""])
        t_var = ""
        var_in = 0
        var_role = ""
        t_conlabel_dict = conceLabel_list[sen_seq]
        coded_sen = codedSen_role_list[sen_seq]
        for item in sen:
            t_label = item[1]
            t_word = item[0]

            if (t_label == "") or (t_label == "O") or ("B-" in t_label):
                if var_in == 1:
                    if var_role == "iv":
                        if remove_label not in ".".join(t_conlabel_dict["l"]):
                            lab_list.append(t_conlabel_dict["l"])
                            var_list.append(t_var + " has effects on")
                    elif var_role == "dv":
                        if remove_label not in ".".join(t_conlabel_dict["r"]):
                            lab_list.append(t_conlabel_dict["r"])
                            var_list.append(t_var + " is affected by")
                    elif var_role == "me":
                        if remove_label not in ".".join(t_conlabel_dict["me"]):
                            lab_list.append(t_conlabel_dict["me"])
                            var_list.append(t_var + " mediates")
                    elif var_role == "mo":
                        if remove_label not in ".".join(t_conlabel_dict["mo"]):
                            lab_list.append(t_conlabel_dict["mo"])
                            var_list.append(t_var + " moderates")
                    else:
                        #cv
                        if remove_label not in ".".join(t_conlabel_dict["l"]):
                            lab_list.append(t_conlabel_dict["l"])
                            var_list.append(t_var + " is correlated with")
                    t_sen_list.append(coded_sen)
                    var_in = 0
                    t_var = ""
                    var_role = ""
            if "B-" in t_label:
                var_in = 1
                var_role = t_label.split("-")[1].rstrip("\n").lower()
            if var_in == 1:
                t_var += t_word + " "
    t_dict = {}
    t_dict["varia"] = var_list
    t_dict["label"] = lab_list

    return t_dict, t_sen_list


    # print(train_var_list[:10], train_varRole_list[:10])
    # print()
    # print(label_split_data["train"][:10], len(label_split_data["test"]))