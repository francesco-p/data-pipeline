# How to run

First build the project with `docker-compose build`
Be sure to first run  `docker-compose up storage` and `docker-compose up storage` when the startup procedure ends then run `docker-compose up app`

You can watch this ascii cast to check my run https://asciinema.org/a/HNqeOaPBgVTDGpCWmi82bF3md

# Considerations

I used a pre-built tool to scrape instagram to save time since a proper scraper needs time to be written. As a matter of fact you can check a scraper I wrote some months ago for a kaggle challenge https://github.com/francesco-p/xeno-canto-scraper

There are some choices I made to quickly solve the assignment, for example the fact that we do not insert rows incrementally through a schema in the database or we have little error handling procedures (mostly in subprocesses).

