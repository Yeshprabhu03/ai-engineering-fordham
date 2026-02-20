import pandas as pd
import pathlib

# Read dataframe and assess uniqueness
data_dir = pathlib.Path('data/fordham-website')
files = list(data_dir.glob('*.md'))

urls = []
file_names = []

for file in files:
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            if lines:
                urls.append(lines[0].strip())
                file_names.append(file.name)
    except:
        pass

df = pd.DataFrame({'filename': file_names, 'url': urls})

print(f"Total files read: {len(df)}")
unique_urls = df['url'].nunique()
unique_files = df['filename'].nunique()

print(f"Unique URLs: {unique_urls}")
print(f"Unique Filenames: {unique_files}")

if unique_urls < len(df):
    duplicates = df[df.duplicated(subset=['url'], keep=False)].sort_values(by='url')
    print("\nSample of duplicate URLs:")
    print(duplicates.head(10))
else:
    print("\nNo duplicate URLs found! All data is unique.")
