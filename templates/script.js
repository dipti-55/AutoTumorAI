document.getElementById('upload-button').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = 224;
            canvas.height = 224;
            ctx.drawImage(img, 0, 0, 224, 224);
            const resizedImageData = canvas.toDataURL('image/jpeg');
            document.getElementById('image-preview').src = resizedImageData;
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
});

document.getElementById('predict-button').addEventListener('click', function() {
    const img = document.getElementById('image-preview').src;
    const data = { image: img.split(',')[1] }; // Extract base64 part

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result-box').style.display = 'block';
        document.getElementById('result-text').innerText = `Prediction: ${result[0].image}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
