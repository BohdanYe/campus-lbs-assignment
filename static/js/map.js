const CAMPUS_CENTER = [53.3550, -6.2792];

const map = L.map("map").setView(
    CAMPUS_CENTER,
    17
);


const osmLayer = L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution:
            "&copy; OpenStreetMap contributors"
    }
);

osmLayer.addTo(map);


const placesLayer = L.layerGroup().addTo(map);
const routesLayer = L.layerGroup().addTo(map);
const zonesLayer = L.layerGroup().addTo(map);

const searchResultsLayer =
    L.layerGroup().addTo(map);


let searchMarker = null;
let radiusCircle = null;


function categoryColour(category) {

    const colours = {
        library: "#6f42c1",
        cafe: "#fd7e14",
        study: "#0d6efd",
        printer: "#6c757d",
        bike: "#198754",
        accessibility: "#dc3545",
        other: "#212529"
    };

    return colours[category] || "#212529";
}


function zoneColour(type) {

    const colours = {
        campus: "#0d6efd",
        pedestrian: "#fd7e14",
        study: "#6f42c1",
        restricted: "#dc3545",
        accessible: "#198754",
        green: "#20c997"
    };

    return colours[type] || "#6c757d";
}


function routeColour(type) {

    const colours = {
        walking: "#0d6efd",
        accessible: "#198754",
        cycling: "#fd7e14"
    };

    return colours[type] || "#212529";
}


async function fetchJSON(url) {

    const response = await fetch(url);

    const data = await response.json();

    if (!response.ok) {
        const message =
            data.error ||
            data.detail ||
            "Request failed.";

        throw new Error(message);
    }

    return data;
}


async function loadPlaces() {

    const category =
        document.getElementById(
            "categoryFilter"
        ).value;

    const accessible =
        document.getElementById(
            "accessibleOnly"
        ).checked;

    const params =
        new URLSearchParams();

    if (category) {
        params.append(
            "category",
            category
        );
    }

    if (accessible) {
        params.append(
            "is_accessible",
            "true"
        );
    }

    let url = "/api/places/";

    if (params.toString()) {
        url += `?${params.toString()}`;
    }

    const data = await fetchJSON(url);

    placesLayer.clearLayers();

    let count = 0;

    data.features.forEach(feature => {

        const properties =
            feature.properties;

        const coordinates =
            feature.geometry.coordinates;

        const marker = L.circleMarker(
            [
                coordinates[1],
                coordinates[0]
            ],
            {
                radius: 8,
                color: "#ffffff",
                weight: 2,
                fillColor:
                    categoryColour(
                        properties.category
                    ),
                fillOpacity: 0.95
            }
        );

        marker.bindPopup(`
            <div>
                <h6>${properties.name}</h6>
                <div>
                    <strong>Category:</strong>
                    ${properties.category}
                </div>
                <div>
                    <strong>Opening hours:</strong>
                    ${properties.opening_hours || "Not provided"}
                </div>
                <div>
                    <strong>Accessible:</strong>
                    ${properties.is_accessible ? "Yes" : "No"}
                </div>
                <p class="mt-2 mb-0">
                    ${properties.description || ""}
                </p>
            </div>
        `);

        marker.addTo(placesLayer);

        count += 1;
    });

    document.getElementById(
        "placeCount"
    ).textContent = count;
}


async function loadRoutes() {

    const data =
        await fetchJSON(
            "/api/routes/"
        );

    routesLayer.clearLayers();

    let count = 0;

    data.features.forEach(feature => {

        const properties =
            feature.properties;

        const layer =
            L.geoJSON(
                feature,
                {
                    style: {
                        color:
                            routeColour(
                                properties.route_type
                            ),
                        weight: 5,
                        opacity: 0.9
                    }
                }
            );

        layer.bindPopup(`
            <div>
                <h6>${properties.name}</h6>
                <div>
                    <strong>Type:</strong>
                    ${properties.route_type}
                </div>
                <div>
                    <strong>Distance:</strong>
                    ${properties.distance_m || "Unknown"} m
                </div>
                <div>
                    <strong>Accessible:</strong>
                    ${properties.is_accessible ? "Yes" : "No"}
                </div>
            </div>
        `);

        layer.addTo(routesLayer);

        count += 1;
    });

    document.getElementById(
        "routeCount"
    ).textContent = count;
}


