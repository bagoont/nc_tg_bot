### Text messages and menu buttons for managing the trash bin.

## Trash bin.
trashbin =
    There
    { $count ->
        [one] is <b>{ $count }</b> file
        [few] are <b>{ $count }</b> files
        *[other] are <b>{ $count }</b> files
    } in the trash bin.
    The trash bin takes <b>{ $size }</b>.
trashbin-item = 🔹 <i>{ $path }</i>
trashbin-empty = The trash bin is empty.

## Cleanup.
trashbin-cleanup-button = Cleanup
trashbin-cleanup-start = Are you sure you want to empty the trash bin?

## Actions with a file inside the trash bin.
trashbin-fsnode = Choose an action
trashbin-delete-button = ❌ Delete
trashbin-restore-button = 🔃 Restore
trashbin-delete-alert = File deleted
trashbin-restore-alert = File restored
