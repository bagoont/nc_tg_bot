### Text messages related to authorization in Nextcloud.

## Authentication in Nextcloud.
auth-init =
    To authorize, you need to follow the link below and grant the bot access to your account. 👇

    { $url }

    Unfortunately, time is limited and you only have <b>{ $timeout } minutes</b> to complete the authorization process. 🕐
auth-timeout =
    The waiting time has exceeded { $timeout } minutes. 🐢

    Send /auth to retry.
auth-success = ✨ <i>Authorization successful.</i> ✨
auth-welcome =
    Welcome. 🎉

    Press { fsnode-menu-button } to go to the file menu.
    Press { search-button } to search for a file by name.
    Press { trashbin-button } to manage the trash bin.

## Logout from Nextcloud.
logout =
    Are you sure you want to log out? <b>This action cannot be undone.</b> 😦

    Logging out will result in losing access to the bot's functionality, including file management on Nextcloud. If you decide to return, you will need to reauthorize.
logout-confirm =
    You have successfully logged out. 🚪

    To use the bot again, <b>send the command /auth to start the authorization process again.</b>
logout-cancel =
    Logout canceled. 🥳

    You remain logged in. If you wish to continue working, simply use the available commands.
