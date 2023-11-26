import json
from collections import Counter

class FindingBestTitleForCV:
    def __init__(self):
        self.data_skills = {}
        self.job_categories = {}
        self.matched_jobs = {}

    def load_job_categories(self):
        self.job_categories_path = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/misc/job_categories.json"
        with open(self.job_categories_path, 'r') as f:
            self.job_categories = json.load(f)

    def preprocess_skills(self, skills):
        # Convert all skills to lowercase and strip extra spaces
        return [skill.lower().strip() for skill in skills]

    def calculate_similarity_scores(self, cv_skills):
        # Convert CV skills to lowercase and strip extra spaces
        cv_skills = self.preprocess_skills(cv_skills)

        scores = Counter()
        for title, skills in self.job_categories.items():
            # Convert job category skills to lowercase and strip extra spaces
            skills = self.preprocess_skills(skills)

            # Calculate the score as the count of matching skills
            score = sum(skill in cv_skills for skill in skills)
            scores[title] = score

        return scores

    def match_skills_with_titles(self):
        for filename, skills in self.data_skills.items():
            scores = self.calculate_similarity_scores(skills)
            # Sort the job titles based on scores in descending order
            best_jobs = scores.most_common()
            self.matched_jobs[filename] = best_jobs

    def print_matched_jobs(self):
        for filename, jobs in self.matched_jobs.items():
            print(f'CV: {filename}')
            for job, score in jobs:
                print(f'{job}: {score}')
            print('---' * 10)
