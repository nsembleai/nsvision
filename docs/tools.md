# Command line tools
Here are some commandline tools which we have included in library to make the process easy for anyone working on image classification or object detection and needs os related processing help like renaming files in sequence or divide data by folders etc.

# Tools
## Split Data
Most useful with image classification , split data as per `train` `val` `test` and `QA` with specific ratio. <br>
`note: if you just want to split data for train and test , set ratio 0 for that folder`

* Syntax

```bash
split_data -d path_to_data_folder -r ratio_in_tuple_string
```

* example

```bash
split_data -d "./cats_vs_dogs" -r "(70,10,10,10)"
```
This will split data inside class folder as 70% for training , 10% validiation, 10% testing and 10% for QA.

For more information about using command line tool:
```bash
split_data -h
```
<br>

## Rename multiple files
Sequentially rename multiple files at once. You can also specify your own numbering series while renaming files

* Syntax

```bash
rename_files -n common name -f folder path -i number from which renaming to be started
```

* example

```bash
rename_files -n "image_" -f "./image_folder" -i 1
```
This will rename the files in the image_folder 

For more information about using command line tool:
```bash
rename_files -h
```
<br>

## Tumor data extractor

Specifically for extracting and converting the mat files of brain tumor image data 
from the downloaded zip file using this [link](https://figshare.com/articles/brain_tumor_dataset/1512427)

* Syntax

```bash
tumor_data_extractor -b folder path of the downloaded zip folder -e extension in which mat files to be converted (default - jpg)
```

* example

```bash
tumor_data_extractor -b "./1512427.zip" -e png
```
This will convert all the .mat file in the above zip folder into the given extension file format(default .jpg)
All the converted files will be save in separate folder named brain_tumor_data in their respective tumor name folder

For more information about using command line tool:
```bash
tumor_data_extractor -h
```
<br>

## Split data (GUI)
gui version of split data
```bash
split_data_gui
```