var function_is_running = false;
var PORT = 7306;

$(document).ready(connect_to_socket);

function connect_to_socket() {
    if (function_is_running) return;

    console.log("Trying to connect...");
    function_is_running = true;
    let socket = new WebSocket("ws://localhost:" + PORT);
    socket.onopen = function (e) {
        console.log("OPENED");
    };
    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        console.log(`New event: ${event.data}`);
        create_players(data);
    };

    socket.onclose = function (event) {
        if (event.wasClean) console.log('CLEAN EXIT: ' + event);
        else console.log('UNCLEAN EXIT: ' + event);
        reconnect_to_socket();
    };

    socket.onerror = function (error) {
        console.log('ERROR: ' + error);
        reconnect_to_socket()
    };
}

function reconnect_to_socket(message) {
    console.log('Reconnecting..')
    function_is_running = false;
    setTimeout(function () {
        connect_to_socket();
    }, 500);
}

// DEBUG
var message = '[{"name": "Henry the fifth sdad sssssAAAAAAAAAAAA", "score": "3", "color": "#FF2222", "faction": "./factions/GDI.jpg", "team": 1}, {"name": "bb", "score": "1", "color": "#1CE11C", "faction": "./factions/GDI.jpg", "team": 2},{"name": "Henry the second", "score": "3", "color": "#5555FF", "faction": "./factions/GDI.jpg", "team": 1}]';
var ndata = JSON.parse(message);
create_players(ndata);

// Get with default value 
function getd(o, key, default_value) {
    if (o[key] !== "" && o[key] !== undefined) return o[key];
    else return default_value;
}

// Goes over players and adds them to the document
function create_players(data) {
    // Clean main
    $("#main").html("");
    // Sort players based on teams
    let ndata = data.sort(function (a, b) { return getd(a, "team", 99) - getd(b, "team", 99) });
    // Create new players
    for (let i = 0; i < ndata.length; i++) {
        if (i == 0 || ndata[i]["team"] != ndata[i - 1]["team"] || ndata[i]["team"] == "")
            $("#main").append(`<div class='team'><div class='teamico'><span>${ndata[i]["team"]}</span></div></div>`);
        create_player(ndata[i]);
    }

    // Setup team structure
    setup_teams(ndata);
    // Fit text to given width
    $(".name").textfill({});
}

// Creates a player element and adds it to the document
function create_player(data) {
    let el = `<div class="player">
        <div class="overlay" style="background: ${data['color']}"></div>
        <img class="faction" src="${data['faction']}">
        <div class="ptext name"><span>${data['name']}</span></div>
        <div class="ptext score"><span>${data['score']}</span></div>
    </div>`;
    $(".team:last").append(el);
}

// Team setup
function setup_teams(data) {
    let no_teams = true;
    for (let i = 0; i < data.length; i++) {
        if (data[i]["team"] != "") {
            no_teams = false;
            break;
        }
    }
    if (no_teams) {
        $(".player").width("100%");
        $(".teamico").hide();
    } else {
        $(".player").width("90%");
        $(".teamico").show();
    }
}