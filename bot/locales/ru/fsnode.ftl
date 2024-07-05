### Текстовые сообщения и кнопки меню управления файлом.

## Заглавное сообщение меню управления файлом.
fsnode =
    <b><i>{ $type ->
        [dir] Папка
        *[file] Файл
    }</i> { $symbol }: { $name }</b>

    <i>{ $path }</i>
    ---
    🔸 <u><i>Владелец:</i></u> { $user }
    🔸 <u><i>В избранном:</i></u> { $favorite }
    🔸 <u><i>Размер:</i></u> { $size }
    🔸 <u><i>Последние изменения:</i></u> { $last_modified }

## Удаление файла.
fsnode-delete =
    Вы уверены, что хотите удалить файл <b>{ $name }</b>? 💣

    <b>Это действие нельзя отменить.</b>
fsnode-delete-alert = Файл "{ $name }" был успешно удален. 💀

## Новый файл.
fsnode-new = ...

fsnode-mkdir-start = Введите название папки, которую вы хотите создать. 📂
fsnode-mkdir-success = Папка <b>{ $name }</b> успешно создана. 👍
fsnode-mkdir-incorrectly = Папка не может быть так названа. 🫷

fsnode-upload-start =
    Отправьте файлы в виде документа, чтобы их загрузить. 📄

    Или нажмите "{ stop-button }", чтобы закончить загрузку.
fsnode-upload-error = Произошла ошибка при попытке загрузить файлы. 😵‍💫
fsnode-upload-success =
    Ваш файл <b>"{ $name }"</b> успешно загружен в Nextcloud.

    <i>Вы можете продолжить работу с другими файлами или завершить процесс загрузки.</i>
fsnode-upload-incorrectly = Файл должен быть в виде документа. 🙅‍♂️

## Скачаивание файла.
fsnode-url =
    Вес этого файла <b>{ $size }</b> превышает допустимый <i>{ $size_limit }</i>. 🏋️‍♂️

    Вы можете перейти по ссылке и скачать этот файл самостоятельно.

    <i><u>Ссылка на файл</u></i>: { $url }

## Кнопки меню управления файлом.
fsnode-delete-button = 🔴 Удалить
fsnode-download-button = ⬇️ Скачать
fsnode-new-button = 🆕 Создать
fsnode-upload-button = ⬆️ Загрузить
fsnode-mkdir-button = 🆕 Создать папку
fsnode-pag-back-button = ⬅️
fsnode-pag-next-button = ➡️
