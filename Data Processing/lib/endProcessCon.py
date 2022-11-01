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
def processConBack2(var_list, label_pred_list, sen_vardict_list, single_pdf_seq2_list, hypo_hid2_list, hypo_sen_single2_list, back_con_list, back_con2_list):
    role_list = ["iv", "dv", "me", "mo", "cv"]
    spdf_list = []
    back_var_list = []

    var_count = 0
    back_count = 0
    back_count2 = 0
    pdf_dict = {}
    for t_seq, var_dict in enumerate(sen_vardict_list):
        t_pdf_seq = single_pdf_seq2_list[t_seq]
        t_hid = hypo_hid2_list[t_seq]
        
        t_hypo_obj = {}
        t_hypo_obj["hid"] = t_hid

        t_sen = hypo_sen_single2_list[t_seq]
        for role in role_list:
            if var_dict[role] != 0:
                t_hypo_obj[role] = {}
                t_hypo_obj[role]["varia"] = var_list[var_count]
                t_hypo_obj[role]["label"] = label_pred_list[var_count]

                if "use experience" in ".".join(label_pred_list[var_count]):
                    if re.search("perception.other|perception.social influence|emotion" ,".".join(label_pred_list[var_count])):
                        t_hypo_obj[role]["label"] = back_con_list[back_count]
                        back_count += 1


                        if "parasocial relationship" in t_hypo_obj[role]["label"]:
                            t_hypo_obj[role]["label"] = back_con2_list[back_count2]
                            back_count2 += 1
                        elif "personality" in t_hypo_obj[role]["label"]:
                            t_hypo_obj[role]["label"] = back_con2_list[back_count2]
                            back_count2 += 1
                var_count += 1
            else:
                t_hypo_obj[role] = 0

        if t_pdf_seq not in pdf_dict:
            pdf_dict[t_pdf_seq] = []
        pdf_dict[t_pdf_seq].append(t_hypo_obj)
    print(var_count)
    print(back_count)
    print(back_count2)
    return pdf_dict
def processConBack(var_list, label_pred_list, sen_vardict_list, single_pdf_seq2_list, hypo_hid2_list, hypo_sen_single2_list, back_con_list, relia_list):
    role_list = ["iv", "dv", "me", "mo", "cv"]
    spdf_list = []
    back_var_list = []

    relia1_dict = {"sum":0, "num":0}
    relia2_dict = {"sum":0, "num":0}

    var_count = 0
    back_count = 0
    pdf_dict = {}
    for t_seq, var_dict in enumerate(sen_vardict_list):
        t_pdf_seq = single_pdf_seq2_list[t_seq]
        t_hid = hypo_hid2_list[t_seq]
        
        t_hypo_obj = {}
        t_hypo_obj["hid"] = t_hid

        t_sen = hypo_sen_single2_list[t_seq]
        for role in role_list:
            if var_dict[role] != 0:
                t_hypo_obj[role] = {}
                t_hypo_obj[role]["varia"] = var_list[var_count]
                t_hypo_obj[role]["label"] = label_pred_list[var_count]

                if "use experience" in ".".join(label_pred_list[var_count]):
                    if re.search("perception.other|perception.social influence|emotion" ,".".join(label_pred_list[var_count])):
                        t_hypo_obj[role]["label"] = back_con_list[back_count]
                        

                        if "parasocial relationship" in t_hypo_obj[role]["label"]:
                            back_var_list.append(var_list[var_count])

                            relia1_dict["sum"] += relia_list[back_count]
                            relia1_dict["num"] += 1
                        elif "personality" in t_hypo_obj[role]["label"]:
                            back_var_list.append(var_list[var_count])

                            relia1_dict["sum"] += relia_list[back_count]
                            relia1_dict["num"] += 1
                        else:
                            relia2_dict["sum"] += relia_list[back_count]
                            relia2_dict["num"] += 1

                        back_count += 1
                var_count += 1
            else:
                t_hypo_obj[role] = 0

        if t_pdf_seq not in pdf_dict:
            pdf_dict[t_pdf_seq] = []
        pdf_dict[t_pdf_seq].append(t_hypo_obj)
    print(var_count)
    print(back_count)
    print(relia1_dict["sum"]/relia1_dict["num"], relia2_dict["sum"]/relia2_dict["num"])
    return pdf_dict, back_var_list
