$(document).on('click', '.add-dir', function(){
  $('.add-directory-panel').attr('style', 'display:block');
  $('.add-file-panel').attr('style', 'display:none');
});
$(document).on('click', '.add-dir-file', function(){
  $('.add-directory-panel').attr('style', 'display:none');
  $('.add-file-panel').attr('style', 'display:block');
});
$(document).on('click', '.modal-close', function(){
  $('.add-directory-panel').attr('style', 'display:none');
  $('.add-file-panel').attr('style', 'display:none');
})
$(document).on('click', '.complete-add-dir', function(){
  let $parent_id = $('#main_node').val();
  let $title = $('#directory-name').val();
  let $data = {'PARENT_ID': $parent_id, 'TITLE': $title};
  $.ajax({
	method: 'post',
	url: '/add-directory',
	data: $data,
	dataType: 'json',
	success: function(data){
		if(data.success){
			let $html_append = '';
			if(data.is_manager){
				$html_append = '<div class="dir"><div class="dir-info"><img class="dir-ico" src="/static/images/code.svg" width="25px" height="25px">'+data.dir_title+'<input class="node_id" hidden value='+data.dir_id+' ></div></div>';
			} else{
				$html_append = '<div class="dir"><div class="dir-info"><img class="dir-ico" src="/static/images/code.svg" width="25px" height="25px">'+data.dir_title+'<input class="node_id" hidden value='+data.dir_id+' ></div><div class="delete-dir">x</div></div>';
			};
			if($('.dir').length == 0){
				if($('.dir-file').length == 0){
					$('.dir-buttons').before($html_append)
				} else {
					$('.dir-file').before($html_append)
				};
			} else {
				$($html_append).insertAfter($('.dir').last());
			}
			$('.add-directory-panel').attr('style', 'display:none');
			$('#directory-name').val("");
		};
	},
  });
})
$(document).on('click', '.complete-file-add', function(){
  let $data = new FormData();
  $data.append('PARENT_ID', $('#main_node').val());
  $data.append('file', $('#directory-file')[0].files[0]);
  console.log($data);
  $.ajax({
        method: 'post',
        url: '/add-directory-file',
	contentType: false,
	processData: false,
        data: $data,
        dataType: 'json',
        success: function(data){
                if(data.success){
			let $html_append = '';
                        if(data.is_manager){
                                $html_append = '<div class="dir-file"><img class="file-ico" src="/static/images/fileico.svg" width="15px" height="15px"><a href="'+data.dir_file_url+'">'+data.dir_file_name+'</a><input hidden class="dir-file-id" value='+data.dir_file_id+'></div>';
                        } else{
                                $html_append = '<div class="dir-file"><img class="file-ico" src="/static/images/fileico.svg" width="15px" height="15px"><a href="'+data.dir_file_url+'">'+data.dir_file_name+'</a><span class="delete-dir-file">x</span><input hidden class="dir-file-id" value='+data.dir_file_id+'></div>';
                        };
                        $('.dir-buttons').before($html_append);
			$('.add-file-panel').attr('style', 'display:none');
			$('#directory-file').val('');
                };
        },
  });
})
$(document).on('click', '.dir-info', function(){
  let $parent_id = $(this).find('.node_id').val();
  let $data = {'PARENT_ID': $parent_id};
  $.ajax({
        method: 'post',
        url: '/show-directories',
        data: $data,
        dataType: 'json',
        success: function(data){
                if(data.success){
                        $('#directories').html(data.response);
                };
        },
  });
})
$(document).on('click', '.delete-dir', function(){
  let $parent_id = $(this).siblings('.dir-info').find('.node_id').val();
  let $data = {'DIR_ID': $parent_id};
  let $this = $(this);
  //$(this).parent('.dir').remove();
  $.ajax({
        method: 'post',
        url: '/delete-directory',
        data: $data,
        dataType: 'json',
        success: function(data){
                if(data.success){
                        $this.parent('.dir').remove();
                };
        },
  });
})
$(document).on('click', '.delete-dir-file', function(){
  let $parent_id = $(this).siblings('.dir-file-id').val();
  let $data = {'FILE_ID': $parent_id};
  let $this = $(this);
  //$(this).parent('.dir').remove();
  $.ajax({
        method: 'post',
        url: '/delete-directory-file',
        data: $data,
        dataType: 'json',
        success: function(data){
                if(data.success){
                        $this.parent('.dir-file').remove();
                };
        },
  });
})
