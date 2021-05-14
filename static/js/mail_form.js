$(function() {
    if (!window.Quill) {
        return $('#quill-editor,#quill-toolbar').remove();
    }

    const editor = new Quill('#quill-editor', {
        modules: {
            toolbar: '#quill-toolbar'
        },
        placeholder: 'Type something',
        theme: 'snow'
    });


    function toBase64(file) {
        return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve({base64: reader.result, filename: file.name});
        reader.onerror = error => reject(error);
        });
    };

    async function tobase64Handler(files) {
        const filePathsPromises = [];
        Array.from(files).forEach(file => {
        filePathsPromises.push(toBase64(file));
        });
        const filePaths = await Promise.all(filePathsPromises);
        const mappedFiles = filePaths.map((item) => ({ "name":"files[]", "value": item.base64, "filename": item.filename }));
        return mappedFiles;
    }

    const form2 = document.getElementById('mailing-form');

    if(form2) {
        form2.onsubmit = async function(e) {
            e.preventDefault();
            const content = document.querySelector('input[name=content]');
            content.value = $('div.ql-editor').html();
            const files = await tobase64Handler($('input[name="files[]"]')[0].files);
            const data = JSON.stringify({data: [...$(form2).serializeArray(), ...files]});
            const url = $(form2).attr('action');
            console.log("Submitted", data, {data: [...$(form2).serializeArray(), ...files]}, $(form2).serialize());
            $.post(url, data, function(){},'json')
            .done(function(result){
                if(result.meta && result.meta.error === 201){
                    document.location.assign(result.link);
                } else {
                    let message = result.meta.messages.join(' ');
                    $('#modal-error .modal-body').html(message);
                    $('#modal-error').modal('show');
                }
            })
            .fail(()=>{
                $('#modal-error .modal-body').html('<div>Ошибка выполнения запроса. Обратитесь к администратору</div>');
                $('#modal-error').modal('show');
            });
            return false;
        };
    }


    const okText = "Ок";
    const clearText = "Очистить";
    const nowText = "Сейчас";
    const cancelText = "Отменить";

    $('#b-m-dtp-date').bootstrapMaterialDatePicker({
        weekStart: 1,
        time: false,
        format: 'DD.MM.YYYY',
        okText: okText,
        clearText: clearText,
        nowText: nowText,
        cancelText: cancelText,
        lang: 'ru',
        clearButton: true
    });

    $('#b-m-dtp-datetime').bootstrapMaterialDatePicker({
        weekStart: 1,
        format : 'DD MMMM YYYY - HH:mm',
        shortTime: true,
        nowButton : true,
        okText: okText,
        clearText: clearText,
        nowText: nowText,
        cancelText: cancelText,
        lang: 'ru',
        minDate : new Date()
    });

    $('#b-m-dtp-time').bootstrapMaterialDatePicker({
        date: false,
        shortTime: false,
        okText: okText,
        clearText: clearText,
        nowText: nowText,
        cancelText: cancelText,
        lang: 'ru',
        format: 'HH:mm'
    });

    $('.select2').each(function() {
        $(this)
            .wrap('<div class="position-relative"></div>')
            .select2({
                placeholder: 'Выберите значение',
                dropdownParent: $(this).parent()
            });
    });
    $('select[data-bs-ms="multiple"]').each(function() {
        $(this)
        .multiselect({
            enableClickableOptGroups: true,
            enableCollapsibleOptGroups: true,
            collapseOptGroupsByDefault: false,
            enableFiltering: true,
            includeSelectAllOption: true,
            buttonWidth: '100%',
            maxHeight: 400,
            dropUp: true,
            selectAllText: $(this).data('bs-ms-alltext') || "Выбрать все",
            allSelectedText: "Все выбраны",
            nonSelectedText: "Выберите значения",
            nSelectedText: " выбраны",
            filterPlaceholder: "Поиск",
            templates: {
              filter: '<li class="multiselect-item filter"><div class="input-group input-group-sm"><span class="input-group-prepend"><span class="input-group-text"><i class="ion ion-ios-search"></i></span></span><input class="form-control multiselect-search" type="text" placeholder="Поиск"></div></li>',
              filterClearBtn: '<span class="input-group-append"><button class="btn btn-default multiselect-clear-filter" type="button"><i class="ion ion-md-close"></i></button></span>',
            }
          });
    });

});