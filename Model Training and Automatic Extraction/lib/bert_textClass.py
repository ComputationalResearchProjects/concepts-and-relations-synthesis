
import random
import json
import pandas as pd
random.seed(2020)
import jsonlines
import networkx as nx
def geneTrainEvaTest(hypo_sen_train_dict, hypo_sen_pred_dict):
	sen_train_list = []
	t_len = len(hypo_sen_train_dict["sen"])
	for i in range(t_len):
		t_sen = hypo_sen_train_dict["sen"][i]
		t_type = hypo_sen_train_dict["type"][i]
		t_obj = {}
		t_obj["sen"] = t_sen
		t_obj["type"] = t_type
		sen_train_list.append(t_obj)

	train_list = []
	eval_list = []
	seq_list = range(len(sen_train_list))
	train_seq_list = random.sample(seq_list, int(0.8*len(sen_train_list)))
	eval_totalSeq_list = []

	for seq in seq_list:
		t_obj = sen_train_list[seq]
		if seq in train_seq_list:
			train_list.append(t_obj)
		else:
			eval_totalSeq_list.append(seq)
			eval_list.append(t_obj)

	sen_pred_list = []
	t_len = len(hypo_sen_pred_dict["sen"])
	for i in range(t_len):
		t_sen = hypo_sen_pred_dict["sen"][i]
		t_type = hypo_sen_pred_dict["type"][i]
		t_obj = {}
		t_obj["sen"] = t_sen
		t_obj["type"] = t_type
		sen_pred_list.append(t_obj)

	return [train_list, eval_list, sen_pred_list]
def split(hypo_sen_dict):
	tokenLabels_list = []
	t_len = len(hypo_sen_dict["sen"])
	for i in range(t_len):
		t_sen = hypo_sen_dict["sen"][i]
		t_type = hypo_sen_dict["type"][i]
		t_obj = {}
		t_obj["sen"] = t_sen
		t_obj["type"] = t_type
		tokenLabels_list.append(t_obj)
		
	train_list = []
	eval_list = []

	seq_list = range(len(tokenLabels_list))
	train_seq_list = random.sample(seq_list, int(0.8*len(tokenLabels_list)))
	eval_totalSeq_list = []

	for seq in seq_list:
		t_tokenLabels = tokenLabels_list[seq]
		if seq in train_seq_list:
			train_list.append(t_tokenLabels)
		else:
			eval_totalSeq_list.append(seq)
			eval_list.append(t_tokenLabels)


	test_list = []
	dev_list = []

	eval_seq_list = range(len(eval_list))
	test_seq_list = random.sample(eval_seq_list, int(0.5*len(eval_list)))
	test_totalSeq_list = []

	for seq in eval_seq_list:
		t_tokenLabels = eval_list[seq]
		t_totalSeq = eval_totalSeq_list[seq]

		if seq in test_seq_list:
			test_list.append(t_tokenLabels)
			test_totalSeq_list.append(t_totalSeq)
		else:
			dev_list.append(t_tokenLabels)

	return [train_list, test_list, dev_list, test_totalSeq_list]
def read_json(path):
    t_file = open(path, "r", encoding = "utf-8")
    json_data = json.load(t_file)
    t_file.close()
    return json_data
def write_json(json_data, path):
    t_file = open(path, "w", encoding = "utf-8")
    json.dump(json_data, t_file)
    t_file.close()
def write_files(dataset, folder):
	name_list = ["train", "dev", "test"]
	for i, t_list in enumerate(dataset[:3]):
		data_list = []
		t_sen_list = []
		t_type_list = []
		for t_obj in t_list:
			data_list.append({"sentence": t_obj["sen"]+" . ", "label": t_obj["type"]})

		if name_list[i] == "test":
			with jsonlines.open(folder + name_list[i] + '.json', mode='w') as writer:
				for item in data_list:
					writer.write(item)
			
		else:
			with jsonlines.open(folder + name_list[i] + '.json', mode='w') as writer:
				for item in data_list:
					writer.write(item)