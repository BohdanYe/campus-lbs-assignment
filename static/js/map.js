// ============================================================
// Campus Services & Accessibility Finder
// Main Leaflet map
// ============================================================


// ------------------------------------------------------------
// 1. Map setup
// ------------------------------------------------------------

const CAMPUS_CENTER = [53.3552, -6.2798];

const map = L.map("map").setView(
    CAMPUS_CENTER,
    16
);


// OpenStreetMap base layer
const osmLayer = L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }
);

osmLayer.addTo(map);


// ------------------------------------------------------------
// 2. Map layers
// ------------------------------------------------------------

// FeatureGroup is used because it supports getBounds().
const placesLayer = L.featureGroup().addTo(map);
const routesLayer = L.featureGroup().addTo(map);
const zonesLayer = L.featureGroup().addTo(map);

// Temporary highlighted search results
const searchResultsLayer = L.featureGroup().addTo(map);

let searchMarker = null;
let radiusCircle = null;
let campusBounds = null;


// ------------------------------------------------------------
// 3. Colours
// ------------------------------------------------------------

function categoryColour(category) {

    const colours = {
        academic: "#0d6efd",
        library: "#6f42c1",
        student_services: "#6610f2",
        health: "#dc3545",
        sports: "#198754",
        cafe: "#fd7e14",
        study: "#20c997",
        accessibility: "#d63384",
        transport: "#6c757d",
        heritage: "#795548",
        community: "#0dcaf0",
        other: "#212529"
    };

    return colours[category] || "#212529";
}


function routeColour(type) {

    const colours = {
        walking: "#0d6efd",
        accessible: "#198754",
        cycling: "#fd7e14"
    };

    return colours[type] || "#212529";
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


// ------------------------------------------------------------
// 4. API helper
// ------------------------------------------------------------

async function fetchJSON(url) {

    const response = await fetch(url);

    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error("The server returned an invalid response.");
    }

    if (!response.ok) {

        const message =
            data.error ||
            data.detail ||
            "The request failed.";

        throw new Error(message);
    }

    return data;
}


// ------------------------------------------------------------
// 5. Place popup
// ------------------------------------------------------------

function createPlacePopup(properties) {

    const buildingCode = properties.building_code
        ? `
            <div>
                <strong>Building code:</strong>
                ${properties.building_code}
            </div>
        `
        : "";

    return `
        <div style="min-width: 220px;">

            <h6 class="mb-2">
                ${properties.name}
            </h6>

            ${buildingCode}

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

            <hr class="my-2">

            <p class="mb-0">
                ${properties.description || "No description available."}
            </p>

        </div>
    `;
}


// ------------------------------------------------------------
// 6. Load places
// ------------------------------------------------------------

async function loadPlaces() {

    const categoryElement =
        document.getElementById("categoryFilter");

    const accessibleElement =
        document.getElementById("accessibleOnly");

    const category =
        categoryElement ? categoryElement.value : "";

    const accessible =
        accessibleElement ? accessibleElement.checked : false;


    const params = new URLSearchParams();

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


    data.features.forEach(feature => {

        const properties = feature.properties;
        const coordinates = feature.geometry.coordinates;

        const marker = L.circleMarker(
            [
                coordinates[1],
                coordinates[0]
            ],
            {
                radius: 8,
                color: "#ffffff",
                weight: 2,
                fillColor: categoryColour(
                    properties.category
                ),
                fillOpacity: 0.95
            }
        );


        marker.bindPopup(
            createPlacePopup(properties)
        );

        marker.addTo(placesLayer);
    });


    const placeCount =
        document.getElementById("placeCount");

    if (placeCount) {
        placeCount.textContent =
            data.features.length;
    }
}


// ------------------------------------------------------------
// 7. Load routes
// ------------------------------------------------------------

