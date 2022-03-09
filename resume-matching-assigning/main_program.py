# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:47:45 2022

@author: Admin
"""

import os
from os import listdir
from os.path import isfile, join
import logging
import pandas as pd
from resume_util import *

logging.basicConfig(level=logging.DEBUG,filename="log_resume_assignment.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

try:
    #Read the file
    logging.info("Started processing ")
    mypath = input("Enter the path where resumes present : ")
    logging.info("Started reading the resumes from path : " + str(mypath))
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    final_database=pd.DataFrame()
    i = 0 
    file_name = []
    linkedin_prof = []
    git_prof = []
    email_lst = []
    skills_lst = []
    comm = []
    while i < len(onlyfiles):
        file = onlyfiles[i]
        logging.info("****************************************")
        logging.info("Started reading resume " + str(file))
        ext = os.path.splitext(file)[-1].lower()
        if ext == '.pdf':
            text = pdfextract(file)
        elif ext == '.docx':
            text = extract_text_from_docx(file)
        else:
            comm.append('Not in either acceptable pdf or docx format')
            logging.info("Not in either acceptable pdf or docx format")
        
        head, tail = os.path.split(file)
        file_name.append(tail)
        logging.info("Fetching Linkedin details if any")
        linkedin_text = extract_linkedin(text)
        linkedin_prof.append(linkedin_text)
        logging.info("Fetching email details if any")
        email_text = extract_email(text)
        email_lst.append(email_text)
        logging.info("Fetching github details if any")
        github_text = extract_github(text)
        git_prof.append(github_text)  
        logging.info("Fetching skills details ")
        skills_list = fetch_skill_list()
        skills_text = extract_skills(text,skills_list)
        skills_lst.append(skills_text) 
        logging.info("finished reading resume " + str(file))
        logging.info("****************************************")
        i +=1
    final_database['filename'] = file_name
    final_database['linkedin'] = linkedin_prof
    final_database['email'] = email_lst
    final_database['github'] = git_prof
    final_database['skills'] = skills_lst
    final_database = final_database.set_index('filename')
    print(final_database.head())
    final_database.to_csv('final_result.csv')

except Exception as e:
    logging.exception("Exception occurred during operations")
    