$(document).ready(function () {
    initialize_event_handler();
});

function initialize_event_handler() {
    delete_guide();
}

function delete_guide(){
    $(document).on('click', 'button[name="delete_guide"]', function () {
        let isDelete = window.confirm("本当にこのガイドを削除してよろしいですか");
        if (isDelete) {
            document.delete_guide_form.target = "_self";
            document.delete_guide_form.method = "post";
            document.delete_guide_form.action = "/guide/delete/";
            document.delete_guide_form.submit();
        }
    });
}
