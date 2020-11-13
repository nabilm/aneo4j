
# aneo4j

A work in progress !
based on my gist [gist](https://gist.github.com/nabilm/beb31e960c099d59297c0ef0cfbac55a)
aneo4j is a really simple async wrapper for neo4j since all the async wrapper/client is all out of date and the async bolt support is not ready yet



* Free software: GNU General Public License v3
* Documentation: https://aneo4j.readthedocs.io. (in progress)


Usage
-----

```python
import asyncio
loop = asyncio.get_event_loop()
config = {'user': 'neo4j' , 'password' : 'test' , 'uri' : 'bolt://localhost:7687'}
an = AsyncNeo4j(config=config, loop=loop)
# And of course it require python3.7 and neo4j
# Now you should easily create queries with dynamic variables like
CREATE (h:human { name: $name, 
                    user_name: $user_name, 
                    human_id: $human_id, 
                    city: $city, 
                    country: $country, 
                    email: $email,
                    birhdate: date($birthdate)
                    })
                    RETURN ID(h) as id
# The client deals with kwargs
```
Features
--------

* Neo4j write and read transaction functions support
* Dynamic queries ( using $ in the query template )
