function checkUpdatePredictPrice() {
    $(".divTableRow.c_init:not([value='SUCCESS'])").each(function(index, element) {  
        var task = $(element).attr('task');                 
        //console.log("s name = "+ $(element).attr('name') + " task id: " + task);  
        var value_status = $(element).attr('value').trim();               
        if (value_status == "PENDING" ) {
            console.log("Pending set WAITING" + $(element).attr('name') + "quarter: " + $("#select_quarter").val()+
            "date: " + $("#select_date").val());
            $(element).attr('value', "WAITING")
            $.ajax(
                {
                    url:"/stock/query/",
                    type:'POST',
                    dataType:'json',
                    data:{stock_name: $(element).attr('name'), task_id:task, quarter:$("#select_quarter").val()},
                    success: function (response) {
                        //console.log("status: " + response.status + " stock_id: " + response.stock_id + " value: " + response.value);  
                        $('div[name=s_' + response.stock_id + ']').attr("value",  response.status);
                        if (response.status == "SUCCESS") {
                            updatePredictPrice(response.stock_id, response.value);
                        }        
                    }
        
                }
            );
        }
        else if(value_status == "INIT") {
            console.log("INIT set WAITING" + $(element).attr('name') + "quarter: " + $("#select_quarter").val() + 
            "date: " + $("#select_date").val());
            $(element).attr('value', "WAITING")
            $.ajax(
                {
                    url:"/stock/init/",
                    type:'POST',
                    dataType:'json',
                    data:{stock_name: $(element).attr('name'), quarter:$("#select_quarter").val(), date_time:$("#select_date").val()},
                    success: function (response) {
                        //console.log("init status: " + response.status + " stock_id: " + response.stock_id + " task: " + response.task); 
                        
                        $('div[name=s_' + response.stock_id + ']').attr("value",  response.status);
                        $('div[name=s_' + response.stock_id + ']').attr("task",  response.task);
                        $('div[id=name_' + response.stock_id + '] > a').text(response.basic.name);
                        $('div[id=price_now_c_' + response.stock_id + ']').text(response.basic.info.close);
                        if (response.status == "SUCCESS") {
                            updatePredictPrice(response.stock_id, response.value);
                        } 
                              
                    }
        
                }
            );
        }
    });
};

function updatePriceColor(stock_id) {
    var now_price = parseFloat($('#price_now_c_'+ stock_id).text());
    var expensive = parseFloat($('#price_exp_'+ stock_id).text());   
    var resonable = parseFloat($('#price_res_'+ stock_id).text());  
    var cheap = parseFloat($('#price_chp_'+ stock_id).text()); 

    if (isNaN(now_price) || isNaN(expensive) || isNaN(resonable) || isNaN(cheap)  ) {
        return;
    }
    else {
        var color_name;
        var price_level;
        if (now_price <= cheap) {
            color_name = 'Blue';
            price_level = 1;
        }
        else if (now_price > cheap && now_price <= resonable) {
            color_name = 'Green';
            price_level = 2;
        }
        else if (now_price > resonable && now_price <= expensive) {
            color_name = 'Orange';
            price_level = 3;
        }
        else if (now_price > expensive) {
            color_name = 'Red';
            price_level = 4;
        }
        else {
            color_name = 'Black';
            price_level = 0;
        }
        console.log("stock: " + stock_id + " color: " + color_name + " now_price " + now_price
        + " expensive " + expensive+ " resonable " + resonable+ " cheap " + cheap);
        $('#price_now_c_'+ stock_id).attr('p_level', price_level);
        $('#price_now_c_'+ stock_id).css("color", color_name);
    }

}

function updatePredictPrice(stock_id, predict_price_tbl) {
    $('#price_exp_'+ stock_id).text(predict_price_tbl["expen"]);   
    $('#price_res_'+ stock_id).text(predict_price_tbl["reson"]);  
    $('#price_chp_'+ stock_id).text(predict_price_tbl["cheap"]); 
    updatePriceColor(stock_id);
}