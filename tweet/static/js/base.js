$(function(){
    $(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);
}); 