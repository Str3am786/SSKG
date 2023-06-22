import json

def load_data(path):
    with open(path) as f:
        return json.load(f)

def extract_urls(data):
    urls = []
    for item in data:
        urls.append(item['html_url'])
    return urls

def save_urls(urls, path):
    with open(path, 'w') as f:
        json.dump(urls, f, indent=4)
    
    return len(urls)

def main():
    data = load_data('apis/github/repos.json')
    urls = extract_urls(data)
    count = save_urls(urls, 'apis/github/github_urls.json')
    print('Saved {} urls'.format(count))

if __name__ == '__main__':
    main()