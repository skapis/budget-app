$(document).ready(function(){

    var language = $(location).attr('href').split('/')[3];

    var chartCont = $('#barCont')
    var context = $('#barChart').get(0).getContext("2d");
    

    $.ajax({
        type: 'GET',
        url: '/transactions/time?period=month',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            new Chart(context, {
                type: 'bar',
                data: parseMonthData(data.data, language),
                options: {
                    responsive: true,
                    legend: {
                        position: 'bottom'
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                            },
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                            }
                        }]
                        ,
                        xAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                            }
                        }]
                    }
                }
            })
        }
    })

    $('#monthBtn').click(function(){
        $.ajax({
            type: 'GET',
            url: '/transactions/time?period=month',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data){
                chartCont.empty()
                chartCont.append($('<canvas />').attr('id', 'barChart').addClass('chart chart-sm'))
                var context = $('#barChart').get(0).getContext("2d");
                $('#monthBtn').removeClass('btn-outline-primary').addClass('btn-primary')
                $('#yearBtn').removeClass('btn-primary').addClass('btn-outline-primary')
                new Chart(context, {
                    type: 'bar',
                    data: parseMonthData(data.data, language),
                    options: {
                        responsive: true,
                        legend: {
                            position: 'bottom'
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    min: 0,
                                },
                                gridLines: {
                                    color: "rgba(0, 0, 0, 0)",
                                }
                            }]
                            ,
                            xAxes: [{
                                gridLines: {
                                    color: "rgba(0, 0, 0, 0)",
                                }
                            }]
                        }
                    }
                })
            }
        })    
    })

    $('#yearBtn').click(function(){
        $.ajax({
            type: 'GET',
            url: '/transactions/time?period=year',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data){
                chartCont.empty()
                chartCont.append($('<canvas />').attr('id', 'barChart').addClass('chart chart-sm'))
                var context = $('#barChart').get(0).getContext("2d");
                $('#yearBtn').removeClass('btn-outline-primary').addClass('btn-primary')
                $('#monthBtn').removeClass('btn-primary').addClass('btn-outline-primary')
                new Chart(context, {
                    type: 'bar',
                    data: parseYearData(data.data, language),
                    options: {
                        responsive: true,
                        legend: {
                            position: 'bottom'
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    min: 0,
                                },
                                gridLines: {
                                    color: "rgba(0, 0, 0, 0)",
                                }
                            }]
                            ,
                            xAxes: [{
                                gridLines: {
                                    color: "rgba(0, 0, 0, 0)",
                                }
                            }]
                        }
                    }
                })
            }
        })    
    })

})

function parseMonthData(data, lang){
    // sort data by month label
    data.sort((a, b) => (a.month_label > b.month_label) ? 1 : -1)
    labels = Array.from(new Set(data.map((item) => item.month_label)))
    categories = {
        'income': {
            'en': 'Income',
            'cs': 'Příjmy'
        },
        'expense':{
            'en': 'Expense',
            'cs': 'Výdaje'
            
        }
    }

    incomes = new Array()
    expenses = new Array()
    
    labels.map(label => {
        items = data.filter((element) => element.month_label == label)
        if (items.length == 1){
            if(items[0].type__name == 'Income'){
                expenses.push('0')
            } else {
                incomes.push('0')
            }
        }
        items.forEach(item => {
            if (item.type__name == 'Income'){
                incomes.push(item.sum)
            } else {
                expenses.push(item.sum)
            }
        });
    })

    datasets = [
        {
            label: categories.income[lang],
            backgroundColor: 'rgb(75, 192, 192)',
            data: incomes
        },
        {
            label: categories.expense[lang],
            backgroundColor: 'rgb(255, 99, 132)',
            data: expenses
        } 
    ]
    return {'labels': labels ,'datasets': datasets}
};


function parseYearData(data, lang){
    // sort data by month label
    data.sort((a, b) => (a.date__year > b.date__year) ? 1 : -1)
    labels = Array.from(new Set(data.map((item) => item.date__year)))
    categories = {
        'income': {
            'en': 'Income',
            'cs': 'Příjmy'
        },
        'expense':{
            'en': 'Expense',
            'cs': 'Výdaje'
            
        }
    }

    incomes = new Array()
    expenses = new Array()
    
    labels.map(label => {
        items = data.filter((element) => element.date__year == label)
        if (items.length == 1){
            if(items[0].type__name == 'Income'){
                expenses.push('0')
            } else {
                incomes.push('0')
            }
        }
        items.forEach(item => {
            if (item.type__name == 'Income'){
                incomes.push(item.sum)
            } else {
                expenses.push(item.sum)
            }
        });
    })

    datasets = [
        {
            label: categories.income[lang],
            backgroundColor: 'rgb(75, 192, 192)',
            data: incomes
        },
        {
            label: categories.expense[lang],
            backgroundColor: 'rgb(255, 99, 132)',
            data: expenses
        } 
    ]
    return {'labels': labels ,'datasets': datasets}
};
