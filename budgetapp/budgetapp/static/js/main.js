$(document).ready(function(){

    var language = $(location).attr('href').split('/')[3];

    var today = new Date()

    var months =  
    [
        {'id':1,'cs':'Leden', 'en': 'January'},
        {'id':2,'cs':'Únor', 'en': 'February'},
        {'id':3,'cs':'Březen', 'en': 'March'},
        {'id':4,'cs':'Duben', 'en': 'April'},
        {'id':5,'cs':'Květen', 'en': 'May'},
        {'id':6,'cs':'Červen', 'en': 'June'},
        {'id':7,'cs':'Červenec', 'en': 'July'},
        {'id':8,'cs':'Srpen', 'en': 'August'},
        {'id':9,'cs':'Září', 'en': 'September'},
        {'id':10,'cs':'Říjen', 'en': 'October'},
        {'id':11,'cs':'Listopad', 'en': 'November'},
        {'id':12,'cs':'Prosinec', 'en': 'December'}
    
    ]

    months.map((item) => {
        $('[name="month"]')
            .append($('<option>', {
                value: item.id,
                text:  item[language]

            }))
    });

    const searchParams = new URLSearchParams(window.location.search)
    if (searchParams.has('month')){
        $('[name="month"]').val(searchParams.get('month'))
        $('[name="year"]').val(searchParams.get('year'))
    } else {
        $('[name="month"]').val(today.getMonth()+1)
    }

    $('#showBtn').click(function(){
        var month = $('[name="month"]').val()
        var year = $('[name="year"]').val()
        window.location.href = window.location.pathname + '?year=' + year + '&month=' + month
    })

})