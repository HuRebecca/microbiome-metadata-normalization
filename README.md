# Normalization of Public Human Microbiome Metadata from Qiita
Using Python Pandas to engineer features of normalized human metadata for machine learning analysis.
<br> Last updated 3/20/19

## Introduction
The online microbiome analysis platform [Qiita](https://qiita.ucsd.edu/) contains microbial sequencing data for >60,000 public human samples presenting the opportunity to gain greater insight on the effects of the microbiome on the human health and disease. However, effective meta-analyses are often prevented by inconsistent and incompatible metadata. Normalizing and standardizing units, categories, and terminology in an automated fashion will help catalyze the powerful meta-analyses enabled by the platform.

## Data
* Metadata was fetched with RedBiom 
* Contains all human samples from the date stated
* Sample types include fecal, oral, and skin

## Methods 
![method_example](https://github.com/HuRebecca/microbiome-metadata-normalization/blob/master/example.PNG)
* Normalization scripts for the cleaning and pre-processing were written in Python with Pandas library. 
* For each of 20 host attributes, e.g. age, sex, IBD, diabetes, we determined which column headers held relevant information, then wrote scripts to collect and normalize each value into a final “qiita_host_[blank]” column
* The normalization process also including filtering out values that were outside reasonable ranges, e.g bounds of 48-210 cm for height and 0.5-200 kg for weight
* Normalizing certain metrics allowed us to derive new variables.
  * For example, normalizing height and weight allowed us to use those values to calculate BMI and further determine whether the host fell     within a healthy weight range 
  * A total of 17 new variables, including ethnicity, food allergy, medications, etc. were created along with 
* See the bottom of the README for a complete list of normalized column headers and descriptions 

## Summary Statistics
|Sample Type|Number of Rows in Original Metadata|Number of Columns in Original Metadata|
|:-------------:|:-------------:|:-------------:|
|Fecal|40763|2570|
|Oral|4233|1171|
|Skin|7386|979|

## Normalized Column Headers and Descriptions
<br> Note: Quantitative values are float types, True/False are boolean values, and all other, non-nan values are strings; Nans are float
<br>
|Normalized Column Header|Descriptions|
|:-------------:|---------------|
|qiita_host_age|normalized age in years|
|qiita_host_age_units|'years' repeated in all rows|
|qiita_host_sex|normalized sex as 'male' or 'female'|
|qiita_host_ethnicity_white|True if the host identifies as white, False or Nan otherwise|
|qiita_host_ethnicity_black_or_african_american|True if the host identifies as black or African American, False or Nan otherwise|
|qiita_host_ethnicity_hispanic_or_latino|True if the host identifies as hispanic or latino, False or Nan otherwise|
|qiita_host_ethnicity_asian|True if the host identifies as asian, False or Nan otherwise|
|qiita_host_ethnicity_american_indian_or_alaska_native|True if the host identifies as Native American, False or Nan otherwise|
|qiita_host_ethnicity_native_hawaiian_or_other_pacific_islander|True if the host identifies as native Hawaiian or Pacific Islander, False or Nan otherwise|
|qiita_host_ethnicity_other|True if host specified 'other' as ethnicity/race, False or Nan otherwise|
|qiita_host_ethnicity_multiracial|True if host specified 'multi' or some variation as ethnicity/race, False or Nan otherwise|
|qiita_host_multiracial|True if host specified multiple ethinicies/races, False or Nan otherwise|
|qiita_host_ethnicity_combined|string values, most specific host race/ethinicity e.g. 'Japanese-Caucasian'|
|qiita_host_weight|normalized & cleaned weight in kg|
|qiita_host_weight_units|'kg' repeated in all rows|
|qiita_host_height|normalized and cleaned weight in cm|
|qiita_host_height_units|'cm' repeated in all rows|
|qiita_host_bmi|float values, normalized host bmi|
|qiita_host_healthy_weight|True if host falls under healthy weight category, False or Nan otherwise|
|qiita_host_food_allergy|True if host has food allergy (Note: only in fecal normalization file)|
|qiita_host_allergy|True if host has any allergies in allergy dictionaries, False or Nan otherwise |
|qiita_host_cancer|True if host has any cancer in cancer dictionary, False or Nan otherwise |
|qiita_host_ibd|True if host has inflammatory bowel disease, False or Nan otherwise|
|qiita_host_ibd_type|'cd' if host has Crohn's Disease, 'uc' if host has ulcerative colitis, 'not specified' if host has ibd but does not specify what kind, 'not applicable' if host does not have ibd |
|qiita_host_diabetes|True if host has diabetes, False otherwise |
|qiita_host_diabetes_subtype| 'type1' if host has Type I diabetes, 'type2' is host has Type II diabetes, 'not specified' if host has diabetes but does not specify what kind, 'not applicable' if host does not have diabetes|
|qiita_host_disease|True if host has a miscellaneous disease in disease dictionary, False otherwise|
|qiita_host_medication|True if host reported taking any medications, False otherwise |
|qiita_host_healthy|False if host has any disease, allergy, or uses medication, True otherwise|
|qiita_host_body_site|specific body site that smaple was taken from (string type)|
|qiita_host_body_habitat|generalized body habitat that sample was taken from (string type)|
|qiita_host_atherosclerosis|True if host is report to have atherosclerosis, False otherwise|
|qiita_host_arthritis|True if host is report to have arthritis, False otherwise|
|qiita_host_alzheimers|True if host is report to have Alzheimer's Disease, False otherwise|
|qiita_sample_type|'stool'(fecal), 'oral'(oral), 'skin'(skin) repeated in all rows |
|qiita_empo_1|'host-associated' repeated in all rows |
|qiita_empo_2|'animal' repeated in all rows |
|qiita_empo_3|'animal distal gut' (fecal),  'animal proximal gut' (oral),  'animal surface' (skin) repeated in all rows|
|qiita_host_scientific_name|'Homo sapiens' repeated in all rows|
|qiita_host_taxid|9606 repeated in all rows|
|qiita_host_common_name|'human' repeated in all rows|
|qiita_env_feature|'human-associated habitat' repeated in all rows|

