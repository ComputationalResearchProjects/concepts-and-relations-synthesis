
import random
import json
random.seed(2020)

def split_conce(tokenLabels_list, codedSen_conceLabel_list):
	train_list = []
	train_label_list = []
	eval_list = []

	seq_list = range(len(tokenLabels_list))
	train_seq_list = random.sample(seq_list, int(0.8*len(tokenLabels_list)))
	eval_totalSeq_list = []

	for seq in seq_list:
		t_tokenLabels = tokenLabels_list[seq]
		if seq in train_seq_list:
			train_list.append(t_tokenLabels)
			train_label_list.append(codedSen_conceLabel_list[seq])
		else:
			eval_totalSeq_list.append(seq)
			eval_list.append(t_tokenLabels)

	test_list = []
	dev_list = []
	test_label_list = []
	dev_label_list = []

	eval_seq_list = range(len(eval_list))
	test_seq_list = random.sample(eval_seq_list, int(0.5*len(eval_list)))
	test_totalSeq_list = []

	for seq in eval_seq_list:
		t_tokenLabels = eval_list[seq]
		t_totalSeq = eval_totalSeq_list[seq]

		if seq in test_seq_list:
			test_list.append(t_tokenLabels)
			test_label_list.append(codedSen_conceLabel_list[t_totalSeq])
			test_totalSeq_list.append(t_totalSeq)
		else:
			dev_list.append(t_tokenLabels)
			dev_label_list.append(codedSen_conceLabel_list[t_totalSeq])
	label_data = {}
	label_data["train"] = train_label_list
	label_data["test"] = test_label_list
	label_data["dev"] = dev_label_list
	
	return [train_list, test_list, dev_list, test_totalSeq_list, label_data]
def split(tokenLabels_list):
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
def split2(tokenLabels_list):
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


	return [train_list, eval_list]
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
		count = 0
		file = open(folder + name_list[i] + ".txt", "w")
		for tokenLabels in t_list:
			for tokenLabel in tokenLabels:
				t_label = tokenLabel[1]
				file.write(tokenLabel[0] + " " + t_label + "\n")
				count += 1
			file.write("\n")
			count += 1
		file.close()
def write_labels():
	file = open("labels.txt", "w")
	file.write("X\n")
	file.write("O\n")
	file.write("B-PO\n")
	file.write("I-PO\n")
	file.write("B-NE\n")
	file.write("I-NE\n")
	file.write("B-NU\n")
	file.write("I-NU\n")
	file.close()
def write_labels2():
	file = open("labels.txt", "w")
	file.write("X\n")
	file.write("O\n")
	file.write("B-IV\n")
	file.write("I-IV\n")
	file.write("B-DV\n")
	file.write("I-DV\n")
	file.write("B-MO\n")
	file.write("I-MO\n")
	file.write("B-ME\n")
	file.write("I-ME\n")
	file.write("B-CV\n")
	file.write("I-CV\n")
	file.close()
def write_labels3():
	file = open("labels.txt", "w")
	file.write("X\n")
	file.write("O\n")
	file.write("B-PA\n")
	file.write("I-PA\n")
	file.write("B-SU\n")
	file.write("I-SU\n")
	file.write("B-RE\n")
	file.write("I-RE\n")
	file.close()