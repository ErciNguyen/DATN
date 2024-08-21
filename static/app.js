// Function to draw chart
var drawChart = function(data) {
    var dataTrace = {
        x: data.map(item => item.TradingDate),
        open: data.map(item => item.Open),
        high: data.map(item => item.High),
        low: data.map(item => item.Low),
        close: data.map(item => item.Close),
        increasing: { line: { color: '#2EC886' }, fillcolor: '#24A06B' },
        decreasing: { line: { color: '#FF3A4C' }, fillcolor: '#CC2E3C' },
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y'
    };

    var layout = {
        showlegend: false,
        paper_bgcolor: "#1e1e1e",
        plot_bgcolor: "#1e1e1e",
        margin: {
            l: 60,
            r: 10,
            b: 90,
            t: 10
        },
        xaxis: {
            gridcolor: "#1f292f",
            rangeslider: {
                visible: true
            }
        },
        yaxis: {
            gridcolor: "#1f292f",
        },
        autosize: true,
        font: {
            color: '#efefef'
        }
    };

    Plotly.newPlot('chartDiv', [dataTrace], layout);

    // Ensuring the chart resizes correctly
    window.addEventListener('resize', function() {
        Plotly.Plots.resize(document.getElementById('chartDiv'));
    });
}





var app = new Vue({
    el: '#myDiv',
    data: {
        kpiData: []
    },
    methods: {
        loadData: async function() {
            try {
                const response = await fetch('data5.json');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const jsonData = await response.json();
                const data = jsonData.data;

                console.log('Fetched data:', data); // Log the fetched data

                // Ensure data is in the expected format
                if (data && Object.keys(data).length > 0) {
                    // Transform data into an array of objects
                    this.kpiData = Object.keys(data).map(key => ({
                        Symbol: data[key].Symbol,
                        Market: data[key].Market,
                        TradingDate: new Date(data[key].TradingDate), // Convert to Date object
                        Open: parseFloat(data[key].Open),
                        High: parseFloat(data[key].High),
                        Low: parseFloat(data[key].Low),
                        Close: parseFloat(data[key].Close),
                        Volume: parseInt(data[key].Volume, 10),
                        Value: parseFloat(data[key].Value)
                    }));

                    // Call drawChart function after data is loaded
                    drawChart(this.kpiData);

                    this.kpiData.forEach((item, index) => {
                        if (index > 0) {
                            if (item.Value < this.kpiData[index - 1].Value) {
                                item.valueClass = 'red';
                            } else if (item.Value > this.kpiData[index - 1].Value) {
                                item.valueClass = 'green';
                            } else {
                                item.valueClass = ''; // Clear the class if no change
                            }
                        } else {
                            item.valueClass = ''; // Clear the class for the first item
                        }
                    });
                } else {
                    throw new Error('Invalid data format: expected properties are missing');
                }
            } catch (error) {
                console.error('Error fetching or parsing data:', error);
            }
        }
    },
    created() {
        this.loadData();
    }
});