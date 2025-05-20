from typing import List, Dict, Tuple

def categorize_labels(label_dicts: List[Dict[str, any]])  -> Tuple[List[Dict[str, any]], str, bool]:
    """
    Categorize labels into pets and other labels.

    :param label_dicts: List of label dictionaries with keys 'name', 'confidence', and 'parents'.
    :return: A tuple containing:
             - List of pet labels with 'Confidence' and 'Name' keys.
             - Concatenated string of pet label names.
             - Boolean indicating the presence of a face label.
    """
    pet_labels = []
    prompt = ""
    pet = False
    there_is_face = False

    for label in label_dicts:
        if label['name'] == 'Face':
            there_is_face = True
        if label['name'] == 'Pet' or label['name'] == 'Animal' or any(parent['Name'] == 'Pet' for parent in label['parents']):
            if not pet:
                pet = True
            if label['confidence'] >= 60:
                pet_labels.append({
                    "Confidence": label['confidence'],
                    "Name": label['name']
                })
                prompt += label['name'] + " "
            
    return pet_labels, prompt, there_is_face