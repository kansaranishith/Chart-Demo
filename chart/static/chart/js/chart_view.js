  $(document).ready(function () {

    var protocol = window.location.protocol
    var hostname = window.location.hostname
    var port = window.location.port

    var url = protocol + '//' + hostname + ':' + port + '/data/' + file_id;

        $.getJSON(url, function (data) {

            var ctx = document.getElementById('ChartCanvas');

            var myChart = new Chart(ctx, {
                type: chart_type,
                data: {
                    labels: data['X'],
                    datasets: [{
                        label: 'Monthly analysis',
                        data: data['Y'],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(300, 01, 200, 0.2)',
                            'rgba(100, 113, 50, 0.2)',
                            'rgba(215, 50, 50, 0.2)',
                            'rgba(202, 161, 105, 0.2)',
                            'rgba(4, 113, 50, 0.2)',
                            'rgba(1, 50, 113, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(300, 01, 200, 1)',
                            'rgba(100, 113, 50, 1)',
                            'rgba(215, 50, 50, 1)',
                            'rgba(202, 161, 105 , 1)',
                            'rgba(4, 113, 50, 1)',
                            'rgba(4, 50, 113, 1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        });

  });