/* globals Chart:false, feather:false */
document.getElementById("twitter_update").addEventListener("click", function () {
  let progress = document.createElement("div");
  progress.className = "progress";
  progress.style.height = "20px";
  progress.innerHTML = `
    <div class="progress-bar" role="progressbar" 
    style="width: 25%;" 
    aria-valuenow="25" 
    aria-valuemin="0" 
    aria-valuemax="100">
    25%
    </div>
  `;
  document.getElementById("twitter_progress").appendChild(progress);
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
