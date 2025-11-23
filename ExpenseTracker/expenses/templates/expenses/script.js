var data = [{
    type: "pie",
    values: {{ totals_json | safe }},
    labels: {{ categories_json | safe }},
    textinfo: "label+value+percent",
    textposition: "outside",
    automargin: true
}];

var layout = {
    margin: {t:0, b:0, l:0, r:0},
    showlegend: true
};

Plotly.newPlot('piechart', data, layout);

function downloadPDF() {
    const button = document.getElementById('downloadBtn');
    button.style.display = 'none';

    // Hide all delete buttons
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(btn => btn.style.display = 'none');

    const element = document.getElementById('expenseTable');
    const opt = {
        margin:       0.5,
        filename:     'expense.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save().then(() => {
        // Show the button and delete buttons again after PDF is generated
        button.style.display = 'block';
        deleteButtons.forEach(btn => btn.style.display = 'inline-block');
    });
}