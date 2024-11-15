### Text messages and file management menu buttons.

## The title message.
fsnode =
    <b><i>{ $type ->
        [dir] Folder
        *[file] File
    }</i> { $symbol }: { $name }</b>

    <i>{ $path }</i>
    ---
    🔸 <u><i>Owner:</i></u> { $user }
    🔸 <u><i>In favorites:</i></u> { $favorite }
    🔸 <u><i>Size:</i></u> { $size }
    🔸 <u><i>Recent changes:</i></u> { $last_modified }

## Deleting a file.
fsnode-delete =
    Are you sure you want to delete the file <b>{ $name }</b>? 💣

    <b>This action cannot be undone.</b>
fsnode-delete-alert = The file was successfully deleted. 💀

## New file.
fsnode-new = Choose how you want to create a new file inside the <b>{ $name }</b> folder. 🔨

fsnode-mkdir-start = @{ $username }, enter the name of the folder you want to create. 📂
fsnode-mkdir-success = Folder <b>{ $name }</b> successfully created. 👍
fsnode-mkdir-incorrectly = The folder cannot be named that way. 🫷

fsnode-upload-start =
    @{ $username }, send the files as a document to download them. 📄

    Or click "{stop-button}" to finish the download.
fsnode-upload-error = An error occurred while trying to upload files. 😵‍💫
fsnode-upload-success =
    Your file <b>"{$name }"</b> has been successfully uploaded to Nextcloud.

    <i>You can continue working with other files or complete the download process.</i>
fsnode-upload-incorrectly = The file must be in the form of a document. 🙅‍♂️

## Download file.
fsnode-size-limit = The weight of this file { $size } exceeds the allowed { $size_limit }. 🏋️‍♂️
fsnode-empty = The file cannot be empty. 🫗

## File management menu buttons.
fsnode-delete-button = 🔴 Delete
fsnode-download-button = ⬇️ Download
fsnode-new-button = 🆕 New
fsnode-upload-button = ⬆️ Upload
fsnode-mkdir-button = 📁 Create folder
fsnode-pag-back-button = ⬅️
fsnode-pag-next-button = ➡️
