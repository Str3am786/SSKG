# Github API

Documentation for **Github** [link](https://docs.github.com/en/rest/search#about-the-search-api)

## Repositories

Find repositories via various criteria. This method returns up to 100 results per page.

When searching for repositories, you can get text match metadata for the name and description fields when you pass the text-match media type. For more details about how to receive highlighted search results, see [Searching for repositories](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)

- Basic example: `https://api.github.com/search/repositories?q=<your_search>`

## Basic pagination

Requests that return multiple items will be paginated to 30 items by default. You can specify further pages with the `page` parameter. For some resources, you can also set a custom page size up to 100 with the `per_page` parameter. Note that for technical reasons not all endpoints respect the `per_page` parameter, see events for example.

- Basic example: `https://api.github.com/search/repositories?q=<your_search>&per_page=<1..100>&page=<your_page>`

___

## UPM example

Basic query for exploring UPM in Github is: `https://api.github.com/search/repositories?q=Universidad%20politecnica%20de%20madrid+in:name,description,readme`

What is the query doing?

- The firts part refers to repositories: `https://api.github.com/search/repositories?`
- This second part looks for "Universidad politecnica de madrid" : `q=Universidad%20politecnica%20de%20madrid`
- The last part says where to look for the previos part, in this case we look at name,description, and readme : `+in:name,description,readme`
