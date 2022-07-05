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
    $('.check').blur(function(){
        var csrftoken = getCookie('csrftoken');
        var user_reg =  /^[a-z0-9_]{4,20}$/;
        var nickname_reg =  /^[a-zㄱ-ㅎ|ㅏ-ㅣ|가-힣0-9]{2,10}$/;
        var email_reg = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@(naver)*.(com)$/i;

        var get_error_msg = $(this).attr('placeholder');
        var value = $(this).attr('id');

        var value_location = $('#'+value).val();
        var msg = get_error_msg.substr(0,3);
        //value = id값, msg = value 한국어, value_location = 입력값
        var check_value = false;

        if(value_location == ''){
            return;
        }else if(value == 'user_id'){
             if(false === user_reg.test(value_location)){
                $("#message_user_id").show();
                $("#message_user_id").html('올바르지 않습니다. 다시 입력해주세요.');
                $('#img_user_id').hide();
                $('#wrong_img_user_id').show();
                $('#user_id').val('').focus();
            }else{
                check_value = true;
            }
        }else if(value == 'nickname'){
            if(false === nickname_reg.test(value_location)){
                $("#message_nickname").show();
                $("#message_nickname").html('기준에 맞지 않습니다.');
                $('#img_nickname').hide();
                $('#wrong_img_nickname').show();
                $('#nickname').val('').focus();
            }else{
                check_value = true;
            }
        }else if(value == 'email'){
            if(false === email_reg.test(value_location)){
                $("#message_email").show();
                $("#message_email").html('올바르지 않습니다. 다시 입력해주세요.');
                $('#img_email').hide();
                $('#check_email').hide();
                $('#wrong_img_email').show();
                $('#email').val('').focus();
            }else{
                check_value = true;
            }
        }
        if(check_value == true){
            $.ajax({
                url:'api/check-value/',
                type:'post',
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
                    }else if(response.data == 'ban'){
                        $('#message_'+value).show();
                        $("#message_"+value).html("회원가입이 불가능한 이메일입니다. 관리자에게 문의바랍니다.");
                        $('#'+value).val('').focus();
                        return;
                    }else{
                        $('#message_'+value).hide();
                        $('#img_'+value).show();
                        $('#check_'+value).show();
                        $('#wrong_img_'+value).hide();
                        $("#join-submit").attr("check_result_"+value, "success");
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

    $('#check_email').click(function(){
        var user_email = $('#email').val();
        var csrftoken = getCookie('csrftoken');
        var time = 600;
        var min = "";
        var sec = "";

        var x = setInterval(function(){
            min = parseInt(time/60);
            sec = time%60;
            document.getElementById("limit_time").innerHTML = min + "분" + sec + "초";
            time--;

            if(time < 0) {
                clearInterval(x);
                document.getElementById('limit_time').innerHTML = "시간초과";
                $('#check_email').show();
                $('#random_number').hide();
                $('#check_number').hide();
                $('#time_notice').show();
            }
        }, 1000);
        $.ajax({
            url:'api/send-email/',
            type:'post',
            dataType:'json',
            data:{
                'email': user_email,
                'csrfmiddlewaretoken': csrftoken,
            },
            success:function(response){
                if(response.result == 'success'){
                    alert('인증번호를 발송하였습니다.');
                    $('#time_notice').hide();
                    $('#check_email').hide();
                    $('#random_number').show();
                    $('#check_number').show();
                    $('#limit_time').show();
                    return;
                }
                else{
                    alert('다시 시도하시기 바랍니다.');
                    $('#check_email').show();
                    $('#random_number').hide();
                    $('#check_number').hide();
                    return;
                }
            },
            error : function(xhr, error){
                alert("서버와의 통신에서 문제가 발생했습니다.");
                console.error("error : " + error);
            }
        })
    });

    $('#check_number').click(function(){
        var user_number = $('#random_number').val();
        var user_email = $('#email').val();

        $.ajax({
            url:'api/check-number/',
            type:'get',
            dataType:'json',
            data:{
                email: user_email,
                number: user_number,
            },
            success:function(response){
                if(response.data == 'pass'){
                    alert('이메일 인증이 완료되었습니다.');
                    $('#check_number').hide();
                    $('#random_number').hide();
                    $('#limit_time').hide();
                    $('#time_notice').hide();
                    $('#pass_number').show();
                    $('#join-submit').attr('check_result_number', 'success');
                    return;
                }
                else{
                    alert('다시 입력해주세요.');
                    return;
                }
            },
            error : function(xhr, error){
                alert("서버와의 통신에서 문제가 발생했습니다.");
                console.error("error : " + error);
            }
        })
    });

    $('#password').blur(function() {
        var reg = /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;
        var pw = $("#password").val();

        if(pw == ''){
            return;
        }else if (false === reg.test(pw)) {
            $("#message_pw").html('올바르지 않습니다. 다시 입력해주세요.');
            $('#img_password').hide();
            $('#wrong_img_password').show();
        }else {
            $('#join-submit').attr('check_result_password', 'success');
            $('#img_password').show();
            $('#wrong_img_password').hide();
            $('#message_pw').hide()
            return;
        }
    });

    $('#password2').blur(function() {
       var pw = $('#password').val();
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
            $("#join-submit").attr("check_result_password2", "success");
            $('#img_password2').show();
            $('#wrong_img_password2').hide();
            $("#message_pw").hide();
            $("#message_pw2").hide();
            return;
       }
    });

    $('#join-form').submit(function() {
       console.log($("#join-submit").attr("check_result_email"));
       console.log($("#join-submit").attr("check_result_user_id"));
       console.log($("#join-submit").attr("check_result_nickname"));
       console.log($("#join-submit").attr("check_result_password"));
       console.log($("#join-submit").attr("check_result_number"));

       if($("#join-submit").attr("check_result_user_id") == "fail") {
          alert("아이디를 확인해주시기 바랍니다.");
          $("#user_id").focus();
          return false;
       }else if($("#join-submit").attr("check_result_nickname") == "fail") {
          alert("닉네임을 확인해주시기 바랍니다.");
          $("#nickname").focus();
          return false;
       }else if($("#join-submit").attr("check_result_email") == "fail") {
          alert("이메일을 확인해주시기 바랍니다.");
          $("#email").focus();
          return false;
       }else if($("#join-submit").attr("check_result_number") == "fail") {
          alert('이메일 인증을 완료해주시기 바랍니다.');
          return false;
       }else if($("#join-submit").attr("check_result_password") == "fail") {
          alert('비밀번호는 8자 이상이어야 하며, 숫자/대문자/소문자/특수문자를 모두 포함해야 합니다.');
          $("#password").focus();
          return false;
       }else if($("#join-submit").attr("check_result_password2") == "fail") {
          alert('비밀번호가 일치하지 않습니다.');
          $("#password2").focus();
          return false;
       }
    });

    $("#email").on("propertychange change keyup paste input", function(){
       $('#img_email').hide();
       $('#pass_number').hide();
       $('#check_email').hide();
       $('#wrong_img_email').show();
       $('#time_notice').hide();
       $("#join-submit").attr("check_result_email", "fail");
       $("#join-submit").attr("check_result_number", "fail");
    });
    $("#user_id").on("propertychange change keyup paste input", function(){
       $('#img_user_id').hide();
       $('#wrong_img_user_id').show();
       $("#join-submit").attr("check_result_user_id", "fail");
    });
    $("#nickname").on("propertychange change keyup paste input", function(){
       $('#img_nickname').hide();
       $('#wrong_img_nickname').show();
       $("#join-submit").attr("check_result_nickname", "fail");
    });
    $("#password").on("propertychange change keyup paste input", function(){
       $('#password2').val('');
       $('#img_password').hide();
       $('#img_password2').hide();
       $('#wrong_img_password').show();
       $('#wrong_img_password2').show();
       $("#join-submit").attr("check_result_password2", "fail");
    });
});