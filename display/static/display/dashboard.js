/* globals Chart:false, feather:false */
$(document).ready(function(){

  var progress = setInterval(function() {
    var $bar = $('.bar');

    if ($bar.width()>=400) {
      clearInterval(progress);
      $('.progress').removeClass('active');
    } else {
      $bar.width($bar.width()+40);
    }
    $bar.text($bar.width()/4 + "%");
  }, 800);

})


function generate_prediction(elmnt, clr) {
  $.ajax({
    type: "POST",
    url: "test.py",
    data: {param: text}
  }).done(function() {
    console.log("What?")
  });
  elmnt.style.color = clr;
}


(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()
