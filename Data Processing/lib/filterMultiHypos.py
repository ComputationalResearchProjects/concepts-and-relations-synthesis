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
def build_hypo_sen_list(hypo_sen_pred_dict, label_list):
    hypo_sen_list = []
    pdf_seq_list = []
    for i in range(len(label_list)):
        t_sen = hypo_sen_pred_dict["sen"][i]
        t_pdf_seq = hypo_sen_pred_dict["pdf_seq"][i]
        t_label = label_list[i]
        
        if t_label == 1:
            hypo_sen_list.append(t_sen)
            pdf_seq_list.append(t_pdf_seq)
    return [hypo_sen_list, pdf_seq_list]
def build_year_list(seq_list, df):
    year_list = []
    for seq_all in seq_list:
        t_year = df["PY"][seq_all]
        try:
            t_year = int(t_year)
        except:
            t_year = -1
        year_list.append(t_year)
    return year_list
def build_hypo_sen_single_list(hypo_sen_list, pdf_seq_list):
    hypo_sen_single_list = []
    single_pdf_seq_list = []
    hid_list = []
    pat_g1 = "Hypothesis *\d+[a-zA-Z]*(?!:\d)|hypothesis *\d+[a-zA-Z]*(?!:\d)"
    pat_g2 = "|(?:^|[^a-zA-Z])H *\d+[a-zA-Z]*(?!:\d)|(?:^|[^a-zA-Z])h *\d+[a-zA-Z]*(?!:\d)"
    pat_g3 = "|(?:^|[^a-zA-Z])H[a-zA-Z]:|(?:^|[^a-zA-Z])h[a-zA-Z]:"
    pat_g4 = "|(?:^|[^a-zA-Z])H...:|(?:^|[^a-zA-Z])H..:|(?:^|[^a-zA-Z])H.:|(?:^|[^a-zA-Z])H:"
    # pat_g5 = "|(?:^|[^a-zA-Z])H...,|(?:^|[^a-zA-Z])H..,|(?:^|[^a-zA-Z])H.,"
    pat_g6 = "|(?:^|[^a-zA-Z])\(H...\)|(?:^|[^a-zA-Z])\(H..\)|(?:^|[^a-zA-Z])\(H.\)"
    # pat_g7 = "|(?:^|[^a-zA-Z])H...\_|(?:^|[^a-zA-Z])H..\_|(?:^|[^a-zA-Z])H.\_"
    # pat_g8 = "|(?:^|[^a-zA-Z])H.. |(?:^|[^a-zA-Z])H. "
    h_pattern = pat_g1 + pat_g2 + pat_g3 + pat_g4 + pat_g6 

    t_list = []
    for sen_seq, sen in enumerate(hypo_sen_list):
        t_pdf_seq = pdf_seq_list[sen_seq]
        if ("(a)" in sen) and ("(b)" in sen):
            continue
        
        sen = re.sub("(H|h)la", "(H|h)1a", sen)
        sen = re.sub("(H|h)Z", "(H|h)5", sen)

        pats = re.findall(h_pattern, sen)
        
        if (len(pats) == 1):
            t_pat = pats[0]
            t_hid = ""
            t_arr = re.findall("(\d+[a-zA-Z]*)(?!:\d)", t_pat)#h1, h11, h1a
            if t_arr:
                t_hid = t_arr[0]
            hid_list.append(t_hid)
            hypo_sen_single_list.append(sen)
            single_pdf_seq_list.append(t_pdf_seq)
        else:
            t_hid_dict = {}
            t_hid = ""
            for pat in pats:
                t_arr = re.findall("(\d+[a-zA-Z]*)(?!:\d)", pat)
                if t_arr:
                    t_hid = t_arr[0]
                    t_hid_dict[t_hid] = 0
            if len(t_hid_dict.keys()) == 1:# 补充hypothesis 1 (H1)这种单个假设的情况
                hid_list.append(t_hid)
                hypo_sen_single_list.append(sen)
                single_pdf_seq_list.append(t_pdf_seq)
            else:
                t_list.append(sen)
    return [hypo_sen_single_list, single_pdf_seq_list, hid_list, t_list]