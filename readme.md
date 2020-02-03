## Text search PSQL (Trigram) vs ES ##

Comparison how much faster Elasticsearch actually is than full text search in relational db.

### Installation ###

* run with `docker-compose up -d`
* populate with random data using function `populate_articles(count)` (`from app.populate import populate_articles`)
* PSQL search: http://0.0.0.0:8000/search/psql/?q={phrase}
* ES search: http://0.0.0.0:8000/search/es/?q={phrase}