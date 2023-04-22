$(document).ready(function(){
    var categorySelect = $('[name=category]')
    var lang = $(location).attr('href').split('/')[3]

    $.ajax({
        type: 'GET',
        url: '/'+ lang +'/categories',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            if ($('[name=type]').val() == 1) {
                var type = 'income'
            } else {
                var type = 'expense'
            }
            data.categories[type].map((item)=>{
                if (categorySelect.children()[0].value != item.categoryId){
                    categorySelect.append(
                        $('<option/>').val(item.categoryId).text(item.name)
                    )
                }
            })
        }
    })
    

    $('[name=type]').change(function(){
            $.ajax({
                type: 'GET',
                url: '/'+ lang +'/categories',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function(data){
                    categorySelect.empty()
                    if ($('[name=type]').val() == 1) {
                        var type = 'income'
                    } else {
                        var type = 'expense'
                    }
                    data.categories[type].map((item)=>{
                        categorySelect.append(
                            $('<option/>').val(item.categoryId).text(item.name)
                        )
                    })
                }
            })
        }   
    )
})