async function loadRoutes() {

    const data =
        await fetchJSON("/api/routes/");

    routesLayer.clearLayers();


    data.features.forEach(feature => {

        const properties = feature.properties;

        const layer = L.geoJSON(
            feature,
            {
                style: {
                    color: routeColour(
                        properties.route_type
                    ),
                    weight: 5,
                    opacity: 0.9
                }
            }
        );


        layer.bindPopup(`
            <div style="min-width: 200px;">

                <h6>
                    ${properties.name}
                </h6>

                <div>
                    <strong>Route type:</strong>
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

                <hr class="my-2">

                <p class="mb-0">
                    ${properties.description || ""}
                </p>

            </div>
        `);


        layer.addTo(routesLayer);
    });


    const routeCount =
        document.getElementById("routeCount");

    if (routeCount) {
        routeCount.textContent =
            data.features.length;
    }
}


// ------------------------------------------------------------
// 8. Load zones
// ------------------------------------------------------------

async function loadZones() {

    const data =
        await fetchJSON("/api/zones/");

    zonesLayer.clearLayers();


    data.features.forEach(feature => {

        const properties = feature.properties;

        const layer = L.geoJSON(
            feature,
            {
                style: {
                    color: zoneColour(
                        properties.zone_type
                    ),
                    weight:
                        properties.zone_type === "campus"
                            ? 4
                            : 2,
                    fillOpacity:
                        properties.zone_type === "campus"
                            ? 0.05
                            : 0.14
                }
            }
        );


        layer.bindPopup(`
            <div style="min-width: 200px;">

                <h6>
                    ${properties.name}
                </h6>

                <div>
                    <strong>Zone type:</strong>
                    ${properties.zone_type}
                </div>

                <hr class="my-2">

                <p class="mb-0">
                    ${properties.description || ""}
                </p>

            </div>
        `);


        layer.addTo(zonesLayer);
    });


    const zoneCount =
        document.getElementById("zoneCount");

    if (zoneCount) {
        zoneCount.textContent =
            data.features.length;
    }


    // Automatically frame the whole campus.
    if (zonesLayer.getLayers().length > 0) {

        const bounds =
            zonesLayer.getBounds();

        if (bounds.isValid()) {

            campusBounds = bounds;

            map.fitBounds(
                bounds,
                {
                    padding: [25, 25]
                }
            );
        }
    }
}


// ------------------------------------------------------------
// 9. Populate zone selection
// ------------------------------------------------------------

async function populateZoneSelect() {

    const select =
        document.getElementById("zoneSelect");

    if (!select) {
        return;
    }


    const data =
        await fetchJSON("/api/zones/");


    select.innerHTML = `
        <option value="">
            Select a zone
        </option>
    `;


    data.features.forEach(feature => {

        const option =
            document.createElement("option");

        option.value = feature.id;

        option.textContent =
            feature.properties.name;

        select.appendChild(option);
    });
}


// ------------------------------------------------------------
// 10. Search location
// ------------------------------------------------------------

