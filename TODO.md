# bugs
* Capital letters DOI access fails
* encoding issue
* catch error when bibliography does not exist

# enhancements
* textwrap in show
* move text repr from `__str__` to normal method
* highlighting matches in find output
* show bibitem sorted alphabettically
* also read doi.org urls as doi

# features
* implement find
* sorting in show
    * default should be add order
    * cmd flags and config file option for alphabettical, chronological, etc
* PDF support
    * arxiv: download pdf automatically (make it an option not to)
    * command to add a pdf to a reference
        * maybe: `bib add file.pdf`, try to match metadata and suggest id
* `open` command with ids: open DOI in browser if present
