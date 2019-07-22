$(function() {

    if (!window.Quill) {
        return $('#quill-editor,#quill-toolbar').remove();
    }

    var editor = new Quill('#quill-editor', {
        modules: {
            toolbar: '#quill-toolbar'
        },
        placeholder: 'Type something',
        theme: 'snow'
    });


    var form = document.querySelector('form');
    form.onsubmit = function() {
        // Populate hidden form on submit
        var body = document.querySelector('input[name=body]');
        var content = document.querySelector('input[name=content]');
        body.value = $('div.ql-editor').html();
        content.value = $('div.ql-editor').html();
    };


    $('input[wtype="date"]').bootstrapMaterialDatePicker({
        time: false,
        format : 'DD.MM.YYYY',
        nowButton : true,
        lang: 'ru',
        minDate : new Date(),
    });
});