import requests

def create_unpaywall_url(data):
    """
    data: dataframe with doi column that contains the doi url
    """
    # Get the dois_id from the doi column
    data['dois_id'] = data['doi'].str.split('org/').str[-1]
    # we are going to delete the ones that have figshare in the doi_id, due to the fact that they are not in the unpaywall api
    data = data[~data['dois_id'].str.contains('figshare')]
    # we are going to delete the ones that have zenodo in the doi_id, due to the fact that they are not in the unpaywall api
    data = data[~data['dois_id'].str.contains('zenodo')]
    # we are going to negociate pdf content with the unpaywall api
    data['unpaywall_url'] = 'https://api.unpaywall.org/v2/' \
                            + data['dois_id'] \
                            + '?email=nick.haupka@gmail.com'
    return data


def create_unpaywall_url_from_string(doi: str):
    """
    doi: doi url
    :return
    unpaywall  url (String)
    """
    if 'figshare' in doi or 'zenodo' in doi:
        return None
    url = doi.split('org/')[-1]
    unpaywall_url = 'https://api.unpaywall.org/v2/' \
                    + url \
                    + '?email=nick.haupka@gmail.com'
    return unpaywall_url


def get_unpaywall_pdf_url(data):
    pdf_url_list = []
    total_urls = len(data)
    for i in range(total_urls):
        try:

            r = requests.get(data['unpaywall_url'].iloc[i])
            pdf_url = r.json()['best_oa_location']['url_for_pdf']
            pdf_url_list.append(pdf_url)
            print(f'{i} of {total_urls} satisfied')
        except:
            print(f'{i} of {total_urls} non satisfied')
            pdf_url_list.append(None)

    data['pdf_url'] = pdf_url_list

    return data