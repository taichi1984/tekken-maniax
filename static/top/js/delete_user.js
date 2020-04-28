$(document).ready(function () {
    initialize_event_handler();
});

function initialize_event_handler() {
    delete_user();
}

function delete_user(){
    $(document).on('click', 'button[name="delete_account_button"]', function () {
        let isDelete = window.confirm("本当にアカウントを削除してよろしいですか\n " +
            "この操作は取り消すことができません\n");

        if (isDelete) {
            document.delete_account_form.target = "_self";
            document.delete_account_form.method = "post";
            document.delete_account_form.action = "/account_manager/delete_account/";
            document.delete_account_form.submit();
        }
    });
}
