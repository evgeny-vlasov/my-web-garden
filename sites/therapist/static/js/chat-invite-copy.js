document.addEventListener('DOMContentLoaded', function () {
    var button = document.getElementById('copyInviteButton');
    var invite = document.getElementById('inviteUrl');
    if (!button || !invite) return;

    button.addEventListener('click', function () {
        navigator.clipboard.writeText(invite.value).then(function () {
            button.textContent = 'Copied';
        }, function () {
            invite.focus();
            invite.select();
            button.textContent = 'Select and copy the link';
        });
    });
});
