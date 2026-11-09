Column | Meaning | Units
race | Patient race (values: Caucasian, Asian, African American, Hispanic, other) | Not applicable
gender | Patient gender (values: male, female, unknown/invalid) | Not applicable
age | Patient age grouped in 10-year intervals: [0, 10), [10, 20), ..., [90, 100) | Age bracket in years
weight | Patient weight | Pounds
admission_type_id | Categorical integer identifier of the admission type, corresponding to 9 distinct values (e.g., emergency, urgent, elective, newborn, not available) | Not applicable
discharge_disposition_id | Categorical integer identifier of the discharge disposition, corresponding to 29 distinct values (e.g., discharged to home, expired, not available) | Not applicable
admission_source_id | Categorical integer identifier of the admission source, corresponding to 21 distinct values (e.g., physician referral, emergency room, transfer from another hospital) | Not applicable
time_in_hospital | Integer number of days between admission and discharge | Days
payer_code | Categorical integer identifier of the health insurance provider, corresponding to 23 distinct values (e.g., Blue Cross/Blue Shield, Medicare, self-pay) | Not applicable
medical_specialty | Categorical integer identifier of the specialty of the admitting physician, corresponding to 84 distinct values (e.g., cardiology, internal medicine, family/general practice, surgeon) | Not applicable
num_lab_procedures | Number of lab tests performed during the encounter | Count
num_procedures | Number of procedures (other than lab tests) performed during the encounter | Count
num_medications | Number of distinct generic medication names administered during the encounter | Count
number_outpatient | Number of outpatient visits of the patient in the year preceding the encounter | Visits
number_emergency | Number of emergency visits of the patient in the year preceding the encounter | Visits
number_inpatient | Number of inpatient visits of the patient in the year preceding the encounter | Visits
diag_1 | Primary diagnosis of the encounter (first three digits of ICD-9) | Not applicable
diag_2 | Secondary diagnosis of the encounter (first three digits of ICD-9) | Not applicable
diag_3 | Additional secondary diagnosis of the encounter (first three digits of ICD-9) | Not applicable
number_diagnoses | Number of diagnoses entered into the system | Count
max_glu_serum | Result range of the glucose serum test, or 'none' if the test was not measured (values: >200, >300, normal, none) | Not applicable
A1Cresult | Result range of the HbA1c test, or 'none' if the test was not measured (values: >8, >7, normal, none) | Not applicable
metformin | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
repaglinide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
nateglinide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
chlorpropamide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
glimepiride | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
acetohexamide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
glipizide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
glyburide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
tolbutamide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
pioglitazone | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
rosiglitazone | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
acarbose | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
miglitol | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
troglitazone | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
tolazamide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
examide | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
citoglipton | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
insulin | Whether the drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
glyburide-metformin | Whether the combination drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
glipizide-metformin | Whether the combination drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
glimepiride-pioglitazone | Whether the combination drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
metformin-rosiglitazone | Whether the combination drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
metformin-pioglitazone | Whether the combination drug was prescribed or the dosage changed, values: up (dosage increased), down (dosage decreased), steady (dosage unchanged), no (not prescribed) | Not applicable
change | Change in diabetic medications during the encounter (either dosage or generic name); values: change, no change | Not applicable
diabetesMed | Any diabetic medication prescribed; values: yes, no | Not applicable
readmitted | Days to inpatient readmission after discharge (values: <30, >30, No record of readmission) | Not applicable
