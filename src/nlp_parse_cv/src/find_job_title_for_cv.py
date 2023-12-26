import json
from collections import Counter
from  cv_parse import CvParsing as CVP
import pandas as pd

class FindingBestTitleForCV:
    """
    This class is designed to find the best matching job titles for candidates based on the skills extracted from their CVs.

    The class matches the skills listed in the CVs against predefined job categories and their associated skills.
    It then calculates similarity scores to determine which job titles are the best match for each candidate.

    Attributes:
        data_skills (dict): A dictionary to store skills extracted from CVs.
        job_categories (dict): A dictionary to store job categories and their associated skills.
        matched_jobs (dict): A dictionary to store the best matching job titles for each CV.
        candidates_skills (str): Path to the CSV file where the extracted skills from CVs are stored.

    Methods:
        load_job_categories: Loads job categories and their skills from a JSON file.
        preprocess_skills: Processes skills for similarity comparison.
        calculate_similarity_scores: Calculates similarity scores between CV
        skills and job category skills.
        match_skills_with_titles: Matches CV skills with job titles and
        stores the best matches.
        print_matched_jobs: Prints the matched job titles for each CV.
    """
    def __init__(self):
        self.data_skills = {}
        self.job_categories = {}
        self.matched_jobs = {}
        candidates_skills_initiate: CVP = CVP()
        self.candidates_skills = candidates_skills_initiate.process_cvs_in_folder()

    @staticmethod
    def load_job_categories():
        """
        Loads job categories and their associated skills from a JSON file.
        The job categories and skills are stored in the 'job_categories' attribute of the class.
        The path to the JSON file is hardcoded in the method.
        """
        job_categories_path = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/misc/job_categories.json"
        with open(job_categories_path, 'r') as f:
            job_categories = json.load(f)
        # print(job_categories)
        return job_categories

    def preprocess_skills(self, skills):
        """
        Processes a list of skills by converting them to lowercase and stripping extra spaces.
        Parameters:
            skills (list of str): A list of skills to preprocess.

        Returns:
            list of str: A list of processed skills.
        """
        # Convert all skills to lowercase and strip extra spaces
        return [skill.lower().strip() for skill in skills]

    def calculate_similarity_scores(self, cv_skills):
        """
        Calculates similarity scores for each job category based on the number of matching skills in a CV.

        Parameters:
            cv_skills (list of str): A list of skills extracted from a CV.

        Returns:
            Counter: A Counter object with job titles as keys and similarity scores as values.
        """
        # Convert CV skills to lowercase and strip extra spaces
        cv_skills = self.preprocess_skills(cv_skills)
        scores = Counter()
        for title, skills in self.load_job_categories().items():
            # Convert job category skills to lowercase and strip extra spaces
            skills = self.preprocess_skills(skills)

            # Calculate the score as the count of matching skills
            score = sum(skill in cv_skills for skill in skills)
            scores[title] = score

        return scores

    def match_skills_with_titles(self):
        """
        Matches skills extracted from CVs with job titles based on similarity scores.

        This method iterates over each CV, calculates similarity scores with
            job categories, and determines the best
        matching job titles. The results are stored in the 'matched_jobs' attribute.
        """
        matched_jobs = {}
        for filename, skills in self.candidates_skills.items():
            scores = self.calculate_similarity_scores(skills)
            # Sort the job titles based on scores in descending order
            best_jobs = scores.most_common()
            matched_jobs[filename] = best_jobs
        return matched_jobs

    def print_matched_jobs(self):

        """
        Prints the matched job titles and their scores for each CV.

        This method iterates over the 'matched_jobs' attribute and prints the best matching job titles for each CV.
        """
        candidate_title_scoring = []
        match_skills_with_title = self.match_skills_with_titles()
        for filename, jobs in match_skills_with_title.items():
            print(f'CV: {filename}')
            print("jobs", jobs)
            for job, score in jobs:
                print(f'{job}: {score}')
            candidate_title_scoring.append((filename, jobs))
            print('---' * 10)
        df = pd.DataFrame(candidate_title_scoring, columns=['Candidate', 'Job score'])
        csv_filename = 'candidate_scoring.csv'
        df.to_csv(csv_filename, index=False)

find_cv = FindingBestTitleForCV()

find_cv.print_matched_jobs()