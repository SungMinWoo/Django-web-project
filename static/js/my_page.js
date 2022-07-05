function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function(){
    var now = new Date();
    var csrftoken = getCookie('csrftoken');
    var year = now.getFullYear();
    var month = now.getMonth()+1;
//        달은 1더한 것부터 시작이라 +1이 되어있어야함
    var date = now.getDate();
    var hour = now.getHours();
    var min = now.getMinutes();
    var sec = now.getSeconds();
    var result_date = year+'-'+month+'-'+date+' '+hour+':'+min+':'+sec-->

//    var result_date = '2022-10-26 13:27:48';
//        result_date 테스트용
    var result_dates = new Date(result_date);

    var like_date = new Date($("#like_date").text());
    var time = (result_dates.getTime() - like_date.getTime())/(1000*60*60*24*30);
//<!--        time = 월차이 계산-->

//    if((time >= 6) == true){
    if((time <= 3) == true){
        $('#like').attr('disabled', false);
    }else{
        $('#like').attr('disabled', true);
    };
//       3개월 이상이 되면 수정 버튼 활성화
//       유저 정치성향에 체크하기
    if($('#like_info').text() == '진보'){
        $('#inlineRadio1').prop('checked', true);
        $('#inlineRadio1').attr('disabled', true);
    }else if($('#like_info').text() == '중도'){
        $('#inlineRadio2').prop('checked', true);
        $('#inlineRadio2').attr('disabled', true);
    }else if($('#like_info').text() == '보수'){
        $('#inlineRadio3').prop('checked', true);
        $('#inlineRadio3').attr('disabled', true);
    }

    $('input[type=radio][name=like]').change(function(){
        $("#fix_info_submit").attr("check_result_like", "success");
    });


//        수정 버튼 클릭시
    $('.change_value').click(function(){
        var value = $(this).attr('id');
//        버튼의 아이디값 가져오기

        if(value == 'nickname_btn'){
            $('#nickname').show();
            $('#nickname_btn').hide();
            $('#guid_nick').show();
            $('#wrong_img_nickname').show();
        }
        else if(value == 'like'){
            $('.form-check').show();
            $('#guid_like').show();
            $('#like').hide();
        }
    });



    $('.check').blur(function(){
        var value = $(this).attr('id');
        var value_location = $('#'+value).val();

        var password_reg = /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;
        var nickname_reg =  /^[a-zㄱ-ㅎ|ㅏ-ㅣ|가-힣0-9]{2,10}$/;
        var check_value = false;

        if(value_location == ''){
            return;
        }else if(value == 'nickname'){
            if(false === nickname_reg.test(value_location)){
                $("#message_nickname").html('기준에 맞지 않습니다.');
                $('#img_nickname').hide();
                $('#wrong_img_nickname').show();
                $('#input_nickname').val('').focus();
            }else{
                var msg = '닉네임';
                check_value = true;
            }
        }else if(value == 'password'){
            if(false === password_reg.test(value_location)){
                $("#message_password").html('기준에 맞지 않습니다.');
                $('#img_password').hide();
                $('#wrong_img_password').show();
                $('#password').val('').focus();
            }else{
                var msg = '패스워드';
                check_value = true;
            }
        }

        if(check_value == true){
            $.ajax({
                url:'api/check-value/',
                type:'POST',
                dataType:'json',
                data:{
                    'id': value,
                    'value': value_location,
                    'csrfmiddlewaretoken': csrftoken,
                },
                success:function(response){
                    if(response.result != 'success'){
                        console.error(response.data)
                        return;
                    }
                    if(response.data == 'exist'){
                        $('#message_'+value).show();
                        $("#message_"+value).html("이미 존재하는"+msg+"입니다.");
                        $('#'+value).val('').focus();
                        return;
                    }else if(response.data == 'pw_pass'){
                        $('#message_'+value).show();
                        $("#message_"+value).html("비밀번호가 일치합니다.");
                        $('#wrong_img_'+value).hide();
                        $('#check_'+value).show();
                        $("#fix_info_submit").attr("check_result_"+value, "success");
                        return;
                    }else if(response.data == 'pw_no_pass'){
                        $('#message_'+value).show();
                        $("#message_"+value).html("비밀번호가 일치하지않습니다.");
                        $('#'+value).val('').focus();
                        $('#wrong_img_'+value).show();
                        $('#check_'+value).hide();
                        return;
                    }else{
                        $('#message_'+value).hide();
                        $('#img_'+value).show();
                        $('#check_'+value).show();
                        $('#wrong_img_'+value).hide();
                        $("#fix_info_submit").attr("check_result_"+value, "success");
                        return;
                    }
                    // console.log(response)
                },
                error : function(xhr, error){
                    alert("서버와의 통신에서 문제가 발생했습니다.");
                    console.error("error : " + error);
                }
            })
        }
    });

    $('#password1').focus(function(){
        if($('#password').val() == ''){
            alert('이전 비밀번호를 입력해주세요.');
            $('#password1').blur();
            $('password').focus();
        }
    });

    $('#password2').focus(function(){
        if($('#password').val() == ''){
            alert('이전 비밀번호를 입력해주세요.');
            $('#password2').blur();
            $('#password').focus();
        }else if($('#password1').val() == ''){
            alert('새로운 비밀번호를 입력해주세요.');
            $('#password2').blur();
            $('#password1').focus();
        }
    });
    $('#password1').blur(function() {
        var reg = /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;
        var pw = $("#password1").val();

        if(pw == ''){
            return;
        }else if (false === reg.test(pw)) {
            $("#message_pw1").html('올바르지 않습니다. 다시 입력해주세요.');
            $('#img_password1').hide();
            $('#password1').val('').focus();
            $('#wrong_img_password1').show();
        }else if ( $('#password').val() == pw) {
            $("#message_pw1").html('이전 비밀번호와 같습니다. 다시 입력해주세요.');
            $('#img_password1').hide();
            $('#password1').val('').focus();
            $('#wrong_img_password1').show();
        }else {
            $('#join-submit').attr('check_result_password1', 'success');
            $('#img_password1').show();
            $('#wrong_img_password1').hide();
            $('#message_pw1').hide()
            return;
        }
    });

    $('#password2').blur(function() {
       var pw = $('#password1').val();
       var pw2 = $('#password2').val();

       if(pw2 == ''){
            return;
       }if(pw != pw2){
            $("#message_pw2").html('비밀번호가 일치하지 않습니다.');
            $('#img_password2').hide();
            $('#wrong_img_password2').show();
            $('#password2').val('').focus();
            return;
       }else{
            $("#fix_info_submit").attr("check_result_password2", "success");
            $('#img_password2').show();
            $('#wrong_img_password2').hide();
            $("#message_pw1").hide()
            return;
       }
    });


    $('#change-form').submit(function() {
       console.log($("#fix_info_submit").attr("check_result_nickname"));
       console.log($("#fix_info_submit").attr("check_result_password"));
       console.log($("#fix_info_submit").attr("check_result_password2"));

        if($("#fix_info_submit").attr("check_result_nickname") == "fail" &&
            $("#fix_info_submit").attr("check_result_password") == "fail" &&
            $("#fix_info_submit").attr("check_result_password2") == "fail" &&
            $("#fix_info_submit").attr("check_result_like") == "fail"){
            alert('수정할 정보가 없습니다.');
            return false;
        }
    });

    $("#nickname").on("propertychange change keyup paste input", function(){
       $("#fix_info_submit").attr("check_result_nickname", "fail");
    });

    $("#password").on("propertychange change keyup paste input", function(){
       $("#fix_info_submit").attr("check_result_password", "fail");
    });

    $("#password1").on("propertychange change keyup paste input", function(){
       $('#password2').val('');
       $('#img_password1').hide();
       $('#img_password2').hide();
       $('#wrong_img_password1').show();
       $('#wrong_img_password2').show();
       $("#fix_info_submit").attr("check_result_password2", "fail");
    });

    $("#cancel_change").click(function(){
       $('#nickname').val('');
       $('#password').val('');
       $('#password1').val('');
       $('#password2').val('');

       $('#guid_nick').hide();
       $('#guid_like').hide();
       $('#nickname').hide();
       $('#img_nickname').hide();
       $('#wrong_img_nickname').hide();
       $('.change_value').show();

       $('#message_password').hide();
       $('.error_message').hide();
       $('.check_img').hide();
       $('.wrong_check_img').show();
       $('.form-check').hide();
    });
});