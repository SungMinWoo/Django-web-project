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
    var csrftoken = getCookie('csrftoken');
    $('.check').blur(function(){
        var user_reg =  /^[a-z0-9_]{4,20}$/;
        var email_reg = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@(naver)*.(com)$/i;
        var number_reg = /^[0-9]+$/;
        var password_reg = /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;

        var value = $(this).attr('id');
        var value_location = $('#'+value).val();
        var check_value = false;

        var pw = $("#password1").val();
        var user_email = $('#pw_email').val();
        var user_id = $('#user_id').val();

        if(value_location == ''){
            return;
        }else if(value == 'user_id'){
             if(false === user_reg.test(value_location)){
                $("#message_user_id").show();
                $("#message_user_id").html('올바르지 않습니다. 다시 입력해주세요.');
                $('#user_id').val('').focus();
            }else{
                $("#message_user_id").hide();
                check_value = true;
            }
        }else if(value == 'email'){
             if(false === email_reg.test(value_location)){
                $("#message_email").show();
                $("#message_email").html('올바르지 않습니다. 다시 입력해주세요.');

                $('#email').val('').focus();
            }else{
                $("#message_email").hide();
                check_value = true;
            }
        }else if(value == 'pw_email'){
            if(false === email_reg.test(value_location)){
                $("#message_pw_email").show();
                $("#message_pw_email").html('올바르지 않습니다. 다시 입력해주세요.');
                $('#pw_email').val('').focus();
            }else{
                $("#message_email").hide();
                check_value = true;
            }
        }else if (value == 'random_number'){
            if(false === number_reg.test($('#random_number').val())){
                alert('숫자만 입력해주세요');
                $('#random_number').val('').focus();
            }else{
                check_value = true;
            }
        }

        if(check_value == true){
//            id 찾기
            $('#search_id').unbind('click').click(function(){
                $.ajax({
                    url:'api/check-value/',
                    type:'POST',
                    dataType:'json',
                    data:{
                        'id': value,
                        'value': value_location,
                        'send_email': true,
                        'csrfmiddlewaretoken': csrftoken,
                    },
                    success:function(response){
                        if(response.result != 'success'){
                            console.error(response.data)
                            return;
                        }
                        if(response.data == 'exist'){
                            alert("이메일을 보냈습니다.");
                            return;
                        }else if(response.data == 'ban'){
                            alert("관련 이메일은 관리자에게 문의바랍니다.");
                            return;
                        }else if(response.data == undefined){
                            alert("존재하지 않는 아이디 입니다.");
                            return;
                        }
                        // console.log(response)
                    },
                    error : function(xhr, error){
                        alert("서버와의 통신에서 문제가 발생했습니다.");
                        console.error("error : " + error);
                    }
                })
            })
//                중복 클릭 형산 제거 pw 찾기
            $('#check_pw').unbind('click').click(function(){
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
                        $('#random_number').hide();
                        $('#check_pw').show();
                        $('#check_number').hide();
                        $('#time_notice').show();
                    }
                }, 1000);

                $.ajax({
                    url:'api/find-pw/?',
                    type:'POST',
                    dataType:'json',
                    data:{
                        'id': user_id,
                        'email': user_email,
                        'csrfmiddlewaretoken': csrftoken,
                    },
                    success:function(response){
                        if(response.result != 'success'){
                            console.error(response.data)
                            return;
                        }
                        if(response.data == 'pass'){
                            alert("이메일을 보냈습니다. 인증번호를 확인해주세요.");
                            $('#check_pw').hide();
                            $('#random_number').show();
                            $('#check_number').show();
                            $("#message_pw_email").hide();
                            $('#limit_time').show();
                            return;
                        }else if(response.data == 'fail'){
                            alert("아이디 혹은 이메일이 잘못되었습니다.");
                            return;
                        }else if(response.data == 'ban'){
                            alert("관련 이메일은 관리자에게 문의바랍니다.");
                            return;
                        }else if(response.data == undefined){
                            alert("존재하지 않는 아이디 입니다.");
                            return;
                        }
                        // console.log(response)
                    },
                    error : function(xhr, error){
                        alert("서버와의 통신에서 문제가 발생했습니다.");
                        console.error("error : " + error);
                    }
                })
            })
//           인증번호 확인
            $('#check_number').unbind('click').click(function(){
                var user_number = $('#random_number').val();
                var user_email = $('#pw_email').val();
                if (user_number == ''){
                    return false;
                }
                else{
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
                                $('#hidden_email').val(user_email);
                                $('#check_number').hide();
                                $('#random_number').hide();
                                $('#limit_time').hide();
                                $('#time_notice').hide();
                                $('#pass_number').show();
                                $('#join-submit').attr('check_result_number', 'success');
                                $('#change_pw').show();
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
                }
            });
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
       console.log($("#fix_info_submit").attr("check_result_password1"));
       console.log($("#fix_info_submit").attr("check_result_password2"));

        if($("#fix_info_submit").attr("check_result_password1") == "fail" &&
            $("#fix_info_submit").attr("check_result_password2") == "fail"){
            alert('수정할 정보가 없습니다.');
            return false;
        }
    });

    $("#password1").on("propertychange change keyup paste input", function(){
       $('#password2').val('');
       $('#img_password1').hide();
       $('#img_password2').hide();
       $('#wrong_img_password1').show();
       $('#wrong_img_password2').show();
       $("#fix_info_submit").attr("check_result_password2", "fail");
    });

    $("#pw_email").on("propertychange change keyup paste input", function(){
       $("#fix_info_submit").attr("check_result_password1", "fail");
       $("#fix_info_submit").attr("check_result_password2", "fail");
       $('#check_pw').show();
       $('#pass_number').hide();
       $('#change_pw').hide();
    });
})