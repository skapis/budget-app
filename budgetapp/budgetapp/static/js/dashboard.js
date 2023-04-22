$(document).ready(function(){

    var language = $(location).attr('href').split('/')[3];


    var categorySelect = $('#newCategory')
    $('#newTransBtn').click(function(){
            $.ajax({
                type: 'GET',
                url: 'categories',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function(data){
                    categorySelect.empty()
                    data.categories.income.map((item)=>{
                        categorySelect.append(
                            $('<option/>').val(item.categoryId).text(item.name)
                        )
                    })
                }
            })
        }
    )

    $('[name=type]').change(function(){
            $.ajax({
                type: 'GET',
                url: 'categories',
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