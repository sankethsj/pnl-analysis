const summaryChart = document.getElementById('summaryChart');
const scriptChart = document.getElementById('scriptChart');
const scriptDetails = document.querySelector('.script-details');

console.log(data);


new Chart(summaryChart, {
    type: 'doughnut',
    data: {
        labels: [
            'Profit Trades',
            'Loss Trades',
        ],
        datasets: [{
            label: 'PnL Report Summary',
            data: [data.overall.profit_trades, data.overall.loss_trades],
            backgroundColor: [
                'rgb(50, 255, 0)',
                'rgb(255, 0, 50)'
            ],
            hoverOffset: 4
        }]
    }
});


script_labels = Object.keys(data.script_analysis)

script_profit_counts = Object.entries(data.script_analysis).map((element) => element[1].profit_trades)
script_loss_counts = Object.entries(data.script_analysis).map((element) => element[1].loss_trades)


new Chart(scriptChart, {
    type: 'bar',
    data: {
        labels: script_labels,
        datasets: [
            {
                label: 'Number of Profit Trades',
                data: script_profit_counts,
                backgroundColor: 'rgb(50, 255, 0)',
            },
            {
                label: 'Number of Loss Trades',
                data: script_loss_counts,
                backgroundColor: 'rgb(255, 0, 50)'
            }
        ]
    },
    options: {
        plugins: {
          title: {
            display: true,
            text: 'Script-wise trade details'
          },
        },
        responsive: true,
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true
          }
        }
      }
});

let max_profit_pct = 0;
let max_profit_script = "";

Object.entries(data.script_analysis).forEach(element => {
    if(element[1].profit_trades_pct > max_profit_pct){
        max_profit_pct = element[1].profit_trades_pct;
        max_profit_script = element[0];
    }
});

let temp = `<p>Your Profitable Script : <span id="script-name">${max_profit_script}</span>
<span id="script-win-rate" style="background-color: ${max_profit_pct > 50 ? 'green' : 'red'};">WIN RATE : ${max_profit_pct} %</span>
</p>
<em>${data.script_analysis[max_profit_script].trade_summary}</em>
`
scriptDetails.innerHTML = temp;

console.log(data.script_analysis[max_profit_script], max_profit_pct);