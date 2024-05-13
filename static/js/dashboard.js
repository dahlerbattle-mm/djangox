// Shows the callout box
function showCallout() {
  document.getElementById('callout').style.display = 'block';
  renderBarChart(); // Default to rendering the Bar Chart when opened
}

// Hides the callout box
function hideCallout() {
  document.getElementById('callout').style.display = 'none';
}

// Renders a generic Bar Chart
function renderBarChart() {
  Highcharts.chart('highcharts-graph', {
      chart: {
          type: 'column'
      },
      title: {
          text: 'Sample Bar Chart'
      },
      xAxis: {
          categories: ['Apples', 'Bananas', 'Oranges']
      },
      yAxis: {
          title: {
              text: 'Fruit eaten'
          }
      },
      series: [{
          name: 'Jane',
          data: [1, 0, 4]
      }, {
          name: 'John',
          data: [5, 7, 3]
      }]
  });
}

// Renders a generic Treemap
function renderTreemap() {
  Highcharts.chart('highcharts-graph', {
      series: [{
          type: 'treemap',
          layoutAlgorithm: 'squarified',
          data: [
              { name: 'A', value: 6 },
              { name: 'B', value: 6 },
              { name: 'C', value: 4 },
              { name: 'D', value: 3 },
              { name: 'E', value: 2 },
              { name: 'F', value: 2 },
              { name: 'G', value: 1 }
          ]
      }],
      title: {
          text: 'Sample Treemap'
      }
  });
}

// Renders a generic Dial (Gauge)
function renderDial() {
  Highcharts.chart('highcharts-graph', {
      chart: {
          type: 'gauge',
          plotBackgroundColor: null,
          plotBackgroundImage: null,
          plotBorderWidth: 0,
          plotShadow: false
      },
      title: {
          text: 'Sample Dial'
      },
      pane: {
          startAngle: -150,
          endAngle: 150
      },
      yAxis: {
          min: 0,
          max: 200,
          title: {
              text: 'Speed'
          },
          stops: [
              [0.1, '#55BF3B'], // green
              [0.5, '#DDDF0D'], // yellow
              [0.9, '#DF5353'] // red
          ],
          lineWidth: 0,
          minorTickInterval: null,
          tickPixelInterval: 400,
          tickWidth: 0,
          labels: {
              y: 16
          }
      },
      series: [{
          name: 'Speed',
          data: [120], // Example speed
          tooltip: {
              valueSuffix: ' km/h'
          }
      }]
  });
}

// Event listeners for sidebar charts (if still needed)
document.getElementById('bar').addEventListener('click', renderBarChart);
document.getElementById('tree').addEventListener('click', renderTreemap);
document.getElementById('dial').addEventListener('click', renderDial);
