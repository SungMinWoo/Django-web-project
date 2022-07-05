$(function(){
    $('#terms-form').submit(function() {
       if($("input:checkbox[id='agree-prov']").is(":checked") == false) {
          alert("약관동의를 확인하여 주시기 바랍니다.");
          return false;
       }else if($("input:checkbox[id='agree-prov2']").is(":checked") == false) {
          alert("개인정보 처리방침를 확인하여 주시기 바랍니다.");
          return false;
       }else if($("input:checkbox[id='agree-age']").is(":checked") == false) {
          alert("만 14이상에 동의하여 주시기 바랍니다.");
          return false;
       }else{
          return true;
       }
    });
});