fetch('/hello')
    .then(response => response.text())
    .then(text => {
        document.getElementById('hello').innerText = text;
    });