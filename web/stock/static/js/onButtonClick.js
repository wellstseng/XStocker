function onSortIdClick() {
    $("#tbody .divTableRow.c_init").sort(function (a, b) {
       
        var contentA =parseInt( $(a).attr('name').replace("s_", ""));
        var contentB =parseInt( $(b).attr('name').replace("s_", ""));
        console.log("onSortIdClick sort a: " + contentA + "  content B: " + contentB);
        return (contentA < contentB) ? -1 : (contentA > contentB) ? 1 : 0;
     }).appendTo('#tbody')
}

function onSortCloseClick() {
    console.log("onSortCloseClick");
    $("#tbody .divTableRow.c_init").sort(function (a, b) {       
        var keyA1 =parseInt( $(a).children(".divTableCell.cPrice").attr('p_level'));
        var keyA2 =parseFloat( $(a).children(".divTableCell.cPrice").text());
        var keyB1 =parseInt( $(b).children(".divTableCell.cPrice").attr('p_level'));
        var keyB2 =parseFloat( $(b).children(".divTableCell.cPrice").text());
        console.log("onSortCloseClick sort a: " + keyA1+ " a2" + keyA2+"  content B: " + keyB1+ " b2" + keyB2);
        if (keyA1 < keyB1) return -1;
        if (keyA1 > keyB1) return 1;
        if (keyA2 < keyB2) return -1;
        if (keyA2 > keyB2) return 1;
        return 0;
     }).appendTo('#tbody')
}

function onUpdateClick() {
    $(".divTableRow.c_init").attr('value', 'INIT');
}

function onAddClick() {
    var new_stock = $("#new_stock_input").val();
    //console.log("new stock: " + new_stock);
    var $newdiv1 = $( '<div class="divTableRow c_init" name="s_'+ new_stock + '" value="INIT" task=""></div>' );
    $($newdiv1).append('<div class="divTableCell" id = "id_'+new_stock+'" >'+new_stock+'</div>');
    $($newdiv1).append('<div class="divTableCell" id = "name_'+new_stock+'">'+
    '<a target="_blank" href="https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='+new_stock+'&YEAR_PERIOD=9999&RPT_CAT=M_QUAR"></a></div>');
    $($newdiv1).append('<div class="divTableCell" id = "price_now_c_'+new_stock+'"></div>');
    $($newdiv1).append('<div class="divTableCell" id = "price_exp_'+ new_stock +'"> </div>');
    $($newdiv1).append('<div class="divTableCell" id = "price_res_'+ new_stock +'"> </div>');
    $($newdiv1).append('<div class="divTableCell" id = "price_chp_'+ new_stock +'"> </div>');
    $($newdiv1).append(
        '<div class="divTableCell" id = "toolbar_'+ new_stock +'">'+
            '<input type="button" id="delbtn_'+ new_stock +'"name="'+ new_stock +'" onclick="onDeleteClick(this.name)" value="移除">'+
        '</div>');
    $("#tbody").append($newdiv1);
    
}

function onDeleteClick(clicked_name) {
    console.log("Click delete " +  clicked_name);
     $.ajax(
        {
            url:"/stock/delete_stock/",
            type:'POST',
            dataType:'json',
            data:{stock_id: clicked_name},
            success: function (response) {
                console.log("onDeleteClick sstatus"+ response.status +" stock_id: " + response.stock_id );  
                $('div[name=s_' + response.stock_id + ']').remove();                                  
            }

        }
    );
}
