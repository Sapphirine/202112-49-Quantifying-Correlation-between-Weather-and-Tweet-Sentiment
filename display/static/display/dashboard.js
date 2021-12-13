/* globals Chart:false, feather:false */
function startTimer(duration, display) {
  let timer = duration, minutes, seconds;
  setInterval(function () {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    display.textContent = minutes + ":" + seconds;

    if (--timer < 0) {
      timer = duration;
    }
  }, 1000);
}

function tweet_countdown(button) {
  button.onclick = null;
  let i = document.getElementById("twitter_dropdown").value;
  let display = document.getElementById('twitter_timer');
  startTimer(i, display);
}

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

//plot the prediction graph
var xValue = ['Product A', 'Product B', 'Product C'];

var yValue = [20, 14, 23];

var trace1 = {
  x: xValue,
  y: yValue,
  type: 'bar',
  text: yValue.map(String),
  textposition: 'auto',
  hoverinfo: 'none',
  marker: {
    color: 'rgb(158,202,225)',
    opacity: 0.6,
    line: {
      color: 'rgb(8,48,107)',
      width: 1.5
    }
  }
};

var data = [trace1];

var layout = {
  title: 'January 2013 Sales Report',
  barmode: 'stack'
};

Plotly.newPlot('prediction_graph', data, layout);