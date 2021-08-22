let activePreviewId;

const openPreview = (docType, docId) => {
    window.open(getBaseUrl() + `preview-deprecated/${docType}/${docId}`);
}

const showPreview = function()  {
    let docId = parseInt(($(this).attr('doc-id')))
    if (previewsMap.has(docId)) {
        if (!existing_preview.has(docId) && id_to_preview_type.has(docId)){

            if (id_to_preview_type.get(docId) == 'embed'){
                openPreview(id_to_preview_type.get(docId), docId)
            }

            if (id_to_preview_type.get(docId) == 'image'){
                openPreview(id_to_preview_type.get(docId), docId)
            }

            if (id_to_preview_type.get(docId) == 'excel'){
                openPreview(id_to_preview_type.get(docId), docId)
            }

            if (id_to_preview_type.get(docId) == 'clear_pdf'){
                openPreview(id_to_preview_type.get(docId), docId)
            }
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
        url: getBaseUrl() + 'load_docs_info/'+window.location.search,
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