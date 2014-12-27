###############################
### Artist guide to the API ###
###############################

### Searches ###

Interacting with the API involves a more-or-less standard JSON API.

### Searching

To create a search, POST the following data to the endpoint /api/searches/

    {
        'url': 'http: //www.amazon.com',
        'title': 'The name for this search is Gary',
    }

This will return confirmation data of the following form except without extraneous spaces

    {
        "id": 1,
        "title": "this is a title",
        "url": "http: //www.google.com",
        "webpages": [],
        "created": "2014-12-27T07: 59: 36.374135Z",
        "updated": "2014-12-27T07: 59: 36.374173Z",
        "owner": null
    }

As you can see, the id, created, updated, and owner fields are automatically populated. The url
field has some ability to tolerate different formattings. Ultimagely handling these will be
the responsability of the API.

To modify or delete this search object, send a PUT or DELETE request the endpoint /api/searches/<id>/
where <id> is the id of the search. For the example above this would be

    /api/searches/1/



### Loggin in, out

Not implemented in
