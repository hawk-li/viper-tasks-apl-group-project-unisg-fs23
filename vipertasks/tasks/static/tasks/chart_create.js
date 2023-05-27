// Color Palette
const colorPalette = [
    '#4CAF50', // Green
    '#FF5722', // Orange
    '#2196F3', // Blue
    '#FFC107', // Yellow
    '#E91E63', // Pink
    '#9C27B0', // Purple
  ];
  
  fetch('/task/stats' + '?user=' + window.location.pathname.split('/')[1])
    .then(response => response.json())
    .then(data => {
      new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: {
                color: '#fff', // Dark gray
                fontColor: 'rgb(000, 000, 000)'
              },
            },
          },
        },
      });
    });
  
  fetch('/task/completed-per-day' + '?user=' + window.location.pathname.split('/')[1])
    .then(response => response.json())
    .then(data => {
      new Chart(document.getElementById('lineChart'), {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              ticks: {
                stepSize: 1,
                color: '#fff', // Dark gray
              },
            },
            x: {
              ticks: {
                color: '#fff', // Dark gray
              },
            },
          },
          plugins: {
            legend: {
              labels: {
                color: '#fff', // Dark gray
              },
            },
          },
        },
      });
    });
  
  fetch('/task/completion-time' + '?user=' + window.location.pathname.split('/')[1])
    .then(response => response.json())
    .then(data => {
      new Chart(document.getElementById('completionTimeChart'), {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              ticks: {
                color: '#f8f9fa', // White
              },
            },
            x: {
              ticks: {
                color: '#f8f9fa', // White
              },
            },
          },
          plugins: {
            legend: {
              labels: {
                color: '#f8f9fa', // White
              },
            },
          },
        },
      });
    });
  
  fetch('/task/completion-rate' + '?user=' + window.location.pathname.split('/')[1])
    .then(response => response.json())
    .then(data => {
      const completionRate = data.datasets[0].data[0];
  
      new Chart(document.getElementById('progressChart'), {
        type: 'bar',
        data: {
          labels: ['Completion Rate'],
          datasets: [
            {
              data: [completionRate],
              backgroundColor: colorPalette[0], // Green
              borderColor: colorPalette[0], // Green
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {
            x: {
              beginAtZero: true,
              max: 100,
              ticks: {
                callback: value => value + '%',
                color: '#f8f9fa', // White
              },
            },
            y: {
              ticks: {
                color: '#f8f9fa', // White
              },
            },
          },
          plugins: {
            legend: {
              display: false,
            },
          },
        },
      });
    });
  
  fetch('/task/overdue-rate' + '?user=' + window.location.pathname.split('/')[1])
    .then(response => response.json())
    .then(data => {
      const overdueRate = data.datasets[0].data[0];
  
      new Chart(document.getElementById('overdueRateChart'), {
        type: 'bar',
        data: {
          labels: ['Overdue Rate'],
          datasets: [
            {
              data: [overdueRate],
              backgroundColor: colorPalette[1], // Orange
              borderColor: colorPalette[1], // Orange
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {
            x: {
              beginAtZero: true,
              max: 100,
              ticks: {
                callback: value => value + '%',
                color: '#f8f9fa', // White
              },
            },
            y: {
              ticks: {
                color: '#f8f9fa', // White
              },
            },
          },
          plugins: {
            legend: {
              display: false,
            },
          },
        },
      });
    });
  
  fetch('/task/creation-rate' + '?user=' + window.location.pathname.split('/')[1])
    .then(response => response.json())
    .then(data => {
      new Chart(document.getElementById('creationRateChart'), {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: '#f8f9fa', // White
              },
            },
            x: {
              ticks: {
                color: '#f8f9fa', // White
              },
            },
          },
          plugins: {
            legend: {
              labels: {
                color: '#f8f9fa', // White
              },
            },
          },
        },
      });
    });
  