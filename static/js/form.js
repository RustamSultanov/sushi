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
        body.value = JSON.stringify(editor.getContents());

        console.log("Submitted", $(form).serialize(), $(form).serializeArray());

        // No back end to actually submit to!
        alert('Для production варианта нужно изменить функцию сабмита формы!')
        return false;
    };


    $('#b-m-dtp-datetime').bootstrapMaterialDatePicker({
        weekStart: 1,
        format : 'DD MMMM YYYY - HH:mm',
        shortTime: true,
        nowButton : true,
        lang: 'ru',
        minDate : new Date()
    });
});