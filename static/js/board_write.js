var doubleSubmitFlag = false;

function doubleSubmitCheck(){
    if(doubleSubmitFlag){
        return doubleSubmitFlag;
    }else{
        doubleSubmitFlag = true;
        return false;
    }
}

function insert(){
    var result = confirm('등록하시겠습니까?');
    if(result) {
        if(doubleSubmitCheck()) return;
    }else{
        return false;
    }
}
$(function(){
    $('#id_post_title').keyup(function (e){
        var content = $(this).val();
        $('.counter').html("("+content.length+" / 최대 40)");    //글자수 실시간 카운팅

        if (content.length > 40){
            alert("최대 40자까지 입력 가능합니다.");
            $(this).val(content.substring(0, 40)); // 최대 글자 수 설정
            $('.counter').html("(40 / 최대 40자)");
        }
    });

    $('#cancel').click(function() { //사진 올리고 취소 누를시 유저가 올린 이미지 삭제
        if(confirm('작성을 취소하시겠습니까?') == true){
            history.back()
            var iframe_code = document.getElementById('id_post_content_iframe').contentWindow.document.body.innerHTML;

            $.ajax({
                url:'api/check-img/?',
                type:'POST',
                data: {
                    'code': iframe_code,
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                },
                dataType: 'html'
                ,
                success:function(response){
                    if(response.data == 'exist'){
                        return;
                    }
                    else{
                        return;
                    }
                },
                error : function(xhr, error){
                    console.error("error : " + error);
                }
            });
        }else{
            return False;
        }
    });
})