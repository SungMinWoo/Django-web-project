function post_like(id) {
    $.ajax({
        url: id+"/post_likes/?", // data를 전송할 url 입니다.
        data: {
            'review_id': id
        },
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            if(response.result == 'success'){
                $('.'+id).filter('#like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
                $('.'+id).filter('#dislike_count').html(response.dislike_count)
            }else if(response.result == 'login'){
                alert('로그인이 필요한 서비스입니다.');
            }else if(response.result == 'fail'){
                alert("권한이 존재하지 않습니다.");
            }
        },
        login : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    })
}

function reply_like(id) {
    $.ajax({
        url: id+"/reply_likes/?", // data를 전송할 url 입니다.
        data: {
            'review_id': id
        },
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            if(response.result == 'success'){
                $('.'+id).filter('#reply_like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
                $('.'+id).filter('#reply_dislike_count').html(response.dislike_count)
                $('.'+id).filter('#message').html(response.message) //id가 message의 내용을 전송받은 message로 바꾼다
            }else if(response.result == 'login'){
                alert('로그인이 필요한 서비스입니다.');
            }else if(response.result == 'fail'){
                alert("권한이 존재하지 않습니다.");
            }
        },
        login : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    })
}

function post_dislike(id) {
    $.ajax({
        url: id+"/post_dislikes/?", // data를 전송할 url 입니다.
        data: {
            'review_ids': id
        }, // post_id 라는 name으로 id 값 전송
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            if(response.result == 'success'){
                $('.'+id).filter('#like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
                $('.'+id).filter('#dislike_count').html(response.dislike_count)
            }else if(response.result == 'login'){
                alert('로그인이 필요한 서비스입니다.');
            }else if(response.result == 'fail'){
                alert("권한이 존재하지 않습니다.");
            }
        },
        error : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    })
}

function reply_dislike(id) {
    $.ajax({
        url: id+"/reply_dislikes/?", // data를 전송할 url 입니다.
        data: {
            'review_ids': id
        }, // post_id 라는 name으로 id 값 전송
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            if(response.result == 'success'){
                $('.'+id).filter('#reply_like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
                $('.'+id).filter('#reply_dislike_count').html(response.dislike_count)
            }else if(response.result == 'login'){
                alert('로그인이 필요한 서비스입니다.');
            }else if(response.result == 'fail'){
                alert("권한이 존재하지 않습니다.");
            }
        },
        error : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    })
}


function re_reply_like(id) {
    $.ajax({
        url: id+"/reply_likes/?", // data를 전송할 url 입니다.
        data: {
            'review_id': id
        },
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            if(response.result == 'success'){
                $('.'+id).filter('#re_reply_like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
                $('.'+id).filter('#re_reply_dislike_count').html(response.dislike_count)
                $('.'+id).filter('#message').html(response.message) //id가 message의 내용을 전송받은 message로 바꾼다
            }else if(response.result == 'login'){
                alert('로그인이 필요한 서비스입니다.');
            }else if(response.result == 'fail'){
                alert("권한이 존재하지 않습니다.");
            }
        },
        login : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    })
}

function re_reply_dislike(id) {
    $.ajax({
        url: id+"/reply_dislikes/?", // data를 전송할 url 입니다.
        data: {
            'review_ids': id
        }, // post_id 라는 name으로 id 값 전송
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            if(response.result == 'success'){
                $('.'+id).filter('#re_reply_like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
                $('.'+id).filter('#re_reply_dislike_count').html(response.dislike_count)
            }else if(response.result == 'login'){
                alert('로그인이 필요한 서비스입니다.');
            }else if(response.result == 'fail'){
                alert("권한이 존재하지 않습니다.");
            }
        },
        error : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    })
}
<!--        등록 두번 클릭시-->
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
    $('#choice').on('change', function(){
        $('#choice').val($(this).val());
        $('#choiceForm').submit();
    });

    $('.delete').click(function() {
        var result = confirm('삭제하시겠습니까?');
        if(result) {
            return true;
        }else{
            return false;
        }
    });

        //       수정
    $('.update_reply').click(function(){
        var value = $(this).attr('name');
        var content = $('[name='+value+']').filter('.reply_contents').text();
        if($('[name='+value+']').filter('#update_reply_form').css('display') == 'none'){ // 두번 클릭시 다시 사라짐
            $('[name='+value+']').filter('#update_reply_form').css('display', '');
            $('[name='+value+']').filter('.form-control').val(content);
        }else{
            $('[name='+value+']').filter('#update_reply_form').css('display', 'none');;
        }
    });

    $('.update_re_reply').click(function(){
        var value = $(this).attr('name');
        var content = $('[name='+value+']').filter('.reply_contents').text();
        if($('[name='+value+']').filter('#update_re_reply_form').css('display') == 'none'){ // 두번 클릭시 다시 사라짐
            $('[name='+value+']').filter('#update_re_reply_form').css('display', '');
            $('[name='+value+']').filter('.form-control').val(content);
        }else{
            $('[name='+value+']').filter('#update_re_reply_form').css('display', 'none');;
        }
    });

        //        글자수 새기
    $('.form-control').keyup(function (e){
        var content = $(this).val();
        var id = $(this).attr('title');

        $('.counter').filter('[title='+id+']').html("("+content.length+" / 최대 300)");    //글자수 실시간 카운팅

        if (content.length > 300){
            alert("최대 300자까지 입력 가능합니다.");
            $(this).val(content.substring(0, 300)); // 최대 글자 수 설정
            $('.counter').html("(300 / 최대 300자)");
        }
    });

})