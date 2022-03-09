# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:18:53 2022

@author: Admin
"""

import PyPDF2
import logging
import os
import docx2txt
import re
import requests
import json
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

def pdfextract(file):
    try:
        text1 = ""
        text = []
        logging.info("Started extracting the details from pdf")
        filereader = PyPDF2.PdfFileReader(open(file,'rb'))
        countpage = filereader.getNumPages()
        count = 0
        while count < countpage:
            pageobj = filereader.getPage(count)
            count +=1
            t = pageobj.extractText()
            text.append(t)
        text1 = str(text)
        text1 = text1.replace("\\n", "")
        text1 = text1.lower()
    except Exception as e:
        logging.exception("Exception occured at the time of extracting from PDF " + str(e))
    return text1  

def extract_text_from_docx(docx_path):
    try:
        txt = docx2txt.process(docx_path)
        if txt:
            return txt.replace('\t', ' ')
    except Exception as e:
        logging.exception("Exception occured at the time of extracting from Doc " + str(e))                
    return None

def extract_linkedin(text):
    try:
        str1 = ""
        lreg1 = re.compile('(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/.*')
        lreg2 = re.compile('(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/pub\/.*')
        lreg3 = re.compile('(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/profile\/.*')
        l1 = re.findall(lreg1,text)
        l2 = re.findall(lreg2,text)
        l3 = re.findall(lreg3,text)
        l1.extend(l2)
        l1.extend(l3)
        str1 = ",".join(l1)
    except Exception as e:
        logging.exception("Exception occured at the time of extracting linkedin details " + str(e))
    return str1

def extract_email(text):
    try:
        str1 = ""
        EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
        l = re.findall(EMAIL_REG, text)
        str1 = ",".join(l)
    except Exception as e:
        logging.exception("Exception occured at the time of extracting email details " + str(e))
    return str1

def fetch_skill_list():
    try:
        skills_list = []
        data = requests.get('https://raw.githubusercontent.com/microsoft/SkillsExtractorCognitiveSearch/master/data/skills.json')
        data1 = data.json()
        for i in data1.values():
            skills_list.append(str.lower(i['sources'][0]['displayName']))
    except Exception as e:
        logging.exception("Exception occured at the time of extracting skill list " + str(e))
    return skills_list

def extract_skills(text,skills_list):
    try:
        found_skills1 = ""
        found_skills = set()
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(text)
        filtered_tokens = [w for w in word_tokens if w not in stop_words]
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
        for token in filtered_tokens:
            if token.lower() in skills_list:
                found_skills.add(token)
        for ngram in bigrams_trigrams:
            if ngram.lower() in skills_list:
                found_skills.add(ngram)
        found_skills1 = ",".join(found_skills)
    except Exception as e:
        logging.exception("Exception occured at the time of extracting skill from resume " + str(e))
    return found_skills1

def extract_github(text):
    try:
        str1 = ""
        gitusr = re.compile('(?:https?:)?\/\/(?:www\.)?github\.com\/.*')
        g1 = re.findall(gitusr,text)
        str1 = ",".join(g1)
    except Exception as e:
        logging.exception("Exception occured at the time of extracting github from resume " + str(e))
    return str1
        