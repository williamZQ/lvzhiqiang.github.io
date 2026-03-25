import csv
import json
import re

def format_author_name(name):
    name = name.strip()
    if not name:
        return ''
    if re.match(r'^[A-Z][a-z]+,?\s+[A-Z][a-z]+$', name):
        parts = name.replace(',', '').split()
        if len(parts) == 2:
            return f'{parts[1]} {parts[0]}'
    if re.match(r'^[\u4e00-\u9fff]+$', name):
        return name
    chinese_with_separator = re.match(r'^([\u4e00-\u9fff]+),?\s+([\u4e00-\u9fff]+)$', name)
    if chinese_with_separator:
        surname = chinese_with_separator.group(1)
        given_name = chinese_with_separator.group(2)
        return f'{surname} {given_name}'
    return name

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)

        publications = []
        for row in reader:
            if not row or not row[0].strip():
                continue

            raw_authors = row[0].strip().rstrip(';')
            authors_list = [format_author_name(a.strip()) for a in raw_authors.split(';') if a.strip()]
            authors = '; '.join(authors_list)

            pub = {
                'authors': authors,
                'title': row[1].strip() if len(row) > 1 else '',
                'publication': row[2].strip() if len(row) > 2 else '',
                'volume': row[3].strip() if len(row) > 3 else '',
                'number': row[4].strip() if len(row) > 4 else '',
                'pages': row[5].strip() if len(row) > 5 else '',
                'year': row[6].strip() if len(row) > 6 else '',
                'publisher': row[7].strip() if len(row) > 7 else ''
            }
            publications.append(pub)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(publications, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(publications)} publications to {json_file}")

if __name__ == '__main__':
    csv_to_json('citations.csv', 'publications.json')