document.getElementById('image-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const imageName = document.getElementById('foto').value;

    const bucketName = 'vision-image-files-bucket'; //Substituir pelo seu bucket

    try {
        const response = await fetch('https://jntnuwkzuj.execute-api.us-east-1.amazonaws.com/v2/vision', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                imageName: imageName,
                bucket: bucketName
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResultV2(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Ocorreu um erro ao buscar os dados. Verifique o console para mais detalhes.');
    }
});

document.getElementById('analisar-emocao').addEventListener('click', async () => {
    const imageName = document.getElementById('foto').value;
    const bucketName = 'vision-image-files-bucket';

    try {
        const response = await fetch('https://jntnuwkzuj.execute-api.us-east-1.amazonaws.com/v1/vision', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                imageName: imageName,
                bucket: bucketName
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResultV1(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Ocorreu um erro ao buscar os dados. Verifique o console para mais detalhes.');
    }
});

document.getElementById('ver-imagem').addEventListener('click', () => {
    const imageName = document.getElementById('foto').value;
    const bucketName = 'vision-image-files-bucket';
    const imageUrl = `https://${bucketName}.s3.amazonaws.com/${imageName}`;

    displayImage(imageUrl);
});

function displayResultV2(data) {
    const resultDiv = document.getElementById('result');
    let html = '<table><tr><th>Nome</th><th>Confiança</th></tr>';

    if (data.pets && data.pets[0].labels) {
        data.pets[0].labels.forEach(label => {
            html += `<tr><td>${label.Name}</td><td>${label.Confidence.toFixed(2)}%</td></tr>`;
        });
    } else {
        html += '<tr><td colspan="2">No labels found</td></tr>';
    }

    html += '</table>';

    if (data.pets[0].Dicas) {
        html += `<p><strong>Dica:</strong> ${data.pets[0].Dicas}</p>`;
    } else {
        html += `<p><strong>Sem dica</strong></p>`;
    }

    resultDiv.innerHTML = html;
}

function displayResultV1(data) {
    const resultDiv = document.getElementById('result');
    let html = '<table><tr><th>Emoção</th><th>Confiança</th><th>Posição (Height, Left, Top, Width)</th></tr>';

    if (data.faces && data.faces.length > 0) {
        data.faces.forEach(face => {
            if (face.classified_emotion !== null) {
                html += `<tr>
                    <td>${face.classified_emotion}</td>
                    <td>${face.classified_emotion_confidence !== null ? face.classified_emotion_confidence.toFixed(2) + '%' : 'N/A'}</td>
                    <td>${face.position.Height !== null ? face.position.Height.toFixed(2) : 'N/A'}, ${face.position.Left !== null ? face.position.Left.toFixed(2) : 'N/A'}, ${face.position.Top !== null ? face.position.Top.toFixed(2) : 'N/A'}, ${face.position.Width !== null ? face.position.Width.toFixed(2) : 'N/A'}</td>
                </tr>`;
            } else {
                html += '<tr><td colspan="3">No emotions found</td></tr>';
            }
        });
    } else {
        html += '<tr><td colspan="3">No emotions found</td></tr>';
    }

    html += '</table>';
    resultDiv.innerHTML = html;
}

function displayImage(url) {
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = `<img src="${url}" alt="Imagem do S3">`;
}
