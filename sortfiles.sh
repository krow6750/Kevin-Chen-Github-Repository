#!/bin/bash

'
Course:        DCS 211 Winter 2022
Assignment:    Project 1
Topic:         Bash Scripting
Purpose:       Use a bash script to easily organize the Downloads folder

Student Name: Rebecca Anderson
Partner Name: Kevin Chen

Other students outside my pair that I received help from ('N/A' if none):
    N/A

Other students outside my pair that I gave help to ('N/A' if none):
    N/A

Citations/links of external references used ('N/A' if none):
    https://devhints.io/bash
    stackoverflow.com
    geeksforgeeks.org

'

cd ~/Downloads        #moves out of directory the script is called from & into Downloads

#array representing folders to be created
folders=('pdfs' 'python' 'csv_files' 'word_documents' 'powerpoints' 'excel_sheets' 'applications' 'images' 'miscellaneous')

for i in ${folders[@]}; do        #making directories for different file types
  mkdir -p ${i}                   #only creates directory if directory
done                              #does not exist

#arrays representing main file types within Downloads (array)
#and folders for sorting each type (array2)
array=('.pdf' '.py' '.csv' '.docx' '.pptx' '.xlsx' '.app')
array2=('pdfs' 'python' 'csv_files' 'word_documents' 'powerpoints' 'excel_sheets' 'applications')

#separate array for image file types because multiple file types correspond to images
image_files=('.png' '.PNG' '.jpg' '.jpeg' '.JPG' '.heic' '.HEIC')

#iterates through arrays to add all files of one type to corresponding directory
for i in ${!array[@]}; do
  if [[ -e *${array[i]} ]]; then
    mv *${array[i]} ~/Downloads/${array2[i]}
  else
    echo "No files of type ${array[i]} exist in Downloads"
  fi
done

#iterates through image_files to add all files of each file type to images folder
for i in ${image_files[@]}; do
  if [[ -e *${i} ]]; then
    mv *${i} ~/Downloads/images
  else
    echo "No files of type ${i} exist in Downloads"
  fi
done

#adds all remaining files in Downloads to miscellaneous folder
find . -maxdepth 1 \( ! -type d \) -exec mv {} miscellaneous \;