def processCon(var_list, label_pred_list, sen_vardict_list, single_pdf_seq2_list, hypo_hid2_list, hypo_sen_single2_list, relia_list):
    role_list = ["iv", "dv", "me", "mo", "cv"]
    spdf_list = []
    back_var_list = []
    relia1_dict = {"sum":0, "num":0, "low_num":0}
    relia2_dict = {"sum":0, "num":0, "low_num":0}
    sen_count = 0
    threshold = 0.0325
    low_concepts = []

    var_count = 0
    pdf_dict = {}
    for t_seq, var_dict in enumerate(sen_vardict_list):
        t_pdf_seq = single_pdf_seq2_list[t_seq]
        t_hid = hypo_hid2_list[t_seq]
        
        t_hypo_obj = {}
        t_hypo_obj["hid"] = t_hid

        t_sen = hypo_sen_single2_list[t_seq]

        for role in role_list:
            if var_dict[role] != 0:
                t_hypo_obj[role] = {}
                t_hypo_obj[role]["varia"] = var_list[var_count]
                t_hypo_obj[role]["label"] = label_pred_list[var_count]

                if "use experience" in ".".join(label_pred_list[var_count]):
                    if re.search("perception.other|perception.social influence|emotion" ,".".join(label_pred_list[var_count])):
                        back_var_list.append(var_list[var_count])

                        relia2_dict["sum"] += relia_list[var_count]
                        relia2_dict["num"] += 1
                        if relia_list[var_count] < threshold:
                            relia2_dict["low_num"] += 1
                    else:
                        relia1_dict["sum"] += relia_list[var_count]
                        relia1_dict["num"] += 1
                        if relia_list[var_count] < threshold:
                            relia1_dict["low_num"] += 1
                            low_concepts.append(".".join(label_pred_list[var_count]))
                else:
                    relia1_dict["sum"] += relia_list[var_count]
                    relia1_dict["num"] += 1
                    if relia_list[var_count] < threshold:
                        relia1_dict["low_num"] += 1
                        low_concepts.append(".".join(label_pred_list[var_count]))
                var_count += 1
            else:
                t_hypo_obj[role] = 0

        if t_pdf_seq not in pdf_dict:
            pdf_dict[t_pdf_seq] = []
        pdf_dict[t_pdf_seq].append(t_hypo_obj)
    print(var_count)
    print(sen_count)
    print(relia1_dict["sum"]/relia1_dict["num"], relia2_dict["sum"]/relia2_dict["num"])
    print(relia2_dict["num"])
    print(relia1_dict["low_num"], relia2_dict["low_num"])
    return pdf_dict, back_var_list
def new_processCon(var_list, label_pred_list, sen_vardict_list, single_pdf_seq2_list, hypo_hid2_list, hypo_sen_single2_list, relia_list, pos2_list):
    role_list = ["iv", "dv", "me", "mo", "cv"]
    spdf_list = []
    back_var_list = []
    relia1_dict = {"sum":0, "num":0, "low_num":0}
    relia2_dict = {"sum":0, "num":0, "low_num":0}
    sen_count = 0
    threshold = 0.0325
    low_concepts = []

    t_count = 0

    var_count = 0
    pdf_dict = {}
    for t_seq, var_dict in enumerate(sen_vardict_list):
        t_pdf_seq = single_pdf_seq2_list[t_seq]
        t_hid = hypo_hid2_list[t_seq]
        t_pos2 = pos2_list[t_seq]
        
        t_hypo_obj = {}
        t_hypo_obj["hid"] = t_hid
        t_hypo_obj["pos"] = t_pos2

        t_sen = hypo_sen_single2_list[t_seq]

        for role in role_list:
            if var_dict[role] != 0:

                t_hypo_obj[role] = {}
                t_hypo_obj[role]["varia"] = var_list[var_count]
                t_hypo_obj[role]["label"] = label_pred_list[var_count]

                if relia_list[var_count] < threshold:
                    t_count += 1
                var_count += 1
            else:
                t_hypo_obj[role] = 0

        if t_pdf_seq not in pdf_dict:
            pdf_dict[t_pdf_seq] = []
        pdf_dict[t_pdf_seq].append(t_hypo_obj) 
    print(t_count)
    # print(var_count)
    # print(sen_count)
    # print(relia1_dict["sum"]/relia1_dict["num"], relia2_dict["sum"]/relia2_dict["num"])
    # print(relia2_dict["num"])
    
    return pdf_dict, back_var_list