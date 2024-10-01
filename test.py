import pandas as pd
import re
from collections import Counter

def load_and_rename_csv(file_path, column_mapping, source_name, delimiter=',', **kwargs):
    try:
        # Incarcam fisierul CSV si redenumim coloanele conform maparii
        df = pd.read_csv(file_path, delimiter=delimiter, **kwargs)
        df = df.rename(columns=column_mapping)
        print(f"Fisierul {file_path} a fost Incarcat si coloanele au fost redenumite.")
        # print(f"Coloane disponibile In {file_path}: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Eroare la Incarcarea {file_path}: {e}")
        return None

# Functie de normalizare a numelor companiilor
def normalize_company_name(df, column):
    if column in df.columns:
        df[column] = df[column].fillna('') # Inlocuim valorile NaN cu un sir gol pentru a preveni erorile
        df[column] = df[column].str.title().apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x)) \
                                        .apply(lambda x: re.sub(r'\s+', ' ', x).strip())
                                    #    .apply(lambda x: ' '.join(word for word in x.split() if len(word) > 2)) \
                                           
        
        # Eliminam sufixele comune din numele companiilor
        suffixes = ['inc', 'company', 'limited', 'ltd', 'co', 'llc', 'pty', 'srl', 'corporation']
        pattern = r'\b(?:' + '|'.join(suffixes) + r')\b'
        df[column] = df[column].apply(lambda x: re.sub(pattern, '', x, flags=re.IGNORECASE).strip())
        return df
    else:
        raise ValueError(f"Coloana {column} nu exista In DataFrame.")
    
# Functie pentru selectarea celui mai lung nume
def get_most_complex_name(names):
    return max(names, key=lambda x: len(x.split())) if names else ''

# Functie pentru combinarea categoriilor
def combine_categories(categories_str):
    if pd.isna(categories_str):
        return 'Nu s-au gasit date suficiente'
    
    category_sets = [cat.split('|') for cat in categories_str.split('---')] # Impartim categoriile dupa separatorul '---'
    all_categories = [item.strip() for sublist in category_sets for item in sublist] # Combinam toate categoriile intr-un singur set
    category_counts = Counter(all_categories) # Numaram frecventa fiecarei categorii
    unique_categories = sorted(set(all_categories)) # Selectionam categoriile unice si ordonam
    combined_categories = ' | '.join(unique_categories)  # Cream un string cu categoriile combinate si separate prin ' | '
    combined_categories = combined_categories.lstrip(' |') # Eliminam orice | la Inceputul sirului rezultat
    return combined_categories

# Functie de normalizare a numerelor de telefon
def normalize_phone_number(phone):
    return re.sub(r'[^\d]', '', str(phone))

# Functie pentru validarea numerelor de telefon
def is_valid_phone_number(phone):
    return bool(re.match(r'^\+?[1-9]\d{1,14}$', phone))

# Functie pentru prioritizarea numerelor de telefon
def prioritize_phone_numbers(phones):
    phone_counts = Counter(normalize_phone_number(phone) for phone in phones)
    return max(phone_counts, key=phone_counts.get, default=None)

import pandas as pd
import re

def normalize_address(address):
    if pd.isna(address) or not address:
        return ''
    address = address.lower()  # Convertim totul la minuscule
    address = re.sub(r'[^\w\s,.-]', '', address)  # Eliminam caracterele nepermise
    address = re.sub(r'\s+', ' ', address).strip()  # Inlocuim spatiile multiple cu un singur spatiu
    address = re.sub(r'[;|]', ', ', address)  # Inlocuim orice separator neuniform cu virgula
    return address

def combine_and_prioritize_address(google_address, facebook_address, website_address, website_components):
    # Normalizam adresele primite din diferite surse
    google_address = normalize_address(google_address)
    facebook_address = normalize_address(facebook_address)
    website_address = normalize_address(website_address)
    
    # Verificam si returnam adresa din Google, Facebook sau Website, daca exista
    if google_address:
        return google_address
    if facebook_address:
        return facebook_address
    if website_address:
        return website_address
    
    # Daca nu avem adrese complete, combinam componentele adresei din website_components
    if website_components:
        # Extragem si normalizam componentele adresei, cu valori implicite pentru lipsuri
        country = normalize_address(website_components.get('main_country', ''))
        region = normalize_address(website_components.get('main_region', ''))
        city = normalize_address(website_components.get('main_city', ''))
        street = normalize_address(website_components.get('street', ''))
        zip_code = normalize_address(website_components.get('zip_code', ''))
        
        # Combina componentele adresei intr-o singura valoare
        components = [country, region, city, street, zip_code]
        combined_address = ', '.join(comp for comp in components if comp)
        
        # Verificam daca avem componente valide dupa combinare
        if combined_address:
            return combined_address

    return 'Nu s-au gasit date suficiente'  # Daca nu avem nicio adresa valida, returnam mesajul corespunzator


