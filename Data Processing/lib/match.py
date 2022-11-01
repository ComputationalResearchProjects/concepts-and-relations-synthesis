import json
import re
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
def judge_resu(hypo_hid, resu_hid):
    if len(resu_hid) == 1:
        if hypo_hid == resu_hid[0]:
            return True
        else:
            if not re.search("[A-Za-z]",resu_hid[0]): 
                hypo_num = int(re.findall("(\d+)(?!\d)", hypo_hid)[0])
                resu_num = int(re.findall("(\d+)(?!\d)", resu_hid[0])[0])
                if hypo_num == resu_num:
                    return True
            return False
    if len(resu_hid) == 2:
        start_num = resu_hid[0]
        start_num = int(re.findall("(\d+)(?!\d)", start_num)[0])
        
        end_num = resu_hid[0]
        end_num = int(re.findall("(\d+)(?!\d)", end_num)[0])
        
        hypo_num = int(re.findall("(\d+)(?!\d)", hypo_hid)[0])
        
        if (hypo_num >= start_num) and (hypo_num <= end_num):
            return True
        else:
            return False
def combine_resu2hypo(hypo_spdf_dict, resu_spdf_dict, res_sen_dict, all_sen_dict):
    pdf_num = 0
    hid_num = 0
    pdf_overlap = 0
    hid_overlap = 0
    res_num = 0
    hid_in_sen = 0
    hid_in_allsen = 0
    support_pat = "support|confirm|as .. predicted|consistent|significant|in line with|validate"
    reject_pat = "not support|except|not confirm|not consistent|not significant|not in line with|not validate|not hold|reject"
    partial_pat = "partial|part"
    hypo_pat = "(hypothesis *|h|hypotheses *)"

    for pdf_seq in hypo_spdf_dict:
        t_hid_num = 0
        t_hid_overlap = 0

        t_hid_in_allsen = 0
        t_hid_in_sen = 0
        pdf_num += 1
        t_hypos = hypo_spdf_dict[pdf_seq]
        t_hid_hypo_dict = {}
        for item in t_hypos:
            if item["hid"] == "":
                continue
            t_hid_hypo_dict[item["hid"]] = item
        hid_num += len(t_hid_hypo_dict.keys())
        t_hid_num = len(t_hid_hypo_dict.keys())

        if pdf_seq in resu_spdf_dict:
            pdf_overlap += 1
            t_resus = resu_spdf_dict[pdf_seq]

            t_hid_dict = {}
            for item in t_resus:
                try:
                    t_hid_dict[item["hid"][0]] = 0
                except:
                    a = 1
            res_num += len(t_hid_dict.keys())

            for t_hid in t_hid_hypo_dict:
                t_hypo = t_hid_hypo_dict[t_hid]
                t_match = 0
                t_hypo_hid = t_hypo["hid"]
                if t_hypo_hid == "":
                    continue
                
                for t_resu in t_resus:
                    t_resu_hid = t_resu["hid"]
                    t_resu_resu = t_resu["resu"]
                    t_resu_pos = t_resu["pos"]
                    if judge_resu(t_hypo_hid, t_resu_hid):
                        hid_overlap += 1
                        t_hid_overlap += 1
                        t_hypo["resu"] = t_resu_resu
                        t_hypo["resu_pos"] = t_resu_pos
                        t_match = 1
                        break
                t_hid_in_sen_match = 0
                t_hid_in_allsen_match = 0
                for sen in res_sen_dict[pdf_seq]["initial"]:
                    if t_hypo_hid in sen:
                        if not re.search(hypo_pat+t_hypo_hid, sen, flags=re.IGNORECASE):
                            continue
                        if re.search(reject_pat, sen, flags=re.IGNORECASE):
                            hid_in_sen += 1
                            t_hid_in_sen += 1
                            t_hid_in_sen_match = 1
                            break
                        elif re.search(support_pat, sen, flags=re.IGNORECASE):
                            hid_in_sen += 1
                            t_hid_in_sen += 1
                            t_hid_in_sen_match = 1
                            if re.search(partial_pat, sen):
                                a = 1
                            break
                for sen in all_sen_dict[pdf_seq]:
                    sen = sen.replace("HS", "H5").replace("Hla", "H1a")
                    if t_hypo_hid in sen:
                        if not re.search(hypo_pat+t_hypo_hid, sen, flags=re.IGNORECASE):
                            continue
                        if re.search(reject_pat, sen, flags=re.IGNORECASE):
                            hid_in_allsen += 1
                            t_hid_in_allsen += 1
                            t_hid_in_allsen_match = 1
                            break
                        elif re.search(support_pat, sen, flags=re.IGNORECASE):
                            hid_in_allsen += 1
                            t_hid_in_allsen += 1
                            t_hid_in_allsen_match = 1
                            if re.search(partial_pat, sen):
                                a = 1
                            break

def destroy_label(conce_list, sample_con_list):

    t_conce_list_str = ".".join(conce_list).strip(".")

    t_con_last = sample_con_list[-1].split(".")
    while len(t_con_last) < 5:
        t_con_last.extend([""])
    if t_conce_list_str in sample_con_list[:23]:
        return t_con_last
    return conce_list