async function loadZones() {

    const data =
        await fetchJSON(
            "/api/zones/"
        );

    zonesLayer.clearLayers();

    let count = 0;

    data.features.forEach(feature => {

        const properties =
            feature.properties;

        const layer =
            L.geoJSON(
                feature,
                {
                    style: {
                        color:
                            zoneColour(
                                properties.zone_type
                            ),
                        weight: 2,
                        fillOpacity: 0.15
                    }
                }
            );

        layer.bindPopup(`
            <div>
                <h6>${properties.name}</h6>
                <div>
                    <strong>Zone type:</strong>
                    ${properties.zone_type}
                </div>
                <p class="mt-2 mb-0">
                    ${properties.description || ""}
                </p>
            </div>
        `);

        layer.addTo(zonesLayer);

        count += 1;
    });

    document.getElementById(
        "zoneCount"
    ).textContent = count;
}


function getSelectedCoordinates() {

    const lat =
        document.getElementById(
            "searchLat"
        ).value;

    const lng =
        document.getElementById(
            "searchLng"
        ).value;

    if (!lat || !lng) {
        throw new Error(
            "Click on the map to choose a search location first."
        );
    }

    return {
        lat: Number(lat),
        lng: Number(lng)
    };
}


function setSearchPoint(lat, lng) {

    document.getElementById(
        "searchLat"
    ).value = lat.toFixed(6);

    document.getElementById(
        "searchLng"
    ).value = lng.toFixed(6);

    if (searchMarker) {
        map.removeLayer(searchMarker);
    }

    searchMarker = L.marker(
        [lat, lng]
    )
    .addTo(map)
    .bindPopup(
        "Selected search location"
    )
    .openPopup();
}


map.on(
    "click",
    event => {
        setSearchPoint(
            event.latlng.lat,
            event.latlng.lng
        );
    }
);


function clearSearchResults() {

    searchResultsLayer.clearLayers();

    document.getElementById(
        "resultsList"
    ).innerHTML = "";
}


function showPlaceResults(
    features,
    title
) {

    clearSearchResults();

    const results =
        document.getElementById(
            "resultsList"
        );

    document.getElementById(
        "resultsMessage"
    ).textContent =
        `${title}: ${features.length} result(s)`;

    features.forEach(
        (feature, index) => {

            const props =
                feature.properties;

            const coords =
                feature.geometry.coordinates;

            const marker =
                L.circleMarker(
                    [
                        coords[1],
                        coords[0]
                    ],
                    {
                        radius: 11,
                        color: "#000000",
                        weight: 2,
                        fillColor: "#ffc107",
                        fillOpacity: 1
                    }
                )
                .addTo(searchResultsLayer);

            marker.bindPopup(
                `<strong>${props.name}</strong><br>
                 Distance:
                 ${props.distance_m ?? "Unknown"} m`
            );

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "result-item";

            item.innerHTML = `
                <strong>
                    ${index + 1}. ${props.name}
                </strong>
                <div class="result-distance">
                    ${props.distance_m ?? "Unknown"} metres
                </div>
            `;

            item.addEventListener(
                "click",
                () => {
                    map.setView(
                        [
                            coords[1],
                            coords[0]
                        ],
                        19
                    );

                    marker.openPopup();
                }
            );

            results.appendChild(item);
        }
    );
}


async function findNearest() {

    try {

        const { lat, lng } =
            getSelectedCoordinates();

        const limit =
            document.getElementById(
                "nearestLimit"
            ).value;

        const url =
            `/api/places/nearest/` +
            `?lat=${lat}` +
            `&lng=${lng}` +
            `&limit=${limit}`;

        const data =
            await fetchJSON(url);

        showPlaceResults(
            data.features,
            "Nearest places"
        );

    } catch (error) {

        alert(error.message);
    }
}


