import spacy
import json
import os
from spacy import displacy
import pandas as pd
import csv
from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
from sklearn.model_selection import train_test_split
import sys, fitz
# nlp = spacy.load("en_core_web_lg")
# doc = nlp("Apple Inc. is located in Cupertino, California")

# Visualize named entities in a Jupyter Notebook
# displacy.render(doc, style="ent")

class CvParsing:
    def __init__(self) -> None:
        self.folder_path = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/cvforscan"
        self.output_csv = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/output/output.csv"

    @staticmethod
    def read_training_data():

        with open ("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/CV-Parsing-using-Spacy-3/data/training/train_data.json", 'r') as f:
            data =  json.load(f)

        return data

    def get_spacy_doc(self,file,data):
        nlp = spacy.blank("en")
        db = DocBin()
        for text, annot in tqdm(data):
            doc = nlp.make_doc(text)
            annot = annot['entities']

            ent = []
            entities_indicies = []
            for start, end, label in annot:
                skip_entity = False
                for idx in range(start, end):
                    if idx in entities_indicies:
                        skip_entity = True
                        break
            if skip_entity == True:
                continue

            entities_indicies = entities_indicies + list(range(start, end))

            try:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")

            except:

                continue

            if span is None:
                err_data= str([start,end])+ "  " + str(text)+ "\n"
                file.write(err_data)

        try:
            doc.ents = ent
            db.add(doc)
        except:
            pass
        return db

    def extract_results(self,filepath):
        training_data = CvParsing.read_training_data()
        skills = []
        experiences = []
        path_csv = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/output/output.csv"
        train,test = train_test_split(training_data,test_size=0.3)
        file = open('/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/JdModel/train_file.txt', 'w')
        db = self.get_spacy_doc(file,train)
        db.to_disk("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/JdModel/train_data.spacy")

        db = self.get_spacy_doc(file,test)
        db.to_disk("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/JdModel/test_data.spacy")
        file.close()

        nlp = spacy.load("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/Scanning/src/JdModel/output/model-best")

        # fname = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/CV/cvforscan/1. VO NGOC PHU.pdf"
        doc = fitz.open(filepath)
        text = ""


        for page in doc:
            text =text+str(page.get_text())

        doc= nlp(text)

        for ent in doc.ents:
                # Log to console
                # print(ent.text, "---->", ent.label_)

                # Write entity data to CSV
                if ent.label_ == "SKILLS":
                    skills.append(ent.text)
                elif ent.label_ == "POST_EXPERIENCE":
                    experiences.append(ent.text)
        skills_str = ", ".join(skills)
        experiences_str = ", ".join(experiences)
        return skills_str, experiences_str


    def process_cvs_in_folder(self):

        #Get files
        all_files = os.listdir(self.folder_path)

        # Initialize or clear the CSV file with headers
        with open(self.output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Filename", "Skills", "Post Experience"])

        for file_name in all_files:
        # Construct the full file path
            file_path = os.path.join(self.folder_path, file_name)
            # Skip directories and non-PDF files
            if not os.path.isfile(file_path) or not file_name.lower().endswith(".pdf"):
                continue
            # Extract skills and experiences from the CV
            skills_str, experiences_str = self.extract_results(file_path)
        # Write the data to CSV
            with open(self.output_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([file_name, skills_str, experiences_str])


cv_parsing = CvParsing()
cv_parsing.process_cvs_in_folder()
