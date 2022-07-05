$(function(){
    var board_type = $('#board_type').text();
    var value = board_type.slice(0,2);
    var board_id = $('#board_type_en').attr('name');

    $("#board_write").attr('href','/board/board_write/'+board_id);

    if(value=="자유"){
        $('#free').attr('href','/board/free_free');
        $('#politic').attr('href','/board/free_politic');
        $('#issue').attr('href','/board/free_issue');
    }else if(value=="야당"){
        $('#free').attr('href','/board/oppo_free');
        $('#politic').attr('href','/board/oppo_politic');
        $('#issue').attr('href','/board/oppo_issue');
    }else if(value=="여당"){
        $('#free').attr('href','/board/rul_free');
        $('#politic').attr('href','/board/rul_politic');
        $('#issue').attr('href','/board/rul_issue');
    }
})