async function findWithinRadius() {

    try {

        const { lat, lng } =
            getSelectedCoordinates();

        const radius =
            Number(
                document.getElementById(
                    "radiusInput"
                ).value
            );

        const url =
            `/api/places/within-radius/` +
            `?lat=${lat}` +
            `&lng=${lng}` +
            `&radius=${radius}`;

        const data =
            await fetchJSON(url);

        showPlaceResults(
            data.features,
            "Places within radius"
        );

        if (radiusCircle) {
            map.removeLayer(
                radiusCircle
            );
        }

        radiusCircle =
            L.circle(
                [lat, lng],
                {
                    radius: radius,
                    color: "#0dcaf0",
                    weight: 2,
                    fillOpacity: 0.08
                }
            )
            .addTo(map);

        map.fitBounds(
            radiusCircle.getBounds()
        );

    } catch (error) {

        alert(error.message);
    }
}


async function findContainingZone() {

    try {

        const { lat, lng } =
            getSelectedCoordinates();

        const url =
            `/api/zones/contains-point/` +
            `?lat=${lat}` +
            `&lng=${lng}`;

        const data =
            await fetchJSON(url);

        clearSearchResults();

        const list =
            document.getElementById(
                "resultsList"
            );

        document.getElementById(
            "resultsMessage"
        ).textContent =
            `Containing zones: ${data.features.length}`;

        data.features.forEach(
            feature => {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "result-item";

                item.innerHTML = `
                    <strong>
                        ${feature.properties.name}
                    </strong>
                    <div>
                        ${feature.properties.zone_type}
                    </div>
                `;

                list.appendChild(item);

                L.geoJSON(
                    feature,
                    {
                        style: {
                            color: "#ffc107",
                            weight: 5,
                            fillOpacity: 0.25
                        }
                    }
                )
                .addTo(searchResultsLayer);
            }
        );

    } catch (error) {

        alert(error.message);
    }
}


function resetSearch() {

    clearSearchResults();

    if (searchMarker) {
        map.removeLayer(
            searchMarker
        );

        searchMarker = null;
    }

    if (radiusCircle) {
        map.removeLayer(
            radiusCircle
        );

        radiusCircle = null;
    }

    document.getElementById(
        "searchLat"
    ).value = "";

    document.getElementById(
        "searchLng"
    ).value = "";

    document.getElementById(
        "resultsMessage"
    ).textContent =
        "No spatial search performed yet.";

    map.setView(
        CAMPUS_CENTER,
        17
    );
}


document.getElementById(
    "applyPlaceFilter"
).addEventListener(
    "click",
    loadPlaces
);


document.getElementById(
    "findNearest"
).addEventListener(
    "click",
    findNearest
);


document.getElementById(
    "findRadius"
).addEventListener(
    "click",
    findWithinRadius
);


document.getElementById(
    "findZone"
).addEventListener(
    "click",
    findContainingZone
);


document.getElementById(
    "resetSearch"
).addEventListener(
    "click",
    resetSearch
);


document.getElementById(
    "showPlaces"
).addEventListener(
    "change",
    event => {

        if (event.target.checked) {
            map.addLayer(
                placesLayer
            );
        } else {
            map.removeLayer(
                placesLayer
            );
        }
    }
);


document.getElementById(
    "showRoutes"
).addEventListener(
    "change",
    event => {

        if (event.target.checked) {
            map.addLayer(
                routesLayer
            );
        } else {
            map.removeLayer(
                routesLayer
            );
        }
    }
);


document.getElementById(
    "showZones"
).addEventListener(
    "change",
    event => {

        if (event.target.checked) {
            map.addLayer(
                zonesLayer
            );
        } else {
            map.removeLayer(
                zonesLayer
            );
        }
    }
);


async function initialiseApplication() {

    try {

        await Promise.all([
            loadZones(),
            loadRoutes(),
            loadPlaces()
        ]);

    } catch (error) {

        console.error(
            "Application failed to initialise:",
            error
        );

        alert(
            "Could not load spatial data."
        );
    }
}


initialiseApplication();