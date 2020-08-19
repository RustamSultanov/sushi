let activePreviewId;

const showPreview = function()  {
    let docId = parseInt(($(this).attr('doc-id')))
    if (previewsMap.has(docId)) {
        if (activePreviewId !== undefined){
            $(prKeySh(activePreviewId)).hide()
            activePreviewId = docId
            $('#show-preview-button').show()
        }
        if (!existing_preview.has(docId) && id_to_preview_type.has(docId)){

            if (id_to_preview_type.get(docId) == 'embed'){
                let element_template =  `<embed class="preview-internal" id="${prKey(docId)}" src="${previewsMap.get(docId)}" type="application/pdf">`
                $(".preview-content").append(element_template);
                existing_preview.add(docId)
            }

            if (id_to_preview_type.get(docId) == 'image'){
                let element_template =  `<img class="preview-img" id="${prKey(docId)}" src="${previewsMap.get(docId)}">`
                existing_preview.add(docId)
                $(".preview-content").append(element_template);
            }

            if (id_to_preview_type.get(docId) == 'excel'){
                let element_template = `<div id="${prKey(docId)}" class="table-wrapper table-responsive"></div>`
                existing_preview.add(docId)
                
                //устанавливаем bootstrap стили в таблицу загруженную через api
                $(".preview-content").append(element_template);
                $(prKeySh(docId)).load('/load_excel/'+ docId, function(){
                    $('table').attr('class', 'table')
                    $('table thead th').attr('scope', 'col')
                    $('table tbody tr th').attr('scope', 'row')
                })
            }

            if (id_to_preview_type.get(docId) == 'clear_pdf'){
                let element_template = `<embed class="preview-internal" id="${prKey(docId)}" src="/load_pdf_stream_preview/${docId}" type="application/pdf">`
                existing_preview.add(docId)
                $(".preview-content").append(element_template);
            }
            activePreviewId = docId
            $('#show-preview-button').show()
        } else {
            activePreviewId = docId
            $(prKeySh(activePreviewId)).show()
        }
    }  
}


const timerDelay = 150
let currentToken = 'token'

//отображение id доков в url
let previewsMap = new Map()

//множество скрытых контейнеров с превью
let existing_preview = new Set()
let id_to_preview_type = new Map()

const prKey = (docId) => "prw-" + docId
const prKeySh = (docId) => "#prw-" + docId
const getBaseUrl = () => new URL(document.URL).origin + '/'


const loadDocInfo = function(ids) {
    const final = (response) => {
        for(let key in response.docs_id_to_url)
            previewsMap.set(parseInt(key), response.docs_id_to_url[key])

        for(let key in response.id_to_preview_type)
            id_to_preview_type.set(parseInt(key), response.id_to_preview_type[key])
        
        $(".project-attachment-img").click(showPreview)
    }
    $.ajax({
        type: 'POST',
        url: getBaseUrl() + 'load_docs_info/',
        dataType: 'json',
        data: JSON.stringify(ids),
        success: final
    })
}


const bindPreviewEvents = function() {
    if($("#refresh-container").length){

        let token = $("#refresh-container").attr('refresh-token')
        if (token === currentToken)
            setTimeout(bindPreviewEvents, timerDelay)
        else {
            let ids = []
            $(".project-attachment-img")
            .each(function(){ 
                ids.push($(this).attr('doc-id'))
            })
            loadDocInfo(ids)
            currentToken = token 
        }
    }
    else 
        setTimeout(bindPreviewEvents, timerDelay)
}

bindPreviewEvents()