# Zenodo API

Documentation for **Zenodo** [link](https://developers.zenodo.org/#rest-api)

## Basic Usage

The Zenodo REST API currently supports:

Deposit — upload and publishing of research outputs (identical to functionality available in the user interface).
Records — search published records.
Files — download/upload of files.

We are going to use the Records endpoint.
`https://zenodo.org/api/records/`

Which we can query using `?q=<your_query>`

Here we will filter by 2 types:

- `&type=publication`
- `&type=software`

## Paging

Paging in Zenodo is as simple as saying how much you want per page, and the number of the page. If no size 10 is default.

- `size=1000` it means 1k results per page
- `page=2` it means results from page 2

If you have more than one page to look, you can use the next link that comes with the response.
___

## UPM example

Basic link for exploring UPM in OpenAlex is <https://zenodo.org/api/records/?q=UPM&type=publication&size=1000>