function setSearchPoint(lat, lng) {

    const latInput =
        document.getElementById("searchLat");

    const lngInput =
        document.getElementById("searchLng");


    if (latInput) {
        latInput.value =
            lat.toFixed(6);
    }

    if (lngInput) {
        lngInput.value =
            lng.toFixed(6);
    }


    if (searchMarker) {

        map.removeLayer(
            searchMarker
        );
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


// ------------------------------------------------------------
// 11. Read selected coordinates
// ------------------------------------------------------------

function getSelectedCoordinates() {

    const latElement =
        document.getElementById("searchLat");

    const lngElement =
        document.getElementById("searchLng");


    if (!latElement || !lngElement) {

        throw new Error(
            "Search coordinate fields are not available."
        );
    }


    const lat = latElement.value;
    const lng = lngElement.value;


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


// ------------------------------------------------------------
// 12. Clear search results
// ------------------------------------------------------------

function clearSearchResults() {

    searchResultsLayer.clearLayers();

    const results =
        document.getElementById("resultsList");

    if (results) {
        results.innerHTML = "";
    }
}


// ------------------------------------------------------------
// 13. Display place search results
// ------------------------------------------------------------

function showPlaceResults(
    features,
    title
) {

    clearSearchResults();


    const resultMessage =
        document.getElementById(
            "resultsMessage"
        );

    const resultsList =
        document.getElementById(
            "resultsList"
        );


    if (resultMessage) {

        resultMessage.textContent =
            `${title}: ${features.length} result(s)`;
    }


    features.forEach(
        (feature, index) => {

            const properties =
                feature.properties;

            const coordinates =
                feature.geometry.coordinates;


            const marker =
                L.circleMarker(
                    [
                        coordinates[1],
                        coordinates[0]
                    ],
                    {
                        radius: 11,
                        color: "#000000",
                        weight: 2,
                        fillColor: "#ffc107",
                        fillOpacity: 1
                    }
                );


            marker.bindPopup(
                createPlacePopup(properties)
            );

            marker.addTo(
                searchResultsLayer
            );


            if (resultsList) {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "result-item";


                const distance =
                    properties.distance_m !== null &&
                    properties.distance_m !== undefined
                        ? `${properties.distance_m} m`
                        : "Distance unavailable";


                item.innerHTML = `
                    <strong>
                        ${index + 1}. ${properties.name}
                    </strong>

                    <div class="result-distance">
                        ${distance}
                    </div>
                `;


                item.addEventListener(
                    "click",
                    () => {

                        map.setView(
                            [
                                coordinates[1],
                                coordinates[0]
                            ],
                            19
                        );

                        marker.openPopup();
                    }
                );


                resultsList.appendChild(
                    item
                );
            }
        }
    );
}


// ------------------------------------------------------------
// 14. Nearest place search
// ------------------------------------------------------------

async function findNearest() {

    try {

        const { lat, lng } =
            getSelectedCoordinates();


        const limitElement =
            document.getElementById(
                "nearestLimit"
            );


        const limit =
            limitElement
                ? limitElement.value
                : 5;


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


// ------------------------------------------------------------
// 15. Radius search
// ------------------------------------------------------------

async function findWithinRadius() {

    try {

        const { lat, lng } =
            getSelectedCoordinates();


        const radiusElement =
            document.getElementById(
                "radiusInput"
            );


        const radius =
            radiusElement
                ? Number(radiusElement.value)
                : 150;


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
            radiusCircle.getBounds(),
            {
                padding: [20, 20]
            }
        );

    } catch (error) {

        alert(error.message);
    }
}


// ------------------------------------------------------------
// 16. Find containing zones
// ------------------------------------------------------------

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


        const message =
            document.getElementById(
                "resultsMessage"
            );

        const results =
            document.getElementById(
                "resultsList"
            );


        if (message) {

            message.textContent =
                `Containing zones: ${data.features.length}`;
        }


        data.features.forEach(
            feature => {

                const layer =
                    L.geoJSON(
                        feature,
                        {
                            style: {
                                color: "#ffc107",
                                weight: 5,
                                fillOpacity: 0.22
                            }
                        }
                    );


                layer.addTo(
                    searchResultsLayer
                );


                if (results) {

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

                    results.appendChild(
                        item
                    );
                }
            }
        );

    } catch (error) {

        alert(error.message);
    }
}


// ------------------------------------------------------------
// 17. Find routes intersecting a zone
// ------------------------------------------------------------

async function findIntersectingRoutes() {

    const zoneSelect =
        document.getElementById(
            "zoneSelect"
        );


    if (!zoneSelect) {
        return;
    }


    const zoneId =
        zoneSelect.value;


    if (!zoneId) {

        alert(
            "Select a zone first."
        );

        return;
    }


    try {

        const data =
            await fetchJSON(
                `/api/routes/intersecting-zone/?zone_id=${zoneId}`
            );


        clearSearchResults();


        const message =
            document.getElementById(
                "resultsMessage"
            );

        const results =
            document.getElementById(
                "resultsList"
            );


        if (message) {

            message.textContent =
                `Intersecting routes: ${data.features.length}`;
        }


        data.features.forEach(
            feature => {

                const layer =
                    L.geoJSON(
                        feature,
                        {
                            style: {
                                color: "#dc3545",
                                weight: 8,
                                opacity: 1
                            }
                        }
                    );


                layer.addTo(
                    searchResultsLayer
                );


                if (results) {

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
                            ${feature.properties.route_type}
                        </div>
                    `;

                    results.appendChild(
                        item
                    );
                }
            }
        );

    } catch (error) {

        alert(error.message);
    }
}


// ------------------------------------------------------------
// 18. Reset
// ------------------------------------------------------------

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


    const latInput =
        document.getElementById(
            "searchLat"
        );

    const lngInput =
        document.getElementById(
            "searchLng"
        );


    if (latInput) {
        latInput.value = "";
    }

    if (lngInput) {
        lngInput.value = "";
    }


    const message =
        document.getElementById(
            "resultsMessage"
        );


    if (message) {

        message.textContent =
            "No spatial search performed yet.";
    }


    if (
        campusBounds &&
        campusBounds.isValid()
    ) {

        map.fitBounds(
            campusBounds,
            {
                padding: [25, 25]
            }
        );

    } else {

        map.setView(
            CAMPUS_CENTER,
            16
        );
    }
}


// ------------------------------------------------------------
// 19. Event listeners
// ------------------------------------------------------------

const applyFilterButton =
    document.getElementById(
        "applyPlaceFilter"
    );

if (applyFilterButton) {

    applyFilterButton.addEventListener(
        "click",
        loadPlaces
    );
}


const findNearestButton =
    document.getElementById(
        "findNearest"
    );

if (findNearestButton) {

    findNearestButton.addEventListener(
        "click",
        findNearest
    );
}


const radiusButton =
    document.getElementById(
        "findRadius"
    );

if (radiusButton) {

    radiusButton.addEventListener(
        "click",
        findWithinRadius
    );
}


const zoneButton =
    document.getElementById(
        "findZone"
    );

if (zoneButton) {

    zoneButton.addEventListener(
        "click",
        findContainingZone
    );
}


const intersectionButton =
    document.getElementById(
        "findIntersectingRoutes"
    );

if (intersectionButton) {

    intersectionButton.addEventListener(
        "click",
        findIntersectingRoutes
    );
}


const resetButton =
    document.getElementById(
        "resetSearch"
    );

if (resetButton) {

    resetButton.addEventListener(
        "click",
        resetSearch
    );
}


// ------------------------------------------------------------
// 20. Layer controls
// ------------------------------------------------------------

const placesCheckbox =
    document.getElementById(
        "showPlaces"
    );

if (placesCheckbox) {

    placesCheckbox.addEventListener(
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
}


const routesCheckbox =
    document.getElementById(
        "showRoutes"
    );

if (routesCheckbox) {

    routesCheckbox.addEventListener(
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
}


const zonesCheckbox =
    document.getElementById(
        "showZones"
    );

if (zonesCheckbox) {

    zonesCheckbox.addEventListener(
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
}


// ------------------------------------------------------------
// 21. Initialise application
// ------------------------------------------------------------

async function initialiseApplication() {

    try {

        // Zones are loaded first so the map can frame the campus.
        await loadZones();

        await Promise.all([
            loadRoutes(),
            loadPlaces()
        ]);

        await populateZoneSelect();


        console.log(
            "Campus LBS application loaded successfully."
        );

    } catch (error) {

        console.error(
            "Application failed to initialise:",
            error
        );

        alert(
            "Could not load campus spatial data."
        );
    }
}


initialiseApplication();