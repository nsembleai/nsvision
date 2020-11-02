import os
import glob
import csv
import json
import xml.etree.ElementTree as ET

class XMLConversion:
	"""This class converts xml files into csv,json,txt"""
    def __init__(self,xml_dir, out_dir = None):
        self.xml_dir = xml_dir
        self.out_dir = out_dir
        
    def voc_xml_to_csv(self):
        xml_list = []
        for xml_file in glob.glob(self.xml_dir + '/*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                value = (root.find('filename').text,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         member[0].text,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                xml_list.append(value)
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        try:
            if self.out_dir == None:
                self.out_dir = "output.csv"
            if self.out_dir.endswith("csv"):
                with open(self.out_dir, 'w') as f:
                    write = csv.writer(f) 
                    write.writerow(column_name)
                    write.writerows(xml_list) 
                print(f"csv created successfully {self.out_dir}")
            else:
                print(f'Check File Extension {self.out_dir}')
        except:
            print("Error! Could not write csv")
        
    def parse_voc_annotation(self,xml, labels=[]):
        xml_data = {'object':[]}
        try:
            tree = ET.parse(xml)
        except Exception as e:
            print(e)
            print('Ignore this bad annotation: ' + xml)
        for elem in tree.iter():
            if 'filename' in elem.tag:
                xml_data['filename'] = elem.text
            if 'width' in elem.tag:
                xml_data['width'] = int(elem.text)
            if 'height' in elem.tag:
                xml_data['height'] = int(elem.text)
            if 'object' in elem.tag or 'part' in elem.tag:
                obj = {}

                for attr in list(elem):
                    if 'name' in attr.tag:
                        obj['name'] = attr.text

                        if len(labels) > 0 and obj['name'] not in labels:
                            break
                        else:
                            xml_data['object'] += [obj]

                    if 'bndbox' in attr.tag:
                        for dim in list(attr):
                            if 'xmin' in dim.tag:
                                obj['xmin'] = int(round(float(dim.text)))
                            if 'ymin' in dim.tag:
                                obj['ymin'] = int(round(float(dim.text)))
                            if 'xmax' in dim.tag:
                                obj['xmax'] = int(round(float(dim.text)))
                            if 'ymax' in dim.tag:
                                obj['ymax'] = int(round(float(dim.text)))
        return xml_data

    def get_coco_annotation_from_obj(self,xml_obj_data, label2id):
        label = xml_obj_data['name']
        assert label in label2id, f"Error: {label} is not in label2id !"
        category_id = label2id[label]
        xmin = int(xml_obj_data['xmin']) - 1
        ymin = int(xml_obj_data['ymin']) - 1
        xmax = int(xml_obj_data['xmax'])
        ymax = int(xml_obj_data['ymax'])
        assert xmax > xmin and ymax > ymin, f"Box size error !: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"
        o_width = xmax - xmin
        o_height = ymax - ymin
        ann = {
            'area': o_width * o_height,
            'iscrowd': 0,
            'bbox': [xmin, ymin, o_width, o_height],
            'category_id': category_id,
            'ignore': 0,
            'segmentation': []  # This script is not for segmentation
        }
        return ann
    
    def get_label2id(self,ann_path_list):
        
        seen_labels = {}
        
        for ann in ann_path_list:
            xml_data = self.parse_voc_annotation(ann)
            for dct in xml_data['object']:
                if dct['name'] in seen_labels:
                    seen_labels[dct['name']] += 1
                else:
                    seen_labels[dct['name']] = 1
        label2id = {k:v+1 for (v,k) in enumerate(list(seen_labels.keys()))}
        return label2id
    

    def get_object_params(self,xml_obj_data,width,height):
        
        xmin = xml_obj_data['xmin']
        xmax = xml_obj_data['xmax']
        ymin = xml_obj_data['ymin']
        ymax = xml_obj_data['ymax']
            
        image_width = 1.0 * width
        image_height = 1.0 * height

        absolute_x = xmin + 0.5 * (xmax - xmin)
        absolute_y = ymin + 0.5 * (ymax - ymin)

        absolute_width = xmax - xmin
        absolute_height = ymax - ymin

        x = absolute_x / image_width
        y = absolute_y / image_height
        abs_width = absolute_width / image_width
        abs_height = absolute_height / image_height

        return x, y, abs_width, abs_height
        


    def voc_xml_to_coco_json(self):

        ann_path_list = glob.glob(os.path.join(self.xml_dir,"*.xml"))
        if ann_path_list == []:
            print('No XML files Found')
            
        label2id = self.get_label2id(ann_path_list)

        output_json_dict = {
            "images": [],
            "type": "instances",
            "annotations": [],
            "categories": []
        }
        bnd_id = 1
        for i,ann in enumerate(sorted(ann_path_list)):
            xml_data = self.parse_voc_annotation(ann)
                
            filename = xml_data['filename']
            width = xml_data['width']
            height = xml_data['height']

            image_info = {
                'file_name': filename,
                'height': height,
                'width': width,
                'id': i
            }

            output_json_dict['images'].append(image_info)
            
            for obj_data in xml_data['object']:
                ann = self.get_coco_annotation_from_obj(obj_data, label2id)
                ann.update({'image_id': image_info['id'], 'id': bnd_id})
                output_json_dict['annotations'].append(ann)
                bnd_id = bnd_id + 1

        for label, label_id in label2id.items():
            category_info = {'supercategory': 'none', 'id': label_id, 'name': label}
            output_json_dict['categories'].append(category_info)

        try:
            if self.out_dir == None:
                self.out_dir = "output.json"
            if self.out_dir.endswith("json"):
                with open(self.out_dir, 'w') as f:
                    output_json = json.dumps(output_json_dict)
                    f.write(output_json)
                    print(f"JSON created successfully {self.out_dir}")
            else:
                print(f'Check File Extension {self.out_dir}')
        except:
            print("Error! Could not write json")
        
            
	def voc_xml_to_txt(self):
		try:
			ann_path_list = glob.glob(os.path.join(self.xml_dir,"*.xml"))
		except:
			print(f"Cannot create list of xml files. Check {self.xml_dir}")
	    if ann_path_list == []:
	    	print('No XML files Found')
	        
        label2id = self.get_label2id(ann_path_list)
        result = []
        for i,ann in enumerate(sorted(ann_path_list)):
            xml_data = self.parse_voc_annotation(ann)
            
            width = xml_data['width']
            height = xml_data['height']
            
            for xml_obj_data in xml_data['object']:
                x, y, abs_width, abs_height = self.get_object_params(xml_obj_data,width,height)
                result.append("%d %.6f %.6f %.6f %.6f" % (label2id[xml_obj_data['name']], x, y, abs_width, abs_height))
            try:
                if self.out_dir == None:
                    self.out_dir = os.path.dirname(os.path.abspath("__file__"))
                with open(os.path.join(self.out_dir, "%s.txt" % os.path.splitext(xml_data['filename'])[0]), "w+") as f:
                    f.write("\n".join(result))
                print(f"txt created successfully {self.out_dir}")
                result = []
            except:
                print("Error! Could not write txt")