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


class CvParsing:
    """
        This class is designed for parsing and processing CVs (Curriculum Vitae) for scanning and analysis.

        Attributes:
            folder_path (str): Path to the folder containing the CVs to be scanned. This path should lead to a directory
                            where the CV files are stored.
            output_csv (str): Path to the output CSV file where the results of the CV parsing will be saved. This should
                            be a file path where the output will be written in CSV format.

        The class is initialized with default paths for the folder containing the CVs and the output CSV file.
        These paths need to be provided during the initialization of an instance of this class.

        Example:
            cv_parser = CvParsing()
            # Now cv_parser has 'folder_path' and 'output_csv' attributes set.

        Note:
            This class requires the CVs to be in a specific format or in specific file types that are compatible
            with the parsing mechanism implemented. Ensure that the CVs in the specified folder are in the required
            format for successful parsing.
    """
    def __init__(self) -> None:
        self.folder_path = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/misc/cvforscan"
        self.output_csv = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/output/output.csv"

    @staticmethod
    def read_training_data():

        with open("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/model/CV-Parsing-using-Spacy-3/data/training/train_data.json", 'r') as f:
            data = json.load(f)

        return data

    def get_spacy_doc(self, file, data):
        """
            Processes a batch of text data and annotations to create SpaCy Doc objects, which are then stored in a DocBin.

            This method iterates over the provided data, each element of which should be a tuple of text and its corresponding
            annotations. It creates SpaCy Doc objects from the text and processes the annotations to create entity spans.
            These Docs are then added to a DocBin for later use.

            Parameters:
                file: A file object or file-like object where error data related to entity spans will be written.
                    If a span cannot be created, the start and end indices, along with the text, are written to this file.
                data: An iterable of tuples, where each tuple contains text (str) and its annotations (dict).
                    The annotations dict should have a key 'entities', which is a list of tuples.
                    Each tuple in this list should contain start index, end index, and label of the entity.

            Returns:
                A DocBin object containing the created SpaCy Doc objects.

            Note:
                - This method assumes that 'data' is in a specific format (as described above).
                - Entities are only added to the Doc if their spans do not overlap with previously processed entities in the same text.
                - This method uses a blank English model from SpaCy. To process text in other languages or with more features,
                modify the 'nlp' object creation accordingly.
        """
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
                err_data = str([start, end]) + "  " + str(text) + "\n"
                file.write(err_data)

        try:
            doc.ents = ent
            db.add(doc)

        except:

            pass
        return db

    def extract_results(self, filepath):
        """
        Processes a single CV file, extracting skills and post-experience information using a trained SpaCy model.

        This method reads a CV from the provided file path, processes the text using a pre-trained SpaCy NLP model, and
        extracts entities labeled as 'SKILLS' and 'POST_EXPERIENCE'. It returns strings of concatenated skills and
        experiences extracted from the CV.

        Parameters:
            filepath (str): Path to the CV file to be processed. Currently, this method is configured to process PDF files.

        Returns:
            tuple: A tuple containing two strings: a comma-separated string of skills and a comma-separated string of
                post-experiences extracted from the CV.

        Note:
            This method relies on a specific directory structure and file paths as defined in the method. Ensure that the
            necessary model and training data files are available at the specified locations.
        """
        training_data = CvParsing.read_training_data()
        skills = []
        experiences = []
        # path_csv = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/output/output.csv"
        train, test = train_test_split(training_data, test_size=0.3)
        file = open('/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/model/JdModel/train_file.txt', 'w')
        db = self.get_spacy_doc(file, train)
        db.to_disk("//Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/model/JdModel/train_data.spacy")
        db = self.get_spacy_doc(file, test)
        db.to_disk("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/model/JdModel/test_data.spacy")
        file.close()
        nlp = spacy.load("/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/src/nlp_parse_cv/model/JdModel/output/model-best")
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text = text+str(page.get_text())
        doc = nlp(text)
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
        """
        Processes all CV files in the specified folder, extracting skills and post-experience information from each CV.

        This method iterates over all PDF files in the folder path set in the 'folder_path' attribute of the class.
        It extracts skills and experiences from each CV and writes the results to a CSV file specified by the 'output_csv'
        attribute. The method returns a dictionary containing the extracted skills for each candidate.

        Returns:
            dict: A dictionary where each key is a file name, and the value is a list of skills extracted from the respective CV.

        Note:
            - Only PDF files are processed. Other file types are ignored.
            - The CSV file is initialized (or cleared if it exists) with headers at the beginning of the method.
            - The method assumes a specific structure for the input data and relies on the 'extract_results' method for processing each CV.
        """
        data_skills = {}
        candidate_skills = []

        # Get files
        all_files = os.listdir(self.folder_path)

        # Initialize or clear the CSV file with headers
        with open(self.output_csv, mode='w',
                  newline='', encoding='utf-8') as file:
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
            candidate_skills.append(skills_str)
            data_skills[file_name] = candidate_skills
        # Write the data to CSV
            with open(self.output_csv, mode='a', newline='',
                      encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([file_name, skills_str, experiences_str])

        return data_skills


