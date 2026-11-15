document.addEventListener("DOMContentLoaded", () => {
  const selectGeocerca = document.getElementById("geofence_select");
  const inputNombre = document.getElementById("nombre_input");

  function completarNombre() {
    const opcion = selectGeocerca.options[selectGeocerca.selectedIndex];
    if (!opcion) return;
    const nombreLimpio = opcion.text.replace(/\s*\(ID:\s*\d+\)$/, "");
    inputNombre.value = nombreLimpio;
  }

  if (selectGeocerca && inputNombre) {
    selectGeocerca.addEventListener("change", completarNombre);
    if (!inputNombre.value) {
      completarNombre();
    }
  }

  const mapaDiv = document.getElementById("mapa-vecinal");
  if (mapaDiv && mapaDiv.dataset.geojson) {
    const geojsonData = JSON.parse(mapaDiv.dataset.geojson);

    const map = L.map("mapa-vecinal").setView([-33.123, -64.349], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    const poligono = L.geoJSON(geojsonData, {
      style: {
        color: "#123A7A",
        weight: 2,
        fillColor: "#1B4F9C",
        fillOpacity: 0.25,
      },
    }).addTo(map);

    map.fitBounds(poligono.getBounds());
  }
});