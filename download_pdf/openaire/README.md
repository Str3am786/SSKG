# OpenAire API

<https://explore.openaire.eu/search/organization?organizationId=openorgs____::cad284878801b9465fa51a95b1d779db>

Waiting for openaire response about how to query organizations

Possible alternative:

- first query funding/projects
- then query projects for publications
- then query publications for software

## API Link

<https://graph.openaire.eu/develop/api.html#rproducts>

___

### Example UPM

UPM_id = `openorgs____::cad284878801b9465fa51a95b1d779db`

Query for projects = `https://api.openaire.eu/search/projects?openaireParticipantID=openorgs____::cad284878801b9465fa51a95b1d779db`

Query for publications in projects = `https://api.openaire.eu/search/publications?openaireProjectID=corda_______::f9547005c58091aa24543f99884da7fb`

Query for software in projects = `https://api.openaire.eu/search/software?openaireProjectID=corda_______::f9547005c58091aa24543f99884da7fb`
