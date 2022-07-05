function review_like(id) {
    console.log("hi")
    $.ajax({
        url: "like/?", // data를 전송할 url 입니다.
        data: {
            'review_id': id
        }, // post_id 라는 name으로 id 값 전송
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            $('.'+id).filter('#like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
            $('.'+id).filter('#dislike_count').html(response.dislike_count)
            $('.'+id).filter('#message').html(response.message) //id가 message의 내용을 전송받은 message로 바꾼다
            $('.'+id).filter('#toast').fadeIn(400).delay(100).fadeOut(400) //class가 toast인 것을 서서히 나타나게 하는 메서드입니다.
        }
    })
}

function review_dislike(id) {
    console.log("hi")
    $.ajax({
        url: "dislike/?", // data를 전송할 url 입니다.
        data: {
            'review_ids': id
        }, // post_id 라는 name으로 id 값 전송
        dataType: "json",
        success: function (response) { // ajax 통신이 정상적으로 완료되었을 때
            $('.'+id).filter('#like_count').html(response.like_count) //id가 like_count의 내용을 전송받은 좋아요 수로 바꾼다
            $('.'+id).filter('#dislike_count').html(response.dislike_count)
            $('.'+id).filter('#message').html(response.message)
            $('.'+id).filter('#toast').fadeIn(400).delay(100).fadeOut(400)
        }
    })
}


$(function(){
    var politic_nm = $('#politic_name').text();

    var data = {
        'politic_nm': politic_nm,
    };
    $.ajax({
        url:'api/check-value/?',
        type:'get',
        data: JSON.stringify(data)
        ,
        success:function(response){
            if(response.data == 'exist'){
                $('#rate_button').attr('disabled', true);
                return;
            }
            else{
                $('#rate_button').attr('disabled', false);
                return;
            }
        },
        error : function(xhr, error){
            alert("서버와의 통신에서 문제가 발생했습니다.");
            console.error("error : " + error);
        }
    });

    $('#choice').on('change', function(){
        $('#choice').val($(this).val());
        $('#choiceForm').submit();
    });

//        글자수 새기
    $('#message-text').keyup(function (e){
        var content = $(this).val();
        $('#counter').html("("+content.length+" / 최대 70자)");    //글자수 실시간 카운팅

        if (content.length > 70){
            alert("최대 70자까지 입력 가능합니다.");
            $(this).val(content.substring(0, 70)); // 최대 글자 수 설정
            $('#counter').html("(70 / 최대 70자)");
        }
    });

    $('.delete').click(function() {
        var result = confirm('삭제하시겠습니까?');
        if(result) {
            return true;
        }else{
            return false;
        }
    });

    var nInitialCount = 150;
    var moretext = "더보기 >";
    var lesstext = "줄이기";
    $('#longtext').each(function() {
         var paraText = $(this).html();
         if (paraText.length > nInitialCount) {
             var sText = paraText.substr(0, nInitialCount);
             var eText = paraText.substr(nInitialCount, paraText.length - nInitialCount);
             var newHtml = sText + '<span id="comma">...</span><span class="moretext"><span>' + eText + '</span><a href="" id="links">' + moretext + '</a></span>';
             $(this).html(newHtml);
         }
    });

    $("#links").on('click', function(e) {
        var lnkHTML = $(this).html();
        if (lnkHTML == lesstext) {
            $(this).html(moretext);
            $('#comma').show();
        } else {
            $(this).html(lesstext);
            $('#comma').hide();
        }
        $(this).prev().toggle();
        e.preventDefault();
    });
})