import json
import re
import pandas as pd
import random
def read_json(path):
    t_file = open(path, "r")
    json_data = json.load(t_file)
    t_file.close()
    return json_data
def write_json(json_data, path):
    t_file = open(path, "w")
    json.dump(json_data, t_file)
    t_file.close()
def build_sen_vardict_list(total_sen_list, single_pdf_seq_list, hypo_hid_list, hypo_sen_single_list, pos_list):
    sen_vardict_list = []
    single_pdf_seq2_list = []
    hypo_hid2_list = []
    hypo_sen_single2_list = []
    pos2_list = []

    count_noiv = 0
    var_list = []
    count_list = []
    # lab_list = []
    for sen_seq, sen in enumerate(total_sen_list):
        t_var = ""
        var_in = 0
        var_role = ""
    #     t_conlabel_dict = conceLabel_list[sen_seq]
        t_vardict = {"iv": 0, "dv": 0, "me": 0, "mo": 0, "cv": 0}
        t_pdf_seq = single_pdf_seq_list[sen_seq]
        t_hid = hypo_hid_list[sen_seq]
        ttt_sen = hypo_sen_single_list[sen_seq]
        t_pos = pos_list[sen_seq]

        t_var_list_len = len(var_list)
        for item in sen:
            if item != "":
                t_label = item.split(" ")[1]
                t_word = item.split(" ")[0]
            if (item == "") or ("O" == t_label) or ("B-" in t_label):#句子结束或者变量结束
                if var_in == 1:
                    var_list.append(t_var)
                    t_vardict[var_role] = t_var
                    var_in = 0
                    t_var = ""
                    var_role = ""
            if "B-" in t_label:#变量开始
                var_in = 1
                var_role = t_label.split("-")[1].rstrip("\n").lower()
            if var_in == 1:#在变量中
                t_var += t_word + " "
        
        count_list.append(len(var_list) - t_var_list_len)
        
        if ((t_vardict["iv"] == 0) or (t_vardict["dv"] == 0)) or (len(var_list) - t_var_list_len >= 5):
            # if random.randint(1, 50) == 1:
            #     print(sen)
            count_noiv += 1
        else:
            sen_vardict_list.append(t_vardict)
            single_pdf_seq2_list.append(t_pdf_seq)
            hypo_hid2_list.append(t_hid)
            hypo_sen_single2_list.append(ttt_sen)
            pos2_list.append(t_pos)
    return [sen_vardict_list, single_pdf_seq2_list, hypo_hid2_list, count_list, hypo_sen_single2_list, pos2_list]