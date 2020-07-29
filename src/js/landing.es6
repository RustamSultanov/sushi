$(function() {
    var swiperWithPagination = new Swiper('#swiper-with-pagination', {
        pagination: {
            el: '.swiper-pagination',
            clickable: true
        }
    });

    // Wrap charts
    $('.chartjs').each(function() {
        $(this).wrap($('<div style="height:' + this.getAttribute('height') + 'px"></div>'));
    });
    var pieChart = new Chart(document.getElementById('chart-pie').getContext("2d"), {
        type: 'pie',
        data: {
            labels: ['Пройдено', 'Не пройдено'],
            datasets: [{
                data: [ 5, 15 ],
                backgroundColor: [ '#F2F2F2', '#F26722' ],
                hoverBackgroundColor: [ '#F2F2F2', '#F26722']
            }]
        },

        // Demo
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            }
        }
    });
});