$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker({
        format: "dd mmm yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            clear: "Clear",
            done: "Select",
            cancel: "Cancel"
        }
    });
    $('select').formSelect();

    due_date = Date.parse('{{task.due_date}}');
    $('#due_date').datepicker("setDate", new Date($('#due_date').val()));
});