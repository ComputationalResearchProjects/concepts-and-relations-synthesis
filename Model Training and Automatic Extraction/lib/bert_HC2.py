import random
import json
import networkx as nx

def build_class_hiera(data_list):
  class_hierarchy = {}
  for var_obj in data_list:
    t_label = var_obj["doc_label"]
    t_dict = class_hierarchy
    for item in t_label:
      if item not in t_dict:
        t_dict[item] = {}
      t_dict = t_dict[item]
  return class_hierarchy
def build_DiGraph(class_hiera):
  DG = nx.DiGraph()
  def traverse(node, key):
    DG.add_node(key)
    for t_key in node:
      DG.add_node(t_key)
      DG.add_edge(key, t_key)

      traverse(node[t_key], t_key)
  traverse(class_hiera["<ROOT>"], "<ROOT>")
  return DG
def build_train_dev_test(t_dict, random_seed):
  random.seed(random_seed)
  varia_list = t_dict["varia"]
  label_list = t_dict["label"]

  data_list = []
  for i in range(len(varia_list)):
    t_varia = varia_list[i]

    t_label_list_new = []
    t_label_list = label_list[i]
    culmu_string = ""
    for item_seq in range(len(t_label_list)):
      item = t_label_list[item_seq]
      if item == "":
        break
      else:
        culmu_string += "=>" + item
        t_label_list_new.append(culmu_string)

    t_obj = {}
    t_obj["doc_label"] = t_label_list_new
    t_obj["doc_token"] = t_varia.split(" ")
    t_obj["doc_keyword"] = []
    t_obj["doc_topic"] = []
    data_list.append(t_obj)
  

  class_hierarchy1 = {"<ROOT>":{}}
  class_hierarchy1["<ROOT>"] = build_class_hiera(data_list)
  DG = build_DiGraph(class_hierarchy1)
  node_list = []
  t_nodes = DG.nodes
  for node in t_nodes:
    t_list = [node]
    for node_child in DG.neighbors(node):
      t_list.append(node_child)
    node_list.append(t_list)

  train_data = []
  dev_data = []
  test_data = []
  t_train_label_dict = {}
  t_dev_label_dict = {}
  for obj_seq, obj in enumerate(data_list):
    obj["doc_label"] = obj["doc_label"][-1:]
    t_num = random.randint(1,10)
    if t_num >= 3:
      train_data.append(obj)
      if obj["doc_label"][0] not in t_train_label_dict:
        t_train_label_dict[obj["doc_label"][0]] = 1
      else:
        t_train_label_dict[obj["doc_label"][0]] += 1
    elif t_num >= 2:
      test_data.append(obj)
    elif t_num >= 1:
      dev_data.append(obj)
      if obj["doc_label"][0] not in t_dev_label_dict:
        t_dev_label_dict[obj["doc_label"][0]] = 1
      else:
        t_dev_label_dict[obj["doc_label"][0]] += 1
      
  dev_data2 = []
  test_data2 = []
  for obj in dev_data:
    if obj["doc_label"][0] in t_train_label_dict:
      dev_data2.append(obj)
  for obj in test_data:
    if obj["doc_label"][0] in t_train_label_dict:
      test_data2.append(obj)
  return [train_data, dev_data2, test_data2, node_list]
def build_train_dev_test2(t_dict, random_seed):
  random.seed(random_seed)
  varia_list = t_dict["varia"]
  label_list = t_dict["label"]

  data_list = []
  for i in range(len(varia_list)):
    t_varia = varia_list[i]

    t_label_list_new = []
    t_label_list = label_list[i]
    culmu_string = ""
    for item_seq in range(len(t_label_list)):
      item = t_label_list[item_seq]
      if item == "":
        break
      else:
        culmu_string += "=>" + item
        t_label_list_new.append(culmu_string)

    t_obj = {}
    t_obj["doc_label"] = t_label_list_new
    t_obj["doc_token"] = t_varia.split(" ")
    t_obj["doc_keyword"] = []
    t_obj["doc_topic"] = []
    data_list.append(t_obj)
  

  class_hierarchy1 = {"<ROOT>":{}}
  class_hierarchy1["<ROOT>"] = build_class_hiera(data_list)
  DG = build_DiGraph(class_hierarchy1)
  node_list = []
  t_nodes = DG.nodes
  for node in t_nodes:
    t_list = [node]
    for node_child in DG.neighbors(node):
      t_list.append(node_child)
    node_list.append(t_list)

  train_data = []
  dev_data = []
  test_data = []
  t_train_label_dict = {}
  t_dev_label_dict = {}
  for obj_seq, obj in enumerate(data_list):
    obj["doc_label"] = obj["doc_label"][-1:]
    t_num = random.randint(1,10)
    if t_num >= 3:
      train_data.append(obj)
      if obj["doc_label"][0] not in t_train_label_dict:
        t_train_label_dict[obj["doc_label"][0]] = 1
      else:
        t_train_label_dict[obj["doc_label"][0]] += 1
    elif t_num >= 3:
      test_data.append(obj)
    else:
      dev_data.append(obj)
      if obj["doc_label"][0] not in t_dev_label_dict:
        t_dev_label_dict[obj["doc_label"][0]] = 1
      else:
        t_dev_label_dict[obj["doc_label"][0]] += 1
  test_data.append(data_list[0])
      
  dev_data2 = []
  test_data2 = []
  for obj in dev_data:
    if obj["doc_label"][0] in t_train_label_dict:
      dev_data2.append(obj)
  for obj in test_data:
    if obj["doc_label"][0] in t_train_label_dict:
      test_data2.append(obj)
  return [train_data, dev_data2, test_data2, node_list]
def build_test_pred(t_pred_dict):
  varia_list = t_pred_dict["varia"]

  data_list = []
  for i in range(len(varia_list)):
    t_varia = varia_list[i]


    t_obj = {}
    t_obj["doc_label"] = []
    t_obj["doc_token"] = t_varia.split(" ")
    t_obj["doc_keyword"] = []
    t_obj["doc_topic"] = []
    data_list.append(t_obj)
  return data_list
def read_json(path):
  t_file = open(path, "r")
  json_data = json.load(t_file)
  t_file.close()
  return json_data
def write_json(json_data, path):
  with open(path, "w", encoding = "utf-8") as f:
    for item in json_data:
      line = json.dumps(item)
      f.write(line + "\n")
def write_taxonomy(node_list, path):
  file = open(path, "w")
  for t_list in node_list:
      if len(t_list) == 1:
          continue
      for label_seq, label in enumerate(t_list):
          if label_seq != len(t_list) - 1:
              file.write(label + "\t")
          else:
              file.write(label + "\n")
  file.close()