# OpenAlex API

Documentation for **OpenAlex** [link](https://docs.openalex.org/api)

## Basic paging

Use the page query parameter to control which page of results you want (eg page=1, page=2, etc). By default there are 25 results per page; you can use the per-page parameter to change that to any number between 1 and 200.

- [Get the 2nd page of a list:](https://api.openalex.org/works?page=2)
`https://api.openalex.org/works?page=2`

- [Get 200 results on the second page:](https://api.openalex.org/works?page=2&per-page=200) `https://api.openalex.org/works?page=2&per-page=200`

Basic paging only works for to read the first 10,000 results of any list. If you want to see more than 10,000 results, you'll need to use cursor paging.

## Cursor paging

To use cursor paging, you request a cursor by adding the `cursor=*` parameter-value pair to your query.

- Get a cursor in order to start cursor pagination:
`https://api.openalex.org/works?filter=publication_year:2020&per-page=100&cursor=*`

The response to your query will include a next_cursor value in the response's meta object. Here's what it looks like:

```json

{
  "meta": {
    "count": 8695857,
    "db_response_time_ms": 28,
    "page": null,
    "per_page": 100,
    "next_cursor": "IlsxNjA5MzcyODAwMDAwLCAnaHR0cHM6Ly9vcGVuYWxleC5vcmcvVzI0ODg0OTk3NjQnXSI="
  },
  "results" : [
    // the first page of results
  ]
}
```

To retrieve the next page of results, copy the `meta.next_cursor` value into the cursor field of your next request.

- Get the next page of results using a cursor value:
`https://api.openalex.org/works?filter=publication_year:2020&per-page=100&cursor=IlsxNjA5MzcyODAwMDAwLCAnaHR0cHM6Ly9vcGVuYWxleC5vcmcvVzI0ODg0OTk3NjQnXSI=`

This second page of results will have a new value for `meta.next_cursor`.
___

## UPM example

Basic link for exploring UPM in OpenAlex is <https://explore.openalex.org/institutions/I88060688>
