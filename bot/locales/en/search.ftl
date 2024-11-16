### File search text messages.

## Searching files.
search-enter = Enter part of the name of the file you are looking for or the full name to start searching. 🐕‍🦺
search =
    Found { $count ->
            [one] <b>{ $count }</b> match.
            *[other] <b>{ $count }</b> matches.
        }

    Search results for query "<b>{ $query }</b>":
search-item = 🔹 <i>{ $path }</i>
search-empty = Unfortunately, no files were found with such a name. 😶