def build_pdf_whole_list(hypo_spdf_dict, pdf_list, valid_sample_list):
    pdf_desert_count = 0
    count = 0
    pdf_whole_list = []
    item_list = ["l", "r", "me", "mo"]

    pdf_1_count = 0
    sen_1_count = 0
    for t_seq in valid_sample_list:
        t_hypo_id_pos = {}
        t_hypo_id_respos = {}

        pdf_list[t_seq]["seq2"] = t_seq
        hypo_sen_objs = pdf_list[t_seq]["h_extract_obj"]["hypo_sen_objs"]
        for hypo_sen_obj in hypo_sen_objs:
            if 'hypo_objs' in hypo_sen_obj:
                if len(hypo_sen_obj["hypo_objs"]) == 1:
                    hypo_objs = hypo_sen_obj["hypo_objs"]
                    for hypo_obj in hypo_objs:
                        t_hid = hypo_obj['attr'][0]
                        t_pos = hypo_obj['attr'][2]
                        t_hypo_id_pos[t_hid] = t_pos
                        if t_hid in pdf_list[t_seq]['hypo_id_resu']:
                            t_hypo_id_respos[t_hid] = pdf_list[t_seq]['hypo_id_resu'][t_hid][2]

                        tt_list = hypo_obj["l"]
                        if (type(tt_list) == list) and (len(tt_list) == 5):
                            sen_1_count += 1

                        for item in item_list:
                            var_list = hypo_obj[item]
                            if (type(var_list) == list) and (len(var_list) == 5):
                                t_conce_list = var_list[2]
                                t_varia = var_list[1]

                                
                                # var_list[2] = destroy_label(var_list[2], sample_con_list)

        pdf_list[t_seq]["hypo_id_pos"] =  t_hypo_id_pos
        pdf_list[t_seq]["hypo_id_respos"] =  t_hypo_id_respos
        pdf_whole_list.append(pdf_list[t_seq])
        pdf_1_count += 1

    pdf_2_count = 0
    for t_seq in hypo_spdf_dict:
        t_obj_list = hypo_spdf_dict[t_seq]
        t_pdf_obj = pdf_list[int(t_seq)]

        #hypos
        t_hypo_sen_objs = t_pdf_obj["h_extract_obj"]["hypo_sen_objs"]
        for t_obj in t_obj_list:
            iv = t_obj["iv"]
            dv = t_obj["dv"]

            me = t_obj["me"]
            mo = t_obj["mo"]
            t_hypo_obj = {}
            t_rela = "ca"

            if (iv == 0) or (dv == 0):
                count += 1
                continue

            while len(iv["label"]) < 5:
                iv["label"].append("")
            while len(dv["label"]) < 5:
                dv["label"].append("")
            # iv["label"] = destroy_label(iv["label"], sample_con_list)
            # dv["label"] = destroy_label(dv["label"], sample_con_list)
            
            t_hypo_obj["attr"] = ["h"+t_obj["hid"], t_rela, -1, -1]
            t_hypo_obj["l"] = ["iv", iv["varia"], iv["label"], "", ""]
            t_hypo_obj["r"] = ["dv", dv["varia"], dv["label"], "", ""]

            if t_obj["me"] != 0:
                while len(me["label"]) < 5:
                    me["label"].append("")
                # me["label"] = destroy_label(me["label"], sample_con_list)
                
                t_hypo_obj["me"] = ["me", me["varia"], me["label"], "", ""]
            else:
                t_hypo_obj["me"] = ""


            if t_obj["mo"] != 0:
                while len(mo["label"]) < 5:
                    mo["label"].append("")
                # mo["label"] = destroy_label(mo["label"], sample_con_list)

                t_hypo_obj["mo"] = ["mo", mo["varia"], mo["label"], "", ""]
            else:
                t_hypo_obj["mo"] = ""

            t_hypo_sen_obj = {}
            t_hypo_sen_obj["hypo_objs"] = [t_hypo_obj]
            t_hypo_sen_objs.append(t_hypo_sen_obj)

        if len(t_hypo_sen_objs) == 0:
            pdf_desert_count += 1
            continue

        #resu
        t_hypo_id_pos = {}
        t_hypo_id_respos = {}

        t_hypo_id_resu = {}
        for t_obj in t_obj_list:
            t_hid = "h"+t_obj["hid"]

            t_hypo_id_pos[t_hid] = t_obj["pos"].lower()
            if "resu_pos" in t_obj:
                t_hypo_id_respos[t_hid] = t_obj["resu_pos"].lower()

            if "resu" not in t_obj:
                continue
            t_resu = t_obj['resu']
            t_resu_su = t_resu[:2]
            t_resu_po = t_resu[2:]
            if t_resu_po == "nu":
                t_resu_po = "-1"

            t_hypo_id_resu[t_hid] = [t_hid, t_resu_su, t_resu_po, "-1"]
        t_pdf_obj["hypo_id_resu"] = t_hypo_id_resu

        t_pdf_obj["hypo_id_pos"] = t_hypo_id_pos
        t_pdf_obj["hypo_id_respos"] = t_hypo_id_respos

        t_pdf_obj["seq2"] = t_seq

        pdf_2_count += 1
        pdf_whole_list.append(t_pdf_obj)

    return pdf_whole_list