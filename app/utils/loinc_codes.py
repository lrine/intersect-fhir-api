"""
Common LOINC Codes for Intersect Platform
Reference: https://loinc.org/
"""

VITAL_SIGNS = {
    # Blood Pressure
    "85354-9": "Blood pressure panel",
    "8480-6": "Systolic blood pressure",
    "8462-4": "Diastolic blood pressure",
    
    # Pulse/Heart Rate
    "8867-4": "Heart rate",
    "8893-0": "Heart rate by Pulse oximetry",
    
    # Oxygen Saturation
    "2710-2": "Oxygen saturation in Arterial blood by Pulse oximetry",
    "59408-5": "Oxygen saturation in Arterial blood by Pulse oximetry",
    
    # Temperature
    "8310-5": "Body temperature",
    "8331-1": "Oral temperature",
    "8332-9": "Rectal temperature",
    
    # Weight
    "29463-7": "Body weight",
    "3141-9": "Body weight Measured",
    
    # Height
    "8302-2": "Body height",
    "8306-3": "Body height --lying",
    
    # BMI
    "39156-5": "Body mass index (BMI)",
    
    # Respiratory Rate
    "9279-1": "Respiratory rate",
}

PREGNANCY_OBSERVATIONS = {
    "11884-4": "Gestational age at birth",
    "11885-1": "Gestational age",
    "11612-9": "Estimated date of delivery",
    "57722-1": "Number of fetuses",
    "11878-6": "Previous live births",
    "11977-6": "Previous pregnancies",
    "11636-8": "Cesarean section",
    "73812-0": "Pregnancy status",
    "82810-3": "Pregnancy intention",
}

GENOMIC_TESTS = {
    # BRCA
    "81247-9": "BRCA1 gene mutations found",
    "81248-7": "BRCA2 gene mutations found",
    
    # General Genomics
    "48018-6": "Gene studied [ID]",
    "81290-9": "Genomic DNA sequence variation",
    "69548-6": "Genetic variation clinical significance",
    "53037-8": "Genetic disease sequence variation interpretation",
    "81252-9": "Discrete genetic variant",
    "48002-0": "Genomic source class",
    "48001-2": "Cytogenetic (chromosome) location",
    
    # Pharmacogenomics
    "79716-7": "CYP2C19 gene product metabolizer status",
    "79717-5": "CYP2C9 gene product metabolizer status",
    "79718-3": "CYP2D6 gene product metabolizer status",
}

LAB_RESULTS = {
    # Blood Glucose
    "2339-0": "Glucose [Mass/volume] in Blood",
    "2345-7": "Glucose [Mass/volume] in Serum or Plasma",
    "41653-7": "Glucose [Mass/volume] in Capillary blood",
    
    # Hemoglobin
    "718-7": "Hemoglobin [Mass/volume] in Blood",
    "20509-6": "Hemoglobin [Mass/volume] in Blood by calculation",
    "55782-7": "Hemoglobin A1c/Hemoglobin.total in Blood",
    
    # Complete Blood Count (CBC)
    "6690-2": "Leukocytes [#/volume] in Blood by Automated count",
    "789-8": "Erythrocytes [#/volume] in Blood by Automated count",
    "777-3": "Platelets [#/volume] in Blood by Automated count",
    "4544-3": "Hematocrit [Volume Fraction] of Blood",
    
    # Lipid Panel
    "2093-3": "Cholesterol [Mass/volume] in Serum or Plasma",
    "2085-9": "HDL Cholesterol [Mass/volume] in Serum or Plasma",
    "13457-7": "LDL Cholesterol [Mass/volume] in Serum or Plasma",
    "2571-8": "Triglyceride [Mass/volume] in Serum or Plasma",
    
    # Metabolic Panel
    "2951-2": "Sodium [Moles/volume] in Serum or Plasma",
    "2823-3": "Potassium [Moles/volume] in Serum or Plasma",
    "2075-0": "Chloride [Moles/volume] in Serum or Plasma",
    "1975-2": "Bilirubin.total [Mass/volume] in Serum or Plasma",
    "1920-8": "Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma",
    "1742-6": "Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma",
}

OBSERVATION_CATEGORIES = {
    "vital-signs": "Vital Signs",
    "laboratory": "Laboratory",
    "imaging": "Imaging",
    "social-history": "Social History",
    "exam": "Exam",
    "activity": "Activity",
    "survey": "Survey",
    "therapy": "Therapy",
}

INTERPRETATION_CODES = {
    "N": "Normal",
    "A": "Abnormal",
    "H": "High",
    "L": "Low",
    "HH": "Critical high",
    "LL": "Critical low",
    "AA": "Abnormal alert",
    "U": "Significant change up",
    "D": "Significant change down",
}


def get_loinc_display(code: str) -> str:
    """
    Get display text for a LOINC code
    
    Args:
        code: LOINC code
        
    Returns:
        str: Display text or code if not found
    """
    all_codes = {**VITAL_SIGNS, **PREGNANCY_OBSERVATIONS, **GENOMIC_TESTS, **LAB_RESULTS}
    return all_codes.get(code, code)
