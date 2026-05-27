import pandas as pd
import re

def fix_outliers(df):
    """Fix outlier values in the dataset"""
    df_fixed = df.copy()
    
    # Fix 1: Display size (35 inches -> 15.6)
    if 'display(in inch)' in df_fixed.columns:
        df_fixed.loc[df_fixed['display(in inch)'] == 35.0, 'display(in inch)'] = 15.6
    
    # Fix 2: Storage anomalies (4GB and 5GB -> 512GB)
    if 'storage_gb' in df_fixed.columns:
        df_fixed.loc[df_fixed['storage_gb'] == 4, 'storage_gb'] = 512
        df_fixed.loc[df_fixed['storage_gb'] == 5, 'storage_gb'] = 512
    
    # Fix 3: Fill missing processor_gen with -1
    if 'processor_gen' in df_fixed.columns:
        df_fixed['processor_gen'] = df_fixed['processor_gen'].fillna(-1)
    
    return df_fixed

def extract_ram_gb(ram_str):
    """Extract RAM size in GB from string."""
    if pd.isna(ram_str):
        return None
    match = re.search(r'(\d+)\s*GB', str(ram_str))
    return int(match.group(1)) if match else None


def extract_total_storage_gb(storage_str):
    """Extract total storage capacity in GB from string."""
    if pd.isna(storage_str):
        return None

    total_gb = 0
    storage_str = str(storage_str)

    matches = re.findall(r'(\d+)\s*(TB|GB|SSD|HDD)', storage_str, re.IGNORECASE)

    for num, unit in matches:
        num = int(num)
        unit_lower = unit.lower()
        if unit_lower == 'tb':
            num *= 1024
        total_gb += num

    if total_gb == 0:
        match = re.search(r'(\d+)', storage_str)
        if match:
            total_gb = int(match.group(1))

    return total_gb if total_gb > 0 else None


def simplify_os(os_str):
    """Simplify operating system names into categories."""
    if pd.isna(os_str):
        return 'Unknown'

    os_lower = str(os_str).lower()

    if 'windows 11' in os_lower:
        return 'Windows 11'
    elif 'windows 10' in os_lower:
        return 'Windows 10'
    elif 'mac' in os_lower or 'macos' in os_lower:
        return 'macOS'
    elif 'dos' in os_lower:
        return 'DOS'
    elif 'linux' in os_lower:
        return 'Linux'
    elif 'chrome' in os_lower:
        return 'Chrome OS'
    else:
        return 'Other'


def extract_processor_brand(proc_str):
    """Extract processor brand from processor string."""
    if pd.isna(proc_str):
        return 'Unknown'
    proc_lower = str(proc_str).lower()
    if 'intel' in proc_lower:
        return 'Intel'
    elif 'amd' in proc_lower:
        return 'AMD'
    elif 'apple' in proc_lower or 'm1' in proc_lower or 'm2' in proc_lower or 'm3' in proc_lower:
        return 'Apple'
    else:
        return 'Other'


def extract_processor_series(proc_str):
    """Extract processor series from processor string."""
    if pd.isna(proc_str):
        return 'Unknown'
    proc_str = str(proc_str)

    # Intel Core series
    match = re.search(r'Core\s+(i\d|i\d-\d+\w*)', proc_str, re.IGNORECASE)
    if match:
        return match.group(1)

    # AMD Ryzen series
    match = re.search(r'Ryzen\s+(\d+)', proc_str, re.IGNORECASE)
    if match:
        return f'Ryzen {match.group(1)}'

    # Other processor types
    if 'athlon' in proc_str.lower():
        return 'Athlon'

    match = re.search(r'A\d+', proc_str, re.IGNORECASE)
    if match:
        return match.group(0)

    if 'pentium' in proc_str.lower():
        return 'Pentium'
    if 'celeron' in proc_str.lower():
        return 'Celeron'

    return 'Other'


