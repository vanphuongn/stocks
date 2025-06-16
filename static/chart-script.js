let currentType = 'line';
let currentRange = '3M';

const ctx = document.getElementById('priceChart').getContext('2d');


const priceChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: []
  },
  options: {
    responsive: true,
    scales: {
      x: {
        type: 'category'
      },
      y: {
        beginAtZero: false
      }
    },
    plugins: {
      legend: { display: true }
    }
  }
});

function setChartType(type) {
  currentType = type;
  updateChart(currentRange);
}

function updateChart(range) {
  currentRange = range;

  const rangeMap = {
    '1W': 7,
    '1M': 22,
    '3M': 66,
    'ALL': labelsAll.length
  };
  const count = rangeMap[range] || labelsAll.length;

  const labels = labelsAll.slice(-count);
  const closes = dataAll.slice(-count);
  const ohlc = ohlcAll.slice(-count);

  if (currentType === 'line') {
    priceChart.config.type = 'line';
    priceChart.data.labels = labels;
    priceChart.data.datasets = [{
      label: 'Giá đóng cửa',
      data: closes,
      borderColor: '#42a5f5',
      borderWidth: 2,
      tension: 0.1,
      fill: false
    }];
    priceChart.options.scales.x = {
      type: 'category'
    };
  } else {
    priceChart.config.type = 'candlestick';
    priceChart.data.labels = [];
    priceChart.data.datasets = [{
      label: 'Nến giá',
      data: ohlc,
      color: {
        up: '#00e676',
        down: '#ff3d00',
        unchanged: '#999'
      }
    }];
    priceChart.options.scales.x = {
      type: 'time',
      time: {
        unit: 'day',
        tooltipFormat: 'yyyy-MM-dd'
      }
    };
  }

  priceChart.update();
}

// Load initial chart
updateChart('3M');
