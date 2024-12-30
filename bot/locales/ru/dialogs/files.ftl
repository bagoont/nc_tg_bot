files-scrollgroup =
    <blockquote>{ $symbol } { $title }</blockquote>

    <b>🔍 Имя { $type ->
        [dir] Папки
        *[file] Файла
    }:</b> 
    { $name }

    <b>📂 Директория:</b>
    { $user_path }

    <b>Владелец { $type ->
        [dir] Папки
        *[file] Файла
    }:</b>
    { $user }

    <b>🗃️ Размер { $type ->
        [dir] Папки
        *[file] Файла
    }:</b>
    { $size }

    <b>🌐 URL:</b>
    { $url }

    <b>⏱️ Изменено:</b>
    { $last_modified }