def combine_conflicting_values(series, separator='---', column_name=None):
    if column_name == 'phone':
        phones = series.astype(str).dropna().tolist()
        return prioritize_phone_numbers(phones)
    else:
        series = series.astype(str).dropna()
        unique_values = series.unique()
        combined_value = separator.join(sorted(set(unique_values)))
        return combined_value

# Functie pentru combinarea celorlalte functii
def combine_records(group):
    # Verificam daca coloanele necesare exista
    # if 'company_name' not in group.columns:
    #     raise KeyError("Coloana 'company_name' lipseste din grup.")
    # if 'categories' not in group.columns:
    #     raise KeyError("Coloana 'categories' lipseste din grup.")
    # if 'address' not in group.columns:
    #     raise KeyError("Coloana 'address' lipseste din grup.")
    # if 'phone' not in group.columns:
    #     raise KeyError("Coloana 'phone' lipseste din grup.")
    
    company_names = group['company_name'].tolist() # Extragem lista de nume ale companiilor din grup
    combined_name = get_most_complex_name(company_names)  # Obtinem numele combinat
    category = combine_categories('---'.join(group['categories'].dropna())) # Celelalte campuri raman neschimbate, fiind deja tratate in alte parti ale codului
    addresses = group['address'].dropna().tolist()
    
    google_address = addresses[0] if len(addresses) > 0 else None
    facebook_address = addresses[1] if len(addresses) > 1 else None
    website_address = addresses[2] if len(addresses) > 2 else None
    
    website_components = {
        'street': combine_conflicting_values(group['street']) if 'street' in group.columns else '',
        'main_city': combine_conflicting_values(group['main_city']) if 'main_city' in group.columns else '',
        'main_country': combine_conflicting_values(group['main_country']) if 'main_country' in group.columns else '',
        'main_region': combine_conflicting_values(group['main_region']) if 'main_region' in group.columns else '',
        'zip_code': combine_conflicting_values(group['zip_code']) if 'zip_code' in group.columns else ''
    }
    address = combine_and_prioritize_address(google_address, facebook_address, website_address, website_components)
    phone = combine_conflicting_values(group['phone'], column_name='phone')
    # Returnam rezultatele intr-un pd.Series, unde numele companiei este acum combinat
    return pd.Series({
        'company_name': combined_name, 
        'categories': category,
        'address': address,
        'phone': phone,
    })

def main():
    mappings = {
    'facebook': {'categories': 'categories', 'name': 'company_name'},
    'google': {'name': 'company_name', 'address': 'address', 'phone': 'phone', 'category': 'categories'},
    'website': {'s_category': 'categories', 'site_name': 'company_name', 'phone': 'phone'}
    }

    # Incarcam si normalizam datele
    facebook_df = load_and_rename_csv('facebook_dataset.csv', mappings['facebook'], 'facebook', delimiter=',', on_bad_lines='warn', low_memory=False)
    google_df = load_and_rename_csv('google_dataset.csv', mappings['google'], 'google', delimiter=',', on_bad_lines='warn', low_memory=False)
    website_df = load_and_rename_csv('website_dataset.csv', mappings['website'], 'website', delimiter=';', on_bad_lines='warn', low_memory=False)

    # Verificam daca DataFrame-urile nu sunt none inainte de normalizare
    if facebook_df is not None:
        facebook_df = normalize_company_name(facebook_df, 'company_name')
    if google_df is not None:
        google_df = normalize_company_name(google_df, 'company_name')
    if website_df is not None:
        website_df = normalize_company_name(website_df, 'company_name')

    # Combinam toate sursele
    combined_df = pd.concat([facebook_df, google_df, website_df], ignore_index=True)
    
    # Validam si normalizam datele
    combined_df['phone'] = combined_df['phone'].apply(normalize_phone_number)
    combined_df = combined_df[combined_df['phone'].apply(is_valid_phone_number)]
    combined_df = combined_df[combined_df['company_name'].str.len() > 4]
    
    combined_by_company = combined_df.groupby('company_name').apply(combine_records).reset_index(drop=True) # Combinam rândurile pe baza numelui companiei
    
    final_combined_df = combined_by_company.groupby('phone').apply(combine_records).reset_index(drop=True)   # Combinam rândurile pe baza numarului de telefon
    
    # Inlocuim valorile NaN si numerele de telefon nevalide
    final_combined_df['phone'] = final_combined_df['phone'].apply(lambda x: x if len(str(x)) >= 9 else 'Nu s-a gasit un numar de telefon valid')
    final_combined_df['categories'] = final_combined_df['categories'].replace(r'^\s*$', 'Nu s-au gasit suficiente date pentru categorie', regex=True)
    # final_combined_df[['categories', 'address']] = final_combined_df[['categories', 'address']].replace(r'^\s*$', 'Nu s-au gasit suficiente date', regex=True)
    
    final_combined_df.to_csv('test_final.csv', index=False) # Salvam rezultatul final

if __name__ == "__main__":
    main()
