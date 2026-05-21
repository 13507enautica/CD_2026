let h2 = document.querySelector('h2');
let map;

console.log(map);

// Função para inicializar ou atualizar o mapa
function updateMap(lat, lon) {
    

    if (map === undefined) {
        map = L.map('mapid').setView([lat, lon], 13);
    } else {
        map.remove();
        map = L.map('mapid').setView([lat, lon], 13);
    }

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([lat, lon]).addTo(map)
        .bindPopup('Local inserido!')
        .openPopup();
}

// Atualizar o mapa com base na localização do navegador
function success(pos) {
    console.log(pos.coords.latitude, pos.coords.longitude);
    updateMap(pos.coords.latitude, pos.coords.longitude);
}

function error(err) {
    console.log(err);
}

// Capturar localização atual do navegador
navigator.geolocation.watchPosition(success, error, {
    enableHighAccuracy: true,
    timeout: 5000
});

// Adicionar evento ao botão para capturar valores do formulário
document.getElementById('updateMap').addEventListener('click', function () {
    const lat = parseFloat(document.getElementById('latitude').value);
    const lon = parseFloat(document.getElementById('longitude').value);

    if (isNaN(lat) || isNaN(lon)) {
        alert('Por favor, insira valores válidos para latitude e longitude.');
        return;
    }

    updateMap(lat, lon);
});


