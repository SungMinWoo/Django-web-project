var doubleSubmitFlag = false;

function doubleSubmitCheck(){
    if(doubleSubmitFlag){
        return doubleSubmitFlag;
    }else{
        doubleSubmitFlag = true;
        return false;
    }
}

$(function(){
    $('#leave-poty').submit(function() {
       if($("input:checkbox[id='agree-prov']").is(":checked") == false){
          alert("회원탈퇴 관련 사항에 동의해주시기바랍니다.");
          return false;
       }else if($("#leave_submit").attr("check_result_password") == "fail"){
            alert('비밀번호를 입력해주세요.');
            return false;
       }else{
            var result = confirm('탈퇴하시겠습니까?');
            if(result) {
                if(doubleSubmitCheck()) return;
            }else{
                return false;
            }
              return true;
       }
    });

    $('.check').blur(function(){
        var value = $(this).attr('id');
        var password_reg = /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;
        var check_value = false;
        var value_location = $('#'+value).val();

        if(value_location == ''){
            return;
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
                url:'api/check-value/?'+value+'='+value_location,
                type:'get',
                dataType:'json',
                data:{
                    id: value
                },
                success:function(response){
                    if(response.result != 'success'){
                        console.error(response.data)
                        return;
                    }
                    if(response.data == 'pw_pass'){
                        $('#message_'+value).show();
                        $("#message_"+value).html("비밀번호가 일치합니다.");
                        $('#wrong_img_'+value).hide();
                        $('#check_'+value).show();
                        $("#leave_submit").attr("check_result_"+value, "success");
                        return;
                    }else if(response.data == 'pw_no_pass'){
                        $('#message_'+value).show();
                        $("#message_"+value).html("비밀번호가 일치하지않습니다.");
                        $('#'+value).val('').focus();
                        $('#wrong_img_'+value).show();
                        $('#check_'+value).hide();
                        $("#leave_submit").attr("check_result_"+value, "fail");
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

    $("#password").on("propertychange change keyup paste input", function(){
       $("#leave_submit").attr("check_result_password", "fail");
    });
});