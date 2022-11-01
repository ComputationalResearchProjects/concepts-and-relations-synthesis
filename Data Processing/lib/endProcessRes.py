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
def processRes(total_sen_list, pdf_seq_list, pos_sen_list):
    pdf_dict = {}
    for sen_seq, sen in enumerate(total_sen_list):
        t_pdf_seq = pdf_seq_list[sen_seq]
        if t_pdf_seq not in pdf_dict:
            pdf_dict[t_pdf_seq] = []
        # pdf_dict[t_pdf_seq].append(t_hypo_obj)

        t_hid = ""
        hid_in = 0
        hid_resu = ""
        resu_objs = []
        for item in sen:
            if item != "":
                t_label = item.split(" ")[1]
                t_word = item.split(" ")[0]
            if (item == "") or ("O" == t_label) or ("B-" in t_label) or ("X" == t_label):#句子结束或者变量结束
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
            if "B-" in t_label:#变量开始
                hid_in = 1
                hid_resu = t_label.split("-")[1].rstrip("\n").lower()
            if hid_in == 1:#在变量中
                t_hid += t_word + " "

        resu_objs_pos = []
        pos_sen = pos_sen_list[sen_seq]
        for item in pos_sen:
            if item != "":
                t_label = item.split(" ")[1]
                t_word = item.split(" ")[0]
            if (item == "") or ("O" == t_label) or ("B-" in t_label) or ("X" == t_label):#句子结束或者变量结束
                if hid_in == 1:
                    t_resu_obj = {}
                    t_hid = t_hid.replace("la", "1a")
                    t_hid = t_hid.replace("HS", "H5")
                    t_hid = re.findall("(\d+[A-Za-z]*)(?!\d)", t_hid)

                    t_resu_obj["hid"] = t_hid
                    t_resu_obj["resu"] = hid_resu
                    resu_objs_pos.append(t_resu_obj)

                    hid_in = 0
                    t_hid = ""
                    hid_resu = ""
            if "B-" in t_label:#变量开始
                hid_in = 1
                hid_resu = t_label.split("-")[1].rstrip("\n").lower()
            if hid_in == 1:#在变量中
                t_hid += t_word + " "

        for resu_obj in resu_objs:
            t_pos = "-1"
            for resu_obj_pos in resu_objs_pos:
                if resu_obj_pos["hid"] == resu_obj["hid"]:
                    t_pos = resu_obj_pos["resu"]
            resu_obj["pos"] = t_pos
            pdf_dict[t_pdf_seq].append(resu_obj)

    return pdf_dict    
def build_res_sen(resu_sen_list, total_sen_list, pdf_seq_list):
    t_dict = {}
    for seq in pdf_seq_list:
        t_dict[seq] = {"initial": [], "predict": []}
    for i, seq in enumerate(pdf_seq_list):
        t_dict[seq]["initial"].append(resu_sen_list[i])
        t_dict[seq]["predict"].append(total_sen_list[i])
    return t_dict