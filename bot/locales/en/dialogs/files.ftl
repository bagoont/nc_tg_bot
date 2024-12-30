files-scrollgroup = 
    <blockquote>{ $symbol } { $title }</blockquote>

    <b>🔍 { $type ->
        [dir] Folder
        *[file] File
    } Name:</b> 
    { $name }

    <b>📂 Directory:</b>
    { $user_path }

    <b>{ $type ->
        [dir] Folder
        *[file] File
    } Owner:</b>
    { $user }

    <b>🗃️ { $type ->
        [dir] Folder
        *[file] File
    } Size:</b>
    { $size }

    <b>🌐 URL:</b>
    { $url }

    <b>⏱️ Last Modififed:</b>
    { $last_modified }

files-multidownload =
    <i>Select files from <b>{ $user_path }</b>. 
    
    Click Download once you're done.</i>