def extract_generation(proc_str):
    """Extract processor generation from processor string."""
    if pd.isna(proc_str):
        return None

    proc_str = str(proc_str)

    # Intel generation
    match = re.search(r'\(?(\d+)(?:th|nd|rd|st)?\s*Gen\)?', proc_str, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # AMD generation
    match = re.search(r'Ryzen\s+\d\s+(\d{4})[A-Z]*', proc_str, re.IGNORECASE)
    if match:
        series = int(match.group(1))
        return series // 1000

    if 'amd' in proc_str.lower() or 'ryzen' in proc_str.lower():
        match = re.search(r'(\d{4})', proc_str)
        if match:
            series = int(match.group(1))
            return series // 1000

    return None


def extract_brand(name_str):
    """Extract laptop brand from name string."""
    if pd.isna(name_str):
        return 'Unknown'
    name_lower = str(name_str).lower()
    brands = [
        'lenovo', 'asus', 'dell', 'hp', 'apple', 'acer', 'msi',
        'realme', 'xiaomi', 'mi', 'samsung', 'lg', 'razer',
        'gigabyte', 'huawei', 'honor', 'oppo', 'vivo', 'infinix'
    ]
    for brand in brands:
        if brand in name_lower:
            return brand.capitalize()
    return 'Other'


def extract_storage_type(storage_str):
    """Extract storage type (SSD, HDD, or hybrid) from storage string."""
    if pd.isna(storage_str):
        return 'Unknown'
    storage_lower = str(storage_str).lower()
    if 'ssd' in storage_lower and 'hdd' in storage_lower:
        return 'SSD+HDD'
    elif 'ssd' in storage_lower:
        return 'SSD'
    elif 'hdd' in storage_lower:
        return 'HDD'
    else:
        return 'Other'


def extract_display_size(display_str):
    """Extract display size in inches from display string."""
    if pd.isna(display_str):
        return None
    match = re.search(r'(\d+\.?\d*)', str(display_str))
    return float(match.group(1)) if match else None


def process_full_dataset(df):
    """
    Process the dataset by extracting features from raw columns.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Raw dataframe with laptop data
        
    Returns
    -------
    pandas.DataFrame
        Processed dataframe with engineered features
    """
    # Create a copy
    df_processed = df.copy()

    # Process RAM
    df_processed['ram_gb'] = df_processed['ram'].apply(extract_ram_gb)

    # Process storage
    df_processed['storage_gb'] = df_processed['storage'].apply(extract_total_storage_gb)

    # Process OS
    df_processed['os_simplified'] = df_processed['os'].apply(simplify_os)

    # Process processor
    df_processed['processor_brand'] = df_processed['processor'].apply(extract_processor_brand)
    df_processed['processor_series'] = df_processed['processor'].apply(extract_processor_series)
    df_processed['processor_gen'] = df_processed['processor'].apply(extract_generation)

    # Extract brand
    df_processed['brand'] = df_processed['name'].apply(extract_brand)

    # Process storage type
    df_processed['storage_type'] = df_processed['storage'].apply(extract_storage_type)

    # Process display size
    df_processed['display_size'] = df_processed['display(in inch)'].apply(extract_display_size)

    # Fill missing values
    df_processed['processor_gen'] = df_processed['processor_gen'].fillna(-1)
    df_processed['processor_gen'] = df_processed['processor_gen'].astype(int)

    median_storage = df_processed['storage_gb'].median()
    df_processed['storage_gb'] = df_processed['storage_gb'].fillna(median_storage)
    df_processed['storage_gb'] = df_processed['storage_gb'].astype(int)

    median_display = df_processed['display_size'].median()
    df_processed['display_size'] = df_processed['display_size'].fillna(median_display)

    # Binary rating feature
    df_processed['has_rating'] = (df_processed['rating'] > 0).astype(int)

    # Select final columns
    final_columns = [
        'brand', 'price(in Rs.)', 'rating', 'no_of_ratings', 'no_of_reviews',
        'processor_brand', 'processor_series', 'processor_gen',
        'ram_gb', 'storage_gb', 'storage_type', 'os_simplified', 'display_size',
        'has_rating'
    ]

    df_final = df_processed[final_columns].copy()
    df_final = df_final.rename(columns={'os_simplified': 'os'})

    df_final = fix_outliers(df_final)

    print(f"\nFinal size: {df_final.shape}")
    print(f"Missing values: {df_final.isna().sum().sum()}")

    return df_final
