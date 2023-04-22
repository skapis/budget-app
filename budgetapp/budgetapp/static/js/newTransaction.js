$(document).ready(function(){
    $('#submitBtn').click(function(){
        $.ajax({
            type: 'POST',
            url: '/transaction',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: JSON.stringify({
                wallet: $('[name=wallet]').val(),
                type: $('[name=type]').val(),
                date: $('[name=date]').val(),
                amount: $('[name=amount]').val(),
                category: $('[name=category]').val()
            }),
            success: function(data){
                window.location.reload()
            }
        })
    })
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}