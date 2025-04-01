from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def extract_hyperlinks(html_content):
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')
    return anchor_tags

def calculate_null_self_redirect_hyperlinks_percentage(anchor_tags):
    total_hyperlinks = len(anchor_tags)
    null_or_self_redirect_count = 0
    
    for tag in anchor_tags:
        href = tag.get('href')
        if href is None or href.strip() == '' or href.strip() == '#':
            null_or_self_redirect_count += 1
    
    if total_hyperlinks > 0:
        percentage = (null_or_self_redirect_count / total_hyperlinks)
    else:
        percentage = 0
    
    return percentage

def retrieve_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_features_from_url(url):
    parsed_url = urlparse(url)
    text=retrieve_webpage(url)
    a=extract_hyperlinks(text)
    hyper=calculate_null_self_redirect_hyperlinks_percentage(a)
    features = {
        'NumDots': url.count('.'),
        'SubdomainLevel': len(parsed_url.netloc.split('.')) - 1,
        'PathLevel': len(parsed_url.path.split('/')) - 1,
        'UrlLength': len(url),
        'NumDash': url.count('-'),
        'NumDashInHostname': parsed_url.netloc.count('-'),
        'AtSymbol': '@' in parsed_url.netloc,
        'TildeSymbol': '~' in url,
        'NumUnderscore': url.count('_'),
        'NumPercent': url.count('%'),
        'NumQueryComponents': len(parsed_url.query.split('&')),
        'NumAmpersand': url.count('&'),
        'NumHash': url.count('#'),
        'NumNumericChars': sum(c.isdigit() for c in url),
        'NoHttps': 1 if parsed_url.scheme != 'https' else 0,
        'RandomString': 1 if len(parsed_url.query) > 0 and '=' not in parsed_url.query else 0,
        'IpAddress': 1 if parsed_url.netloc.replace('.', '').isdigit() else 0,
        'DomainInSubdomains': parsed_url.netloc.count('.') > 1,
        'DomainInPaths': parsed_url.netloc in parsed_url.path,
        'HttpsInHostname': 'https' in parsed_url.netloc,
        'HostnameLength': len(parsed_url.netloc),
        'PathLength': len(parsed_url.path),
        'QueryLength': len(parsed_url.query),
        'DoubleSlashInPath': '//' in parsed_url.path,
        'PctNullSelfRedirectHyperlinks':hyper
    }

    return features
