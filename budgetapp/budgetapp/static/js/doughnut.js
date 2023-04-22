$(document).ready(function(){

    var language = $(location).attr('href').split('/')[3];

    var context = $('#categoryChart').get(0).getContext("2d");
    var chartCont = $('#catCont')
    var today = new Date()

    const searchParams = new URLSearchParams(window.location.search)
    if (searchParams.has('month')){
        var month = searchParams.get('month')
        var year = searchParams.get('year')
        if (month < 10){
            month = "0" + month
        }
    } else {
        var month = today.getMonth()+1
         if (month < 10){
            month = "0" + month
        }
        var year = $('[name="year"]').val()
    }

    $.ajax({
        type: 'GET',
        url: '/'+ language +'/transactions/category?month='+ year +'-'+ month +'&type=1',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            var labels = Object.keys(data.data)
            var values = Object.values(data.data)
            new Chart(context, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Category',
                        data: values,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                      display: false,
                      text: "Current value by stock",
                    },
                    legend: {
                        position: "bottom",
                        align: 'center',
                        labels:{
                            fontSize: 12,
                            boxWidth: 10
                        }
                    }
                  }
            })
        }
    })

    $('#incomeBtn').click(function(){
        $.ajax({
            type: 'GET',
            url: '/'+ language +'/transactions/category?month='+ year +'-'+ month +'&type=1',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data){
                chartCont.empty()
                chartCont.append($('<canvas />').attr('id', 'categoryChart').addClass('chart chart-sm'))
                var context = $('#categoryChart').get(0).getContext("2d");
                $('#incomeBtn').removeClass('btn-outline-primary').addClass('btn-primary')
                $('#expenseBtn').removeClass('btn-primary').addClass('btn-outline-primary')
                var labels = Object.keys(data.data)
                var values = Object.values(data.data)
                new Chart(context, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Category',
                            data: values,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                          display: false,
                          text: "Current value by stock",
                        },
                        legend: {
                            position: "bottom",
                            align: 'center',
                            labels:{
                                fontSize: 12,
                                boxWidth: 10
                            }
                        }
                      }
                })
            }
        })
    });

    $('#expenseBtn').click(function(){
        $.ajax({
            type: 'GET',
            url: '/'+ language +'/transactions/category?month='+ year +'-'+ month +'&type=2',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data){
                chartCont.empty()
                chartCont.append($('<canvas />').attr('id', 'categoryChart').addClass('chart chart-sm'))
                var context = $('#categoryChart').get(0).getContext("2d");
                $('#expenseBtn').removeClass('btn-outline-primary').addClass('btn-primary')
                $('#incomeBtn').removeClass('btn-primary').addClass('btn-outline-primary')
                var labels = Object.keys(data.data)
                var values = Object.values(data.data)
                new Chart(context, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Category',
                            data: values,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                          display: false,
                          text: "Current value by stock",
                        },
                        legend: {
                            position: "bottom",
                            align: 'center',
                            labels:{
                                fontSize: 12,
                                boxWidth: 10
                            }
                        }
                      }
                })
            }
        })
    